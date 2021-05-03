from django.urls import path

from . import views

app_name = "clubs"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("new", views.new, name="new"),
    path("category/<str:category_url>", views.show_category, name="show_category"),
    path("keyword/<str:keyword_url>", views.show_keyword, name="show_keyword"),
    path("<str:club_url>", views.show, name="show"),
    path("<str:club_url>/edit", views.edit, name="edit"),
    path("<str:club_url>/follow", views.follow, name="follow"),
    path("<str:club_url>/post", views.post, name="post"),
]
