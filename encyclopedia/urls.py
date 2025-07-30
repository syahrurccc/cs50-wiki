from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random", views.random_page, name="random"),
    path("new", views.new_page, name="new_page"),
    path("<str:title>", views.entry_page, name="entry_page"),
    path("<str:title>/edit", views.edit_page, name="edit_page"),
]
