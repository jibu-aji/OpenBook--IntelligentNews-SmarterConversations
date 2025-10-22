from django.urls import path
from . import views

urlpatterns = [
    path("editor/articles/", views.editor_article_list, name="editor_article_list"),
    path("editor/articles/create/", views.create_article, name="create_article"),
    path("editor/articles/<int:pk>/edit/", views.update_article, name="update_article"),
    path("editor/articles/<int:pk>/delete/", views.delete_article, name="delete_article"),

    path('editor/drafts/', views.editor_drafts, name='editor_drafts'),


     # ----- Category URLs -----
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.create_category, name="create_category"),
    path("categories/<int:pk>/edit/", views.update_category, name="update_category"),
    path("categories/<int:pk>/delete/", views.delete_category, name="delete_category"),
    
    
    #---------moderator--------
    path("moderator/articles/", views.moderator_article_list, name="moderator_article_list"),
    path("moderator/articles/<int:pk>/moderate/", views.moderate_article, name="moderate_article"),
    path("moderator/comments/", views.moderator_comment_view_list, name="moderator_comment_view_list"),
    path("moderator/comments/delete/<int:comment_id>/", views.moderator_delete_comment, name="moderator_delete_comment"),

    
    
    #-------------Users-------------------
    
    path("articles/", views.user_article_list, name="article_list"),
    # path("articles/<int:pk>/", views.user_article_detail, name="article_detail"),
    
    
    
    #---------------Visiting Pages--------------
    
    path('index', views.user_index, name = "user_index"),
    
    #--------------saved------------------
    path("article/<int:pk>/save/", views.user_article_save, name="user_article_save"),
    

    path('user_dashboard', views.user_dashboard, name = "user_dashboard"),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    # news/urls.py
    path('article/<int:pk>/<str:value>/', views.user_article_react, name='user_article_react'),


    
    path("saved/", views.user_saved_articles, name="user_saved_articles"),

    path('article/<int:pk>/', views.user_article_det, name='user_article_det'),  # Article detail



    #category:

    path("category/<slug:slug>/", views.category_articles, name="category_articles"),
    
    #search
    path("search/", views.article_search, name="article_search"),
    
    #blogs
    path("blogs/", views.blog_list, name="blog_list"),

]
