
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="post"),
    path("posts/edit/<int:id>", views.edit_post, name="edit_post"),
    path("posts/likes/edit/<int:id>", views.toggle_like, name="toggle_like"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/follow-toggle/<int:id>", views.followToggle, name="follow-toggle")
]
