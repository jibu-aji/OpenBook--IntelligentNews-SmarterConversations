from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import RegistrationForm, LoginForm
from news.models import *



# Only allow Admins (or Superusers) to access this
def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def staff_register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # restrict roles to editor or moderator only
        if role not in ["editor", "moderator"]:
            messages.error(request, "Invalid role selected.")
            return redirect("staff_register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("staff_register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        messages.success(request, f"{role.capitalize()} created successfully!")
        return redirect("login")

    return render(request, "accounts/staff_register.html")

@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("login")
    return render(request, "accounts/admin_dashboard.html")

@login_required
def editor_dashboard(request):
    if request.user.role != "editor":
        return redirect("login")
    return render(request, "accounts/editor_dashboard.html")

@login_required
def moderator_dashboard(request):
    if request.user.role != "moderator":
        return redirect("login")
    return render(request, "accounts/moderator_dashboard.html")



#---------BASE--------

def home(request):
    user = request.user

    # Authenticated users: redirect based on role
    if user.is_authenticated:
        if user.role == "admin":
            return redirect("admin_dashboard")
        elif user.role == "editor":
            return redirect("editor_dashboard")
        elif user.role == "moderator":
            return redirect("moderator_dashboard")
        elif user.role == "user":
            return redirect("user_dashboard")
        else:
            return render(request, "base.html")

    # Anonymous users: render base.html with latest articles
    latest_articles = Article.objects.filter(status='published').order_by('-created_at')[:5]
    context = {
        "latest_articles": latest_articles
    }
    return render(request, "base.html", context)
    
# --------------------------
# Registration View
# --------------------------


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})




# --------------------------
# Login View
# --------------------------

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect by role
            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "editor":
                return redirect("editor_dashboard")
            elif user.role == "moderator":
                return redirect("moderator_dashboard")
            else:
                return redirect("user_dashboard")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


# --------------------------
# Logout View
# --------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


# --------------------------
# Profile View
# --------------------------
@login_required
def profile_view(request):
    user = request.user
    return render(request, "accounts/profile.html", {"user": user})
