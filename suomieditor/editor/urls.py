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
    path("rss/", views.LatestEntriesFeed(), name="rss"),
    path("recent_as_file/", views.recent_as_file, name="recent_as_file"),
    path("raw_analyze/", views.raw_analyze, name="raw_analyze"),
    path("types/", views.by_type_list, name="by_type_list"),
    path(
        "types/<int:declension_id>/<str:gradation_id>",
        views.by_type_word_list,
        name="by_type_word_list",
    ),
]
