from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Category,ArticleImage,Comment,Reaction,SavedArticle,Comment
from .forms import ArticleForm,CategoryForm,EditorArticleForm,ArticleImageForm
from django.forms import modelformset_factory
from news.decorators import role_required


# --------- CATEGORY CRUD ----------

#--------------EDITOR AND ADMIN--------------------------------------------------------

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "news/category_list.html", {"categories": categories})

@login_required
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(request, "news/category_form.html", {"form": form})

@login_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "news/category_form.html", {"form": form})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("category_list")
    return render(request, "news/category_confirm_delete.html", {"category": category})
#------------------------------------------------------------------------------------------------------
# Editor Dashboard - list their own articles
@login_required
def editor_article_list(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, "news/editor_article_list.html", {"articles": articles})


# EDITOR --------------------------------
#----------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------



@login_required
def create_article(request):
    ImageFormSet = modelformset_factory(ArticleImage, form=ArticleImageForm, extra=3)
    
    if request.method == "POST":
        form = EditorArticleForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ArticleImage.objects.none())
        
        if form.is_valid() and formset.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()  # Save tags
            
            # Save images
            for image_form in formset.cleaned_data:
                if image_form:
                    image = image_form['image']
                    caption = image_form.get('caption', '')
                    ArticleImage.objects.create(article=article, image=image, caption=caption)
            
            messages.success(request, "Article created successfully.")
            return redirect("editor_article_list")
    else:
        form = EditorArticleForm()
        formset = ImageFormSet(queryset=ArticleImage.objects.none())
    
    return render(request, "news/article_form.html", {"form": form, "formset": formset})





# Update article
@login_required
def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == "POST":
        form = EditorArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully.")
            return redirect("editor_article_list")
    else:
        form = EditorArticleForm(instance=article)
    return render(request, "news/article_form.html", {"form": form})

# Delete article
@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == "POST":
        article.delete()
        messages.success(request, "Article deleted successfully.")
        return redirect("editor_article_list")
    return render(request, "news/article_confirm_delete.html", {"article": article})


@login_required
def editor_drafts(request):
    # Only show drafts/rejected for logged-in editor
    drafts = Article.objects.filter(author=request.user, status__in=['draft', 'rejected'])
    return render(request, 'news/editor_drafts.html', {'drafts': drafts})


#-------------END--------------


#-----------------------MODERATOR-----------------------------


@login_required
def moderator_article_list(request):
    # Show only draft/review articles
    articles = Article.objects.filter(status__in=['draft', 'review'])
    return render(request, "news/moderator_article_list.html", {"articles": articles})

@login_required
def moderate_article(request, pk):
    article = get_object_or_404(Article, id=pk)

    if request.method == "POST":
        action = request.POST.get("action")
        feedback = request.POST.get("feedback", "").strip()

        if action == 'publish':
            article.status = 'published'
            article.moderator_feedback = ''
            messages.success(request, f"✅ Your article '{article.title}' has been published.")
        elif action == 'reject':
            article.status = 'rejected'
            article.moderator_feedback = feedback
            messages.error(request, f"❌ Your article '{article.title}' was rejected: {feedback}")
        elif action == 'needs_update':
            article.status = 'draft'
            article.moderator_feedback = feedback
            messages.warning(request, f"📝 Your article '{article.title}' needs update: {feedback}")

        article.save()


        return redirect("moderator_article_list")

    return render(request, "news/moderator_article.html", {"article": article})


@login_required
def moderator_comment_view_list(request):
    # Role-based check (no decorator needed)
    if not request.user.is_authenticated or request.user.role != "moderator":
        messages.error(request, "You are not authorized to access this page.")
        return redirect("home")  # redirect to normal user dashboard

    comments = Comment.objects.all().order_by("-created_at")
    return render(request, "news/moderator_comment_view_list.html", {"comments": comments})


@login_required
def moderator_delete_comment(request, comment_id):
    """Allow moderator/admin to delete inappropriate comments (with confirmation page)."""

    # ✅ Role check
    if request.user.role not in ["moderator", "admin"]:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("user_dashboard")

    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        # If confirmed
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect("moderator_comment_view_list")

    # Otherwise show confirmation page
    return render(request, "news/moderator_confirm_delete_comment.html", {"comment": comment})

#----------------user-------------------------------
def user_article_list(request):
    articles = Article.objects.filter(status='published').order_by('-created_at')
    return render(request, "news/user_article_list.html", {"articles": articles})

def user_article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, status='published')
    return render(request, "news/user_article_details.html", {"article": article})


# Public Index Page (guest can view published articles)
def user_index(request):
    articles = Article.objects.filter(status="published").order_by('-created_at')
    return render(request, 'news/user_index.html', {'articles': articles})
from datetime import date
from django.db.models import Count



# Dashboard (requires login)


