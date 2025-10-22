# qa/models.py
from django.db import models
from news.models import Article
from django.conf import settings

class ArticleQA(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="qa_pairs")
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QA for {self.article.title}: {self.question[:50]}"

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    context_articles = models.TextField(blank=True, null=True)  # simple record of which article titles used
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user = self.user.username if self.user else "anonymous"
        return f"Opi chat by {user} at {self.created_at:%Y-%m-%d %H:%M}"