from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("random", views.randomEntry, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit")
]
