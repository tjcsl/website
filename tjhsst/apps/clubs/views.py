import random

from django.shortcuts import render, get_object_or_404

from .models import Club, Keyword, Category

# Create your views here.

def index(request):
    # Order the clubs randomly, but store the seed in a session variable so the
    # order won't change if the user reloads the page.
    if "seed" not in request.session:
        request.session["seed"] = random.randint(0, 10000)
    rand_gen = random.Random(request.session["seed"])

    clubs = Club.objects.all()
    clubs = sorted(clubs, key = lambda c: rand_gen.random())

    return render(request, "clubs/index.html", context = {"clubs": clubs})

def show(request, club_url):
    club = get_object_or_404(Club, url = club_url)
    return render(request, "clubs/show.html", context = {"club": club})

def show_category(request, category_url):
    category = get_object_or_404(Category, url = category_url)
    return render(request, "clubs/categories/show.html", context = {"category": category})

def show_keyword(request, keyword_url):
    keyword = get_object_or_404(Keyword, url = keyword_url)
    return render(request, "clubs/keywords/show.html", context = {"keyword": keyword})
