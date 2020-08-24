from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, AuctionListings, Comments, Bids, Watchlist


def index(request):
    return render(request, "auctions/index.html",{
        "listings": AuctionListings.objects.all()
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

            #If user is redirected to login page from a different page
            #after logging in user will be redirected to the page user was on before.

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
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


#Page for listing a new auction 
@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        
        #collecting data
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["bid"]
        imageURL = request.POST["imageURL"]
        category = request.POST["category"]

        #Creating model instance from collected data
        listing = AuctionListings.objects.create(title=title, description=description, bid=starting_bid, imageURL=imageURL, category=category, author=request.user)
        listing.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/createlisting.html")


#Display a detailed page about the Listing
def listing(request, listing_id):
    item = AuctionListings.objects.get(pk=listing_id)
    message = ""
    bid_list = item.bids.all()
    highest = 0
    for i in bid_list:
        if i.bid > highest:
            highest = i.bid
            highest_bid_by = i.bid_by

    if request.method == 'POST':

        #Form logic for placing a bid

        if request.POST.get("form_name") == "formOne":
            your_bid = int(request.POST['your_bid'])

            if your_bid > item.bid and your_bid > highest:
                obj = Bids.objects.create(bid=your_bid, lisitng=item, bid_by=request.user)
                obj.save()
                highest = your_bid
                messages.success(request, 'Bid Placed.')
                return render(request, "auctions/listing.html", {
                    "listing": item,
                    "highestBid": highest,
                    "comments": Comments.objects.all().filter(lisitng=listing_id)
                })
            else:
                messages.warning(request, 'Bid must be higher than the current bid placed.')
                return render(request, "auctions/listing.html", {
                    "listing": item,
                    "highestBid": highest,
                    "comments": Comments.objects.all().filter(lisitng=listing_id)
                })

        #Form for closing the bid 

        if request.POST.get("form_name") == "formTwo":
            item.active = False
            item.winner = highest_bid_by
            item.save()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))

        #Form for collecting comments on the listing

        if request.POST.get("form_name") == 'formThree':
            content = str(request.POST['comment'])
            if len(content) > 0:
                comment = Comments.objects.create(text=content, commented_by=request.user, lisitng=item)
                comment.save()
                return HttpResponseRedirect(reverse('listing', args=(listing_id,)))

        #Form for adding items to Watchlist

        if request.POST.get("form_name") == 'formFour':

            #if item already in watchlist then remove it else add it.
            
            if Watchlist.objects.filter(user_id=request.user, auction_id=item):
                Watchlist.objects.filter(user_id=request.user, auction_id=item).delete()
            else:
                obj = Watchlist.objects.create(user_id=request.user, auction_id=item)
                obj.save()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        
    return render(request, "auctions/listing.html", {
        "listing": item,
        "highestBid": highest,
        "comments": Comments.objects.all().filter(lisitng=listing_id)
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Watchlist.objects.all().filter(user_id=request.user)
    })



#Displays the list of categories available
def categories(request):      
    return render(request, 'auctions/categories.html',{
        "listings": None,
        "item": ['Fashion', 'Toy','Electronics' ,'Decoration' , 'Others']
    })

#Shows the listing to a specific category
def displaycateg(request, category):
    return render(request, 'auctions/categories.html',{
        "listings":  AuctionListings.objects.all().filter(category=category),
    })

