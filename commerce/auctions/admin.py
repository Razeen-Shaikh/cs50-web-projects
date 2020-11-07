from django.contrib import admin
from .models import User, Auction, Bid, Comment, WatchList
from auctions.models import Winner

# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Winner)
