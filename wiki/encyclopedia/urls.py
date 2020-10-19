from django.urls import path, re_path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("search/", views.search, name="search"),
    path("random/", views.random, name="random"),
    path("<str:title>/", views.entry, name="entry"),
    path("<str:title>/edit/", views.edit, name="edit"),
]
