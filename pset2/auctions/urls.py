from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/create", views.listings_create, name="listings.create"),
    path("listings/<int:id>", views.listings_show, name="listings.show"),
    path("listings/<int:id>/bid", views.listings_bid, name="listings.bid"),
    path("listings/<int:id>/close", views.listings_close, name="listings.close"),
    path("listings/<int:id>/watchlist", views.listings_watchlist, name="listings.watchlist"),
    path("listings/<int:id>/comment", views.listings_comment, name="listings.comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
