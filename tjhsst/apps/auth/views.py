from django.contrib.auth.views import LogoutView
from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request, "auth/login.html")


logout = LogoutView.as_view()
