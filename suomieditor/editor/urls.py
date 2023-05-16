from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # with id (pk)
    path("<int:baseform_id>/", views.detail, name="detail"),
    # analyze
    path("analyze/", views.analyze, name="analyze"),
]
