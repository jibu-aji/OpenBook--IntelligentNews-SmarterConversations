import requests
from django.conf import settings
from django.shortcuts import render

def n_api_latest_news(request):
    api_key = settings.NEWSDATA_API_KEY
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=in&language=en"

    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("results", [])
    except Exception as e:
        articles = []
        print("Error fetching API data:", e)

    return render(request, "n_api/n_api_latest_news.html", {"articles": articles})

api_key = settings.NEWSDATA_API_KEY # replace with your actual API key




def n_api_live_news(request):
    # Check if we have a next page token
    next_page_token = request.GET.get("page")

    url = f"https://newsdata.io/api/1/latest?apikey={api_key}&language=en"
    if next_page_token:
        url += f"&page={next_page_token}"

    response = requests.get(url)
    data = response.json()

    articles = data.get("results", [])
    next_page = data.get("nextPage")  # will be None if no more pages

    context = {
        "articles": articles,
        "next_page": next_page
    }

    return render(request, "n_api/n_api_live_news.html", context)