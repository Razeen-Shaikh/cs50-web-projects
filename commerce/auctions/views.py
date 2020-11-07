from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Auction, Comment, WatchList
from .forms import AuctionForm, BidForm, CommentForm
import datetime
from auctions.models import Bid, Winner
from django.db.models.aggregates import Max


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions,
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
            return redirect("commerce:index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("commerce:index")


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
        return redirect("commerce:index")
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        auction = Auction.objects.filter(title=request.POST['title'])
        if not auction:
            form = AuctionForm(request.POST, request.FILES)
            if form.is_valid:
                auction = form.save(commit=False)
                auction.owner = request.user.username
                auction.created_at = datetime.date.today()
                auction.save()
                return redirect("commerce:auction", title=auction.title)
        else:
            form = AuctionForm()
            message = "Auction title already exists"
            return render(request, "auctions/create.html", {
                "form": form,
                "message": message,
            })
    form = AuctionForm()
    return render(request, "auctions/create.html", {
        "form": form,
    })


@login_required
def watch(request, id):
    if WatchList.objects.filter(auction_id=id, user=request.user.username).exists():
        watchlist = WatchList.objects.get(
            auction_id=id, user=request.user.username)
        watchlist.delete()
    w = WatchList(auction_id=id, user=request.user.username)
    w.save()
    auction = Auction.objects.get(a_id=id)
    auction.watch = not auction.watch
    auction.save()
    return redirect("commerce:auction", auction.title)


@login_required
def watchlist(request):
    watch = WatchList.objects.filter(user=request.user.username)
    auctions = Auction.objects.none()
    for w in watch:
        auctions |= (Auction.objects.filter(a_id=w.auction_id, watch=True))
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "isWatchlist": True,
    })


@login_required
def categories(request):
    return render(request, "auctions/categories.html")


@login_required
def category(request, category):
    auctions = Auction.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "auctions": auctions,
    })


def auction(request, title):
    auction = Auction.objects.get(title=title)
    bids = Bid.objects.filter(auction_id=auction.a_id)
    comments = Comment.objects.filter(auction_id=auction.a_id)
    comment_form = CommentForm()
    bid_form = BidForm()
    isOwner = False
    if auction.owner == request.user.username:
        isOwner = True
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "isOwner": isOwner,
        "bid_form": bid_form,
        "bids": bids,
        "comment_form": comment_form,
        "comments": comments,
    })


@login_required
def bid(request, title):
    auction = Auction.objects.get(title=title)
    bid_form = BidForm()
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if bid_form.is_valid:
            bid_amount = float(request.POST['bid_amount'])
            if auction.starting_bid < bid_amount:
                bid = bid_form.save(commit=False)
                bid.user = request.user.username
                bid.auction_id = auction.a_id
                auction.starting_bid = bid_amount
                auction.save()
                bid.save()
                bid_form = BidForm()
    return redirect("commerce:auction", title=title)


@login_required
def comment(request, title):
    auction = Auction.objects.get(title=title)
    comment_form = CommentForm()
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            comment.user = request.user.username
            comment.auction_id = auction.a_id
            comment.a_id = auction
            comment.save()
            comment_form = CommentForm()
    return redirect("commerce:auction", title)


@login_required
def winner(request):
    winnings = Winner.objects.filter(new_owner=request.user.username)
    return render(request, "auctions/winner.html", {
        "winnings": winnings,
    })


@login_required
def delete(request, id):
    auction = Auction.objects.get(a_id=id)
    bids = Bid.objects.filter(auction_id=id)
    if bids:
        max_bid = Bid.objects.filter(
            auction_id=id
        ).aggregate(maxbid=Max('bid_amount'))['maxbid']
        bid = Bid.objects.get(auction_id=id, bid_amount=max_bid)
        winner = Winner()
        winner.new_owner = bid.user
        winner.title = auction.title
        winner.price = bid.bid_amount
        if auction.image:
            winner.image = auction.image
        else:
            winner.image = auction.image_url
        winner.save(force_insert=True)
    auction.delete()
    return redirect("commerce:index")
