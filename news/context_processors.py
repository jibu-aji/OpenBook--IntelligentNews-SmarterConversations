from news.models import Category

def categories(request):
    return {
        'all_categories': Category.objects.all()
    }


from .models import Article

def latest_articles(request):
    return {
        "latest_articles": Article.objects.filter(status='published').order_by('-created_at')[:5]
    }