@login_required
def user_dashboard(request):
    today = date.today()

    # Current day news
    today_articles = Article.objects.filter(
        status='published',
        created_at__date=today
    ).order_by('-created_at')
    
    # 2️⃣ Trending articles (based on reactions + comments + saved_by)
    trending_articles = (
        Article.objects.filter(status='published')
        .annotate(
            popularity=Count('reactions', distinct=True) +
                       Count('comments', distinct=True) +
                       Count('saved_by', distinct=True)
        )
        .order_by('-popularity')[:6]
    )
    
    #exclude trending articles from all articles
    trending_ids = trending_articles.values_list('id', flat=True)

    articles = Article.objects.filter(status="published").exclude(id__in=trending_ids).order_by('-created_at')
    
    qa_articles = Article.objects.filter(status="published").order_by('-created_at')

    saved_articles = SavedArticle.objects.filter(user=request.user)
    return render(request, 'news/user_dashboard.html', {
        'articles': articles,
        'saved_articles': saved_articles,
        'today_articles': today_articles,
        'trending_articles': trending_articles,
        'qa_articles':qa_articles,
    })
    
    
    
from qa.models import ArticleQA  # only if you created model
# Article detail page
def user_article_det(request, pk):
    article = get_object_or_404(Article, pk=pk, status="published")
    comments = Comment.objects.filter(article=article).order_by('-created_at')
    
    # Get reaction counts
    like_count = Reaction.objects.filter(article=article, value=Reaction.LIKE).count()
    dislike_count = Reaction.objects.filter(article=article, value=Reaction.DISLIKE).count()
    
    #saved
    # Check if this article is saved by the current user
    is_saved = False
    if request.user.is_authenticated:
        try:
            is_saved = SavedArticle.objects.filter(user=request.user, article=article).exists()
        except SavedArticle.DoesNotExist:
            is_saved = False
            
    user_reaction = None
    if request.user.is_authenticated:
        try:
            user_reaction = Reaction.objects.get(user=request.user, article=article).value
        except Reaction.DoesNotExist:
            user_reaction = None
    
    if request.method == "POST":
        if request.user.is_authenticated:
            content = request.POST.get("content")
            if content.strip():
                Comment.objects.create(
                    user=request.user,
                    article=article,
                    text=content
                )
                messages.success(request, "Comment added successfully.")
                return redirect('user_article_det', pk=article.pk)
            else:
                messages.warning(request, "Comment cannot be empty.")
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')
  

    qa_pairs = article.qa_pairs.all()  # Already related_name in model
    return render(request, 'news/user_article_det.html', {
        'article': article,
        'comments': comments,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'user_reaction': user_reaction,
        "is_saved": is_saved,
        "qa_pairs": qa_pairs
        
    })
    

#--------delete comment------
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_staff:  # only moderators/admins can delete
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this comment.")
    return redirect('user_article_det', pk=comment.article.pk)


#-----------------like---------------------
@login_required
def user_article_react(request, pk, value):
    article = get_object_or_404(Article, pk=pk, status="published")
    
    mapping = {"like": Reaction.LIKE, "dislike": Reaction.DISLIKE}
    if value not in mapping:
        messages.error(request, "Invalid reaction type.")
        return redirect('user_article_det', pk=pk)

    value = mapping[value]
    label = "like" if value == Reaction.LIKE else "dislike"
    
    reaction, created = Reaction.objects.get_or_create(
    user=request.user,
    article=article,
    defaults={"value": value}  # 👈 ensures a value is set on creation
)

    if not created:
        if reaction.value == value:
            # Toggle off if same reaction clicked again
            reaction.delete()
            messages.info(request, f"You removed your {label}.")
        else:
            reaction.value = value
            reaction.save()
            messages.success(request, f"You {label}d this article.")
    else:
        messages.success(request,f"You {label}d this article")

    

    return redirect('user_article_det', pk=pk)



# if value not in ["like", "dislike"]:
#         messages.error(request, "Invalid reaction type.")
#         return redirect('user_article_det', pk=pk)

#     # Check if user already reacted
#     reaction, created = Reaction.objects.get_or_create(user=request.user, article=article)

#     if reaction.value == value:
#         # Toggle off if same reaction clicked again
#         reaction.delete()
#         messages.info(request, f"You removed your {value}.")
#     else:
#         # Update or set new reaction
#         reaction.value = value
#         reaction.save()
#         messages.success(request, f"You {value}d this article.")


#-------------------------------------saved----------------------------

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, SavedArticle


@login_required
def user_article_save(request, pk):
    """Toggle save/unsave for an article."""
    article = get_object_or_404(Article, pk=pk, status="published")

    saved, created = SavedArticle.objects.get_or_create(user=request.user, article=article)

    if not created:
        # Already saved → unsave
        saved.delete()
        messages.info(request, "Removed from your saved articles.")
    else:
        messages.success(request, "Article saved for later.")

    return redirect("user_article_det", pk=pk)


@login_required
def user_saved_articles(request):
    """List of all articles saved by the logged-in user."""
    saved_articles = SavedArticle.objects.filter(user=request.user).select_related("article").order_by("-created_at")

    context = {
        "saved_articles": saved_articles,
    }
    return render(request, "news/user_saved_articles.html", context)


@login_required
def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.article_set.filter(status="published").order_by('-created_at')
    return render(request, "news/category_articles.html", {"category": category, "articles": articles})


from django.db.models import Q

#search
@login_required
def article_search(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Article.objects.filter(
            Q(title__icontains=query)
            | Q(body__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(category__name__icontains=query)
        ).distinct()

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "news/article_search.html", context)


#blog
@login_required
def blog_list(request):
    """
    Display all published blog articles.
    """
    blogs = Article.objects.filter(status='published', content_type='blog').order_by('-created_at')
    context = {
        "blogs": blogs,
    }
    return render(request, "news/blog_list.html", context)