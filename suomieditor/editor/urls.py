from django.urls import path

from . import views

app_name = "editor"

urlpatterns = [
    path("", views.index, name="index"),
    # with id (pk)
    path("word/<int:baseform_id>/", views.detail, name="detail"),
    # analyze
    path("analyze/", views.analyze, name="analyze"),
    path("add_cases/", views.add_cases, name="add_cases"),
    path("recent/", views.recent, name="recent"),
    path("search/", views.search, name="search"),
    path("raw/", views.raw, name="raw"),
    path("raw_analyze/", views.raw_analyze, name="raw_analyze"),
]
