from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import *


def index(request):
    listings = Listings.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def creat_listings(request):
    if request.method == "POST":
        form = ListingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.auctioneer = request.user
            f = form.save()
            return HttpResponseRedirect(reverse("listing_details", args=[f.id]))
        else:
            return render(request, "auctions/listings.html", {
                "form": ListingsForm(request.POST)
            })
    else:
        return render(request, "auctions/listings.html", {
            "form": ListingsForm()
        })

@login_required
def listing_details(request, id):
    listing = Listings.objects.get(pk=id)
    user = request.user
    bidsNum = Bid.objects.filter(listing = listing ).count()
    return render(request, "auctions/listingDetails.html", {
        "listing": listing,
        "userWatchlist": Watchlist.objects.filter(listing=listing,user=user),
        "bids" : Bid.objects.filter(listing = listing)[0:5],
        "user" : user,
        "comment" : Comment.objects.filter(listing = listing),
        "bidsNum" : bidsNum,

    })


@login_required
def add_watchlist(request, id):
    listing = Listings.objects.get(id=id)
    user = request.user
    watchlist = Watchlist(listing=listing,user=user)
    watchlist.save()
    return HttpResponseRedirect(reverse('listing_details', args=[id]))


@login_required
def delete_watchlist(request, id):
    listing = Listings.objects.get(id=id)
    user = request.user
    Watchlist.objects.filter(listing=listing,user=user).delete()
    return HttpResponseRedirect(reverse('listing_details', args=[id]))


@login_required
def place_bid(request, id):
    listing = Listings.objects.get(pk=id)
    user = request.user
    # find or create a new Bid object
    try:
        old_bid_price = Bid.objects.filter(listing = listing).order_by('id').reverse()[0:1].get().listing.price
    except Bid.DoesNotExist:
        old_bid_price = listing.price
    if request.method == "POST":
        form = BiddingForm(request.POST)
        
        if form.is_valid():
            new_bid_price = form.cleaned_data['price']
            # new bid must be greater than any other bids have been placed before
            if new_bid_price > old_bid_price:
                form.save()
                listing.price = new_bid_price
                listing.save(update_fields=['price'])
                return HttpResponseRedirect(reverse('listing_details', args=[id]))
            else:
                message = "Bid price must be greater than any other bids have been placed before"
                return render(request, "auctions/place_bid.html", {
                "form": BiddingForm(request.POST),
                "listing": listing,
                "message": message,
            })     
        else:
            return render(request, "auctions/place_bid.html", {
                "form": BiddingForm(request.POST),
                "listing": listing,
            })
    else:
        return render(request, "auctions/place_bid.html", {
            "form": BiddingForm(initial={'price': listing.price, 'user': user, 'listing': listing}),
            "listing": listing,
        })

    
def not_logged(requset):
    return HttpResponse("Must log in fist")

@login_required
def close_auction(request, id):
    user = request.user
    listing = Listings.objects.get(id=id)
    listing.active = False
    try:
        listing.buyer =  Bid.objects.filter(listing = listing).order_by('id').reverse()[0:1].get().user
    except Bid.DoesNotExist:
        listing.buyer = None
    listing.save()
    return render(request,"auctions/listingDetails.html", {
        "listing": listing,
        "userWatchlist": Watchlist.objects.filter(listing=listing,user=user),
        "bids" : Bid.objects.filter(listing = listing)[1:6],
        "user" : user,
        "comment" : Comment.objects.filter(listing = listing),
        })

@login_required
def comment(request, id):
    listing = Listings.objects.get(id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.listing=listing
            form.save()
            return HttpResponseRedirect(reverse('listing_details', args=[id]))
        else:
            return render(request, "auctions/comment.html", {
                "form": CommentForm(request.POST),
                "listing": listing,
            })
    else:
        return render(request, "auctions/comment.html", {
            "form": CommentForm(),
            "listing": listing,
        })

@login_required
def watchlist(request):
    user = request.user
    userWatchlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
            "user": user,
            "userWatchlist": userWatchlist,
            "watchlistNum": userWatchlist.count(),
        })

def all_categories(request):
    categories = dict(CATEOGRY_CHOICES) #transform tuples into dictionary
    categories = categories.values() # access second value of tuple
    return render(request, "auctions/all_categories.html", {
            "categories" : categories
        })

def specific_category(request,category):
    listings = Listings.objects.filter(category=category.lower()) #return all listing with the wanted category
    return render(request, "auctions/specific_category.html", {
            "listings" : listings,
            "category" : category,
            "notListed" : Listings.objects.filter(category=None),
        })

def all_listings(request):
    listings = Listings.objects.all()
    return render(request, "auctions/all_listings.html", {
        "listings": listings,
    })
