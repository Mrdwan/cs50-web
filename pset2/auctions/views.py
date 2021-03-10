from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def listings_create(request):
    if request.method == "POST":
        Listing.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            starting_bid=request.POST['starting_bid'], 
            image_url=request.POST['image_url'],
            category=Category.objects.get(pk=request.POST['category']),
            owner=request.user
        )

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "listings/create.html", {
            "categories": Category.objects.all()
        })

def listings_show(request, id):
    product = Listing.objects.get(pk=id)

    return render(request, "listings/show.html", {
        "listing": product,
        "watchListed": product.watchlist.filter().exists() if request.user.is_authenticated else False,
        "winner": Bid.objects.get(listing=product.id, winner=True) if product.closed == True else None,
        "comments": Comment.objects.filter(listing=product)
    })

@login_required
def listings_watchlist(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)

        if request.POST['type'] == 'add':
            listing.watchlist.set([request.user.id])
        else:
            listing.watchlist.remove(request.user)

        return HttpResponseRedirect(reverse("listings.show", args=[id]))

@login_required
def listings_bid(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        bid = int(request.POST['bid'])
        maxBid = Bid.objects.filter(listing=id).aggregate(Max('bid'))['bid__max']
        
        if bid <= listing.starting_bid or (Bid.objects.filter(listing=id).count() > 0 and bid <= maxBid):
            messages.error(request, f"Bid needs to be higher than the Starting bid, and other bids, highest now is {maxBid}")
        else:
            Bid.objects.create(bidder=request.user, listing=listing, bid=bid)
            messages.success(request, 'Bidded Successfully!')

    return HttpResponseRedirect(reverse("listings.show", args=[id]))

@login_required
def listings_close(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)

        if (Bid.objects.filter(listing=id).count() == 0):
            messages.error(request, 'There is no Bidding!')
            return HttpResponseRedirect(reverse("listings.show", args=[id]))

        maxBid = Bid.objects.filter(listing=id).aggregate(Max('bid'))['bid__max']
        winnerBid = Bid.objects.get(listing=id, bid=maxBid)

        listing.closed = True
        listing.closing_bid = maxBid
        listing.active = False
        listing.save()

        winnerBid.winner = True
        winnerBid.save()

    messages.success(request, 'Bidding Closed!')
    return HttpResponseRedirect(reverse("listings.show", args=[id]))

@login_required
def listings_comment(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)

    Comment.objects.create(
        owner=request.user,
        listing=listing,
        comment=request.POST['comment']
    )

    messages.success(request, 'Comment added!')
    return HttpResponseRedirect(reverse("listings.show", args=[id]))

@login_required
def watchlist(request):
    return render(request, "watchlist/index.html", {
        'watchlist': request.user.watchlist.all()
    })

def categories(request):
    return render(request, "categories/index.html", {
        'categories': Category.objects.all()
    })

def category(request, id):
    category = Category.objects.get(pk=id)
    return render(request, "categories/show.html", {
        'category': category,
        'listings': category.listings.all()
    })