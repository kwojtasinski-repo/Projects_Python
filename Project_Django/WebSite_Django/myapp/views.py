from django.shortcuts import redirect, render
from .decorators import post_only_redirect_home
from . import models
from .scraper import fetch_posts

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')

@post_only_redirect_home
def new_search(request):
    search = request.POST.get("search", "").strip()

    if not search:
        return redirect("/")

    models.Search.objects.create(search=search)

    final_postings = fetch_posts(search)

    return render(
        request,
        "myapp/new_search.html",
        {
            "search": search,
            "final_postings": final_postings,
        },
    )

def not_found(request, exception):
    print("404 error handler called")
    return render(request, "not_found.html", status=404)
