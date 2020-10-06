from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("random_page", views.random_page, name="random_page"),
    path("search", views.search, name="search"),
    path("error", views.error, name="error"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("search_results/<query>", views.results, name="results")
]
