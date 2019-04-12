from django.urls import path

from . import views

app_name = "labs"

urlpatterns = [
    path("", views.index, name = "index"),
    path("<str:lab_url>", views.show, name = "show"),
    path("prerequisite/<str:prerequisite_url>", views.show_prerequisite, name="show_prerequisite"),
    path("recomended/<str:recommended_url>", views.show_recommended, name="show_recommended"),
]

