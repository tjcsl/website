import random

from django.shortcuts import render, reverse, get_object_or_404

from .models import Lab, Prerequisite, Recommended

# Create your views here.

def index(request):
    labs = Lab.objects.all()

    if request.GET.get("q"):
        query = request.GET["q"]
        words = query.split()

        lab_scores = {lab: 0 for lab in labs}
        for word in words:
            for lab in labs.filter(name__contains = word):
                lab_scores[lab] += 2

            for lab in labs.filter(description__contains = word):
                lab_scores[lab] += 1

        labs = sorted((lab for lab in labs if lab_scores[lab] > 0), key = lab_scores.__getitem__)
    else:
        # Order the labs randomly, but store the seed in a session variable so the
        # order won't change if the user reloads the page.
        if "seed" not in request.session:
            request.session["seed"] = random.randint(0, 10000)
        rand_gen = random.Random(request.session["seed"])

        labs = sorted(labs, key = lambda c: rand_gen.random())

    return render(
        request,
        "labs/index.html",
        {
            "labs": labs,
            "search_term": request.GET.get("q", ""),
        },
    )

def show(request, lab_url):
    lab = get_object_or_404(Lab, url = lab_url)

    return render(
        request,
        "labs/show.html",
        {
            "lab": lab,
        },
    )

def show_prerequisite(request, prerequisite_url):
    prerequisite = get_object_or_404(Prerequisite, url = prerequisite_url)

    return render(
        request,
        "labs/prerequisites/show.html",
        {
            "prerequisite": prerequisite,
            "labs": prerequisite.labs.all(),
        },
    )

def show_recommended(request, recommended_url):
    recommended = get_object_or_404(Recommended, url = recommended_url)

    return render(
        request,
        "labs/recommendeds/show.html",
        {
            "recommended": recommended,
            "labs": recommended.labs.all(),
        },
    )

