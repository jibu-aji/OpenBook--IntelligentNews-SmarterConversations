from django.urls import path
from . import views

urlpatterns = [
    path("latest/", views.n_api_latest_news, name="n_api_latest_news"),
    # path("live/", views.n_api_live_news, name="n_api_live_news"),
    path("live/", views.n_api_live_news, name="n_api_live_news"),
]
