from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page/<str:entry_name>", views.edit_page, name="edit_page"),
    path("random", views.random, name="random"),
    path("<str:entry_name>", views.entry, name="entry")
]
