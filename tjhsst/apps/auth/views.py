from django.shortcuts import render
from django.contrib.auth.views import LogoutView

# Create your views here.

def login(request):
    return render(request, "auth/login.html")

logout = LogoutView.as_view()

