from asyncio.windows_events import NULL
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH, CharField


CATEOGRY_CHOICES = [
    ('picup', 'Picup'),
    ('sportCoupe', 'Sport Coupe'),
    ('crossover', 'Crossover'),
    ('van', 'Van'),
    ('compact', 'Compact'),
    ('hatchback', 'Hatchback'),
    ('not listed', 'Not Listed')
]

class User(AbstractUser):
    pass
    userWatchlist = models.ManyToManyField('Listings',related_name="watchlists",default=None)

class Category(models.Model):
    name = models.CharField(max_length=50)

class Listings(models.Model):
    title = models.CharField(max_length=30)
    picture = models.ImageField(blank=True,null=True, upload_to='images/') #optinal
    price = models.PositiveIntegerField("Starting bid") 
    description = models.TextField("Brief desription",max_length=500)
    category = models.CharField(max_length=30, blank=True, choices=CATEOGRY_CHOICES, default="Not listed") #optinal
    active = models.BooleanField(default=True)
    buyer = models.ForeignKey(User,on_delete=models.CASCADE, related_name="Auction_Winner", blank=True, null=True, default= None)
    auctioneer = models.ForeignKey(User,on_delete=models.CASCADE, related_name="Auctioneer")

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    price = models.IntegerField("New bid", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="Auctioneer_bid", null=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="Lot")

    def __str__(self):
        return 'new bid by: ' + str(self.price) + ' SAR on ' + '"' + self.listing.title + '"'

class Comment(models.Model):
    comment = models.CharField(max_length=350)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)


class Watchlist(models.Model):
    listing = models.ForeignKey(Listings,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} added {self.listing} to watchlist"


