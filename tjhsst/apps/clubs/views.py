import random

from django import http
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Club, Keyword, Category
from .forms import ClubForm, ClubCreationForm

# Create your views here.

def index(request):
    clubs = Club.objects.all()

    if request.GET.get("q"):
        query = request.GET["q"]
        words = query.split()

        club_scores = {club: 0 for club in clubs}
        for word in words:
            for club in clubs.filter(name__icontains = word):
                club_scores[club] += 4

            for club in clubs.filter(category__name__icontains = word):
                club_scores[club] += 3

            for club in clubs.filter(keywords__name__icontains = word):
                club_scores[club] += 2

            for club in clubs.filter(description__icontains = word):
                club_scores[club] += 1

        clubs = sorted((club for club in clubs if club_scores[club] > 0), reverse = True, key = club_scores.__getitem__)
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
            "can_edit": request.user.is_superuser or request.user in club.admins.all(),
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
        },
    )

def edit(request, club_url):
    club = get_object_or_404(Club, url = club_url)
    if request.user.is_authenticated and (request.user.is_superuser or request.user in club.admins.all()):
        if request.method == "POST":
            form = ClubForm(request.POST, request.FILES, instance = club)
            if form.is_valid():
                form.save()
                return redirect("clubs:edit", club.url)
        else:
            form = ClubForm(instance = club)

        return render(
            request,
            "clubs/edit.html",
            {
                "club": club,
                "club_form": form,
            },
        )
    else:
        raise http.Http404

def new(request):
    if request.user.is_authenticated and (request.user.is_teacher or request.user.is_superuser):
        if request.method == "POST":
            form = ClubCreationForm(request.POST)
            if form.is_valid():
                club = form.save()
                return redirect("clubs:show", club.url)
        else:
            form = ClubCreationForm()

        return render(
            request,
            "clubs/new.html",
            {
                "club_form": form,
            },
        )
    else:
        raise http.Http404

