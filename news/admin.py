from django.contrib import admin
from .models import Category, Article,Comment,Reaction,SavedArticle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "content_type", "created_at")
    list_filter = ("status", "content_type", "category", "created_at")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "article", "text", "created_at")
    search_fields = ("text", "user__username", "article__title")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "article", "value", "created_at")
    list_filter = ("value", "created_at")
    search_fields = ("user__username", "article__title")
    ordering = ("-created_at",)


@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "article", "created_at")
    search_fields = ("user__username", "article__title")
    list_filter = ("created_at",)
    ordering = ("-created_at",)