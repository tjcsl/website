import random

from django.shortcuts import render, reverse, get_object_or_404

from .models import Club, Keyword, Category

# Create your views here.

def index(request):
    clubs = Club.objects.all()

    if request.GET.get("q"):
        query = request.GET["q"]
        words = query.split()

        club_scores = {club: 0 for club in clubs}
        for word in words:
            for club in clubs.filter(name__contains = word):
                club_scores[club] += 2

            for club in clubs.filter(description__contains = word):
                club_scores[club] += 1

        clubs = sorted((club for club in clubs if club_scores[club] > 0), key = club_scores.__getitem__)
    else:
        # Order the clubs randomly, but store the seed in a session variable so the
        # order won't change if the user reloads the page.
        if "seed" not in request.session:
            request.session["seed"] = random.randint(0, 10000)
        rand_gen = random.Random(request.session["seed"])

        clubs = sorted(clubs, key = lambda c: rand_gen.random())

    return render(
        request,
        "clubs/index.html",
        {
            "clubs": clubs,
            "search_url": reverse("clubs:index"),
            "search_name": "clubs",
            "search_term": request.GET.get("q", ""),
        },
    )

def show(request, club_url):
    club = get_object_or_404(Club, url = club_url)

    return render(
        request,
        "clubs/show.html",
        {
            "club": club,
            "search_url": reverse("clubs:index"),
            "search_name": "clubs",
        },
    )

def show_category(request, category_url):
    category = get_object_or_404(Category, url = category_url)

    return render(
        request,
        "clubs/categories/show.html",
        {
            "category": category,
            "clubs": category.clubs.all(),
            "search_url": reverse("clubs:index"),
            "search_name": "clubs",
        },
    )

def show_keyword(request, keyword_url):
    keyword = get_object_or_404(Keyword, url = keyword_url)

    return render(
        request,
        "clubs/keywords/show.html",
        {
            "keyword": keyword,
            "clubs": keyword.clubs.all(),
            "search_url": reverse("clubs:index"),
            "search_name": "clubs",
        },
    )

