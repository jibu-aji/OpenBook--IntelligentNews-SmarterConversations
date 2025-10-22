# import pandas as pd
# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64
# from django.shortcuts import render
# from news.models import Article, Comment, Reaction
# from accounts.models import User

# def admin_analytics(request):
#     # --- Data Preparation ---
#     articles = Article.objects.all().values("id", "category__name", "status", "created_at")
#     users = User.objects.all().values("id", "role")
#     reactions = Reaction.objects.all().values("article_id", "reaction_type")
#     comments = Comment.objects.all().values("article_id")

#     df_articles = pd.DataFrame(articles)
#     df_users = pd.DataFrame(users)
#     df_reactions = pd.DataFrame(reactions)
#     df_comments = pd.DataFrame(comments)

#     charts = {}

#     # --- Example Chart 1: Articles per Category ---
#     if not df_articles.empty:
#         category_counts = df_articles["category__name"].value_counts()
#         fig, ax = plt.subplots()
#         category_counts.plot(kind="bar", color="skyblue", ax=ax)
#         ax.set_title("Articles per Category")
#         charts["articles_by_category"] = plot_to_base64(fig)

#     # --- Example Chart 2: User Roles Distribution ---
#     if not df_users.empty:
#         role_counts = df_users["role"].value_counts()
#         fig, ax = plt.subplots()
#         role_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax)
#         ax.set_ylabel("")
#         ax.set_title("User Roles Distribution")
#         charts["user_roles"] = plot_to_base64(fig)

#     # Add more as needed...

#     return render(request, "analytics/admin_analytics.html", {"charts": charts})

# def plot_to_base64(fig):
#     """Helper function: convert matplotlib fig to base64 image."""
#     buf = BytesIO()
#     fig.savefig(buf, format="png", bbox_inches="tight")
#     plt.close(fig)
#     buf.seek(0)
#     image_base64 = base64.b64encode(buf.read()).decode("utf-8")
#     return f"data:image/png;base64,{image_base64}"




import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from news.models import Article, Comment, Reaction
from accounts.models import User

def plot_to_base64(fig):
    """Convert matplotlib figure to base64 string for HTML display."""
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"

def admin_analytics(request):
    """Admin analytics view (Pandas + Matplotlib-based)."""

    # 1️⃣ Fetch data
    articles = Article.objects.values("id", "category__name", "status", "created_at")
    users = User.objects.values("id", "role")
    reactions = Reaction.objects.values("id", "value")
    comments = Comment.objects.values("id", "article_id")

    # 2️⃣ Convert to DataFrames
    df_articles = pd.DataFrame(articles)
    df_users = pd.DataFrame(users)
    df_reactions = pd.DataFrame(reactions)
    df_comments = pd.DataFrame(comments)

    charts = {}

    # Define theme colors
    bg_color = "#111"
    fg_color = "#fff"
    accent_color = "#FF1744"

    # Chart 1: Articles per Category
    if not df_articles.empty:
        category_counts = df_articles["category__name"].value_counts()
        fig, ax = plt.subplots(facecolor=bg_color)
        category_counts.plot(kind="bar", color=accent_color, ax=ax)
        ax.set_title("Articles per Category", color=fg_color)
        ax.set_xlabel("Category", color=fg_color)
        ax.set_ylabel("Count", color=fg_color)
        ax.tick_params(axis='x', colors=fg_color)
        ax.tick_params(axis='y', colors=fg_color)
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        for spine in ax.spines.values():
            spine.set_color(accent_color)
        charts["articles_by_category"] = plot_to_base64(fig)

    # Chart 2: User Roles Distribution
    if not df_users.empty:
        role_counts = df_users["role"].value_counts()
        fig, ax = plt.subplots(facecolor=bg_color)
        role_counts.plot(kind="pie", autopct="%1.1f%%", colors=[accent_color, "#fff", "#222", "#444"], textprops={'color': fg_color}, ax=ax)
        ax.set_ylabel("")
        ax.set_title("User Role Distribution", color=fg_color)
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        charts["user_roles"] = plot_to_base64(fig)

    # Chart 3: Total Reactions
    if not df_reactions.empty:
        reaction_counts = df_reactions["value"].value_counts()
        fig, ax = plt.subplots(facecolor=bg_color)
        reaction_counts.plot(kind="bar", color=accent_color, ax=ax)
        ax.set_title("Total Reactions (Likes/Dislikes)", color=fg_color)
        ax.set_xlabel("Reaction", color=fg_color)
        ax.set_ylabel("Count", color=fg_color)
        ax.tick_params(axis='x', colors=fg_color)
        ax.tick_params(axis='y', colors=fg_color)
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        for spine in ax.spines.values():
            spine.set_color(accent_color)
        charts["reactions"] = plot_to_base64(fig)

    return render(request, "analytics/admin_analytics.html", {"charts": charts})
