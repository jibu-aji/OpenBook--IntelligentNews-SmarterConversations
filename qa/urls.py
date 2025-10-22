from django.urls import path
from . import views

urlpatterns = [
    # path('article/<int:pk>/', views.article_qa_detail, name='article_qa_detail'),
    path("generate/<int:article_id>/", views.generate_article_qa, name="generate_article_qa"),
    path("opi/", views.opi_chat_page, name="opi_chat_page"),
    path("opi/chat/", views.opi_chat_api, name="opi_chat_api"),  # AJAX endpoint
]
