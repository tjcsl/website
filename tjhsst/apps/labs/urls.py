from django.urls import path

from . import views

app_name = "labs"

urlpatterns = [
    path("", views.index, name="index"),
    path("find", views.show_courses, name="find_by_courses"),
    path("new", views.new, name="new"),
    path("<str:lab_url>", views.show, name="show"),
    path("<str:lab_url>/edit", views.edit, name="edit"),
    path("course/<str:course_url>", views.show_course, name="show_course"),
    path("<str:lab_url>/projects", views.show_projects, name="show_projects"),
    path("projects/new", views.add_project, name="add_project"),
    path("testimonials/new", views.add_testimonal, name="add_testimonial"),
]
