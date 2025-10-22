from django.shortcuts import render, get_object_or_404, redirect
from news.models import Article
from .models import ArticleQA
from .utils import generate_qa_pairs
from django.contrib import messages
from django.conf import settings

def generate_article_qa(request, article_id):
    """Generate and save Q&A pairs for a specific article."""
    article = get_object_or_404(Article, id=article_id)

    # Ensure only once generation or regenerate on admin trigger
    existing = ArticleQA.objects.filter(article=article)
    if existing.exists():
        messages.info(request, "Q&A pairs already exist for this article.")
        return redirect("user_article_det", article.pk)
    
    qa_pairs = generate_qa_pairs(article.body, num_pairs=5)
    for q, a in qa_pairs:
        ArticleQA.objects.create(article=article, question=q, answer=a)
    
    messages.success(request, "AI-generated Q&A pairs created successfully!")
    return redirect("user_article_det", article.pk)



# qa/views.py
import json
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from qa.models import ChatHistory
from qa.utils import retrieve_relevant_articles, build_context_text, ask_gemini
from news.models import Article

@login_required
def opi_chat_page(request):
    """Render the chat page. Optionally pass last N chat messages for user."""
    # Optionally pass recent chat history
    recent = ChatHistory.objects.filter(user=request.user).order_by("-created_at")[:20]
    # reverse so oldest first
    recent = list(reversed(recent))
    from google.generativeai.types import HarmCategory
    print(list(HarmCategory))
    return render(request, "qa/opi_chat.html", {"recent": recent})

@require_POST
@login_required
def opi_chat_api(request):
    """
    AJAX endpoint: receives JSON {question: "..."}
    returns JSON {answer: "...", used_articles: [...], error: null}
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        question = payload.get("question", "").strip()
    except Exception:
        return JsonResponse({"error": "Invalid request payload."}, status=400)

    if not question:
        return JsonResponse({"error": "Empty question."}, status=400)

    # 1) retrieve relevant articles
    articles = retrieve_relevant_articles(question, top_n=3, min_matches=1)
    context_text = build_context_text(articles) if articles else None
    used_titles = [a.title for a in articles] if articles else []

    # 2) call Gemini
    try:
        answer = ask_gemini(question, context_text=context_text)
    except Exception as e:
        # safe error handling
        return JsonResponse({"error": f"AI error: {str(e)}"}, status=500)

    # 3) save chat history (non-blocking simple save)
    ChatHistory.objects.create(
        user=request.user,
        question=question,
        answer=answer,
        context_articles="; ".join(used_titles) if used_titles else ""
    )

    return JsonResponse({"answer": answer, "used_articles": used_titles})

