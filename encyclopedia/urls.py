from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_page, name="entry_page"),
    path("search", views.search, name="search"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("random_page", views.random_page, name="random_page"),
    path("wiki/<str:entry>/edit", views.edit_page, name="edit_page"),
]
