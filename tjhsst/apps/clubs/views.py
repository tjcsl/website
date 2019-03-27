from django.shortcuts import render, get_object_or_404

from .models import Club, Keyword, Category

# Create your views here.

def show(request, club_url):
    club = get_object_or_404(Club, url = club_url)
    return render(request, "clubs/show.html", context = {"club": club})

