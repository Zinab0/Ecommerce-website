from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings", views.creat_listings, name="listings"),
    path("listingDetails/<int:id>", views.listing_details, name="listing_details"),
    path("delete_list/<int:id>", views.delete_watchlist, name="delete_watchlist"),
    path("add_list/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("place_bid/<int:id>", views.place_bid, name="place_bid"),
    path("accounts/login/", views.not_logged, name="not_logged"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("all_categories", views.all_categories, name="all_categories"),
    path("all_categories/<str:category>", views.specific_category, name="specific_category"),
    path("all_listings", views.all_listings, name="all_listings"),

]