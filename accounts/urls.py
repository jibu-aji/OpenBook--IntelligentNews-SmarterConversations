from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path("staff-register/", views.staff_register_view, name="staff_register"), 
    
     path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("editor-dashboard/", views.editor_dashboard, name="editor_dashboard"),
    path("moderator-dashboard/", views.moderator_dashboard, name="moderator_dashboard"),
    
    # Placeholder for forgot password (future)
    # path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    # path('reset-password/<uuid:token>/', views.reset_password_view, name='reset_password'),

]
