from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name='search'),
    path("random", views.random_page, name='random'),
    path("<str:title>", views.entry_page, name='entry_page'),
]
