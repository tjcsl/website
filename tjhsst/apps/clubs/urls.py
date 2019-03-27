from django.urls import path

from . import views

app_name = "clubs"

urlpatterns = [
    path("<str:club_url>", views.show, name = "show"),
]

