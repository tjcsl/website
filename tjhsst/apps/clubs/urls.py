from django.urls import path

from . import views

app_name = "clubs"

urlpatterns = [
    path("<str:club_url>", views.show, name = "show"),
    path("category/<str:category_url>", views.show_category, name="show_category"),
    path("keyword/<str:keyword_url>", views.show_keyword, name="show_keyword"),
]

