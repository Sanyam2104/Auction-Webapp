from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuctionListings , Comments, Bids, Watchlist

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(AuctionListings)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Watchlist)

