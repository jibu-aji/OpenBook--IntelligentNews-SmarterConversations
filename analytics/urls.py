from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_analytics, name='admin_analytics'),

]
