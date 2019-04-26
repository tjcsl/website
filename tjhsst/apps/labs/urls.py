from django.urls import path

from . import views

app_name = "labs"

urlpatterns = [
    path("", views.index, name = "index"),
    path("<str:lab_url>", views.show, name = "show"),
    path("course/<str:course_url>", views.show_course, name="show_course"),
]

