from django import forms
from .models import Article, Category, ArticleImage

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body", "category", "status", "content_type"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        

class EditorArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "excerpt", "body", "category", "content_type"]  # remove 'status'

    def save(self, commit=True, author=None):
        article = super().save(commit=False)
        article.status = 'review'  # editor can only submit for review
        if author:
            article.author = author
        if commit:
            article.save()
        return article

class ArticleImageForm(forms.ModelForm):
    image = forms.ImageField(label="Image", required=False)

    class Meta:
        model = ArticleImage
        fields = ["image", "caption"]