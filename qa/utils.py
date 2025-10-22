import os
import re
from news.models import Article
import google.generativeai as genai
from django.conf import settings
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.genai import types

genai.configure(api_key=settings.GOOGLE_API_KEY)


def generate_qa_pairs(article_body, num_pairs=5):
    """Generate intelligent Q&A pairs using Gemini for a given article body."""
    model = genai.GenerativeModel("models/gemini-pro-latest")
    
    prompt = f"""
    You are an intelligent assistant for a news platform.
    From the following article content, generate {num_pairs} meaningful and factual Q&A pairs.
    Format the output strictly as:
    Q: <question>
    A: <answer>
    Only include the Q&A, no numbering, no titles.
    Article:
    {article_body}
    """
    
    response = model.generate_content(prompt)
    output = response.text.strip()
    
    # Parse the text into question-answer pairs
    qa_pairs = []
    current_q, current_a = None, None
    for line in output.split("\n"):
        line = line.strip()
        if line.startswith("Q:"):
            if current_q and current_a:
                qa_pairs.append((current_q, current_a))
            current_q = line[2:].strip()
            current_a = None
        elif line.startswith("A:"):
            current_a = line[2:].strip()
    if current_q and current_a:
        qa_pairs.append((current_q, current_a))
    
    return qa_pairs[:num_pairs]
#----------------------------------------------------------------------------------------------------

# Configure Gemini
API_KEY = getattr(settings, "GOOGLE_API_KEY", None)
if not API_KEY:
    # Raise later if not configured
    pass

genai.configure(api_key=API_KEY)


def tokenize(text):
    """Very small tokenizer / normalizer used for keyword counting."""
    if not text:
        return []
    text = text.lower()
    tokens = re.findall(r"\w+", text)
    return tokens


def retrieve_relevant_articles(query, top_n=3, min_matches=1):
    """Keyword-based retrieval of published articles."""
    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    candidates = Article.objects.filter(status="published").only(
        "id", "title", "excerpt", "body", "tags"
    )[:500]

    scored = []
    for art in candidates:
        text = " ".join(filter(None, [art.title or "", art.excerpt or "", art.body or "", art.tags or ""]))
        tokens = tokenize(text)
        score = sum(tokens.count(t) for t in q_tokens)
        if score >= min_matches:
            scored.append((score, art))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [art for score, art in scored[:top_n]]


def build_context_text(articles):
    """Constructs compact prompt context."""
    parts = []
    for a in articles:
        excerpt = a.excerpt if a.excerpt else (a.body[:400] + ("..." if len(a.body) > 400 else ""))
        parts.append(f"Title: {a.title}\nExcerpt: {excerpt}\nCategory: {a.category.name if a.category else 'N/A'}\n")
    return "\n---\n".join(parts)



API_KEY = getattr(settings, "GOOGLE_API_KEY", None)
if not API_KEY:
    raise RuntimeError("Gemini API key not configured (settings.GOOGLE_API_KEY missing).")
genai.configure(api_key=API_KEY)


def ask_gemini(question, context_text=None, model_name="models/gemini-pro-latest", temperature=0.0):
    system_prompt = (
        "You are Opi, an assistant for a news website. Answer clearly and concisely. "
        "Prefer information from provided article snippets. "
        "If context does not answer the question, respond with general knowledge."
    )

    if context_text:
        prompt = (
            f"{system_prompt}\n\nContext:\n{context_text}\n\nUser question: {question}\n\n"
            "Answer clearly and succinctly."
        )
    else:
        prompt = f"{system_prompt}\n\nUser question: {question}\n\nAnswer concisely."

    # Note safety_settings is a dictionary, not a list!
    safety_settings = {
        types.HarmCategory.HARM_CATEGORY_HARASSMENT: types.HarmBlockThreshold.BLOCK_NONE,
        types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: types.HarmBlockThreshold.BLOCK_NONE,
        types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: types.HarmBlockThreshold.BLOCK_NONE,
        types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: types.HarmBlockThreshold.BLOCK_NONE,
    }

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={
            "temperature": temperature,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 512,
        },
        safety_settings=safety_settings,
    )

    response = model.generate_content(prompt)

    if not response.candidates:
        return "Sorry, I couldn't generate a response right now. (No candidates returned)"

    candidate = response.candidates[0]
    finish_reason = getattr(candidate, "finish_reason", None)

    if not candidate.content or not getattr(candidate.content, "parts", None):
        if finish_reason == 2:
            return "Sorry, the response was filtered for safety."
        return "Sorry, Gemini didn't return usable text."

    text_parts = []
    for part in candidate.content.parts:
        if hasattr(part, "text"):
            text_parts.append(part.text)
    answer = "\n".join(text_parts).strip()

    if not answer:
        return "Sorry — Opi couldn't generate an answer right now."

    return answer

