from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass

#Model for adding an auction item 
class AuctionListings(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    bid = models.IntegerField()
    imageURL = models.URLField(blank=True)
    category = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    winner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True, related_name="purchased_itemw")
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

#Model for bidding on item
class Bids(models.Model):
    bid = models.IntegerField(default=0)
    lisitng = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, null=True, related_name='bids')
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    
#Model forstoring comments on item
class Comments(models.Model):
    text = models.TextField(null=True)
    time = models.DateTimeField(default=timezone.now)
    lisitng = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, null=True, related_name='comments')
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name='comments')

    def __str__(self):
        return "{self.text} by {self.commented_by}"
    
#Model for adding an item to user watchlist
class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)