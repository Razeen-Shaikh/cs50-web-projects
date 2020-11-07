from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

CATEGORIES = [
    ('FA', 'Fashion'),
    ('TY', 'Toys'),
    ('EC', 'Electronics'),
    ('HM', 'Home'),
    ('OT', 'Others'),
]


class User(AbstractUser):
    pass


class Auction(models.Model):
    a_id = models.IntegerField(primary_key=True)
    owner = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10000)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateField()
    category = models.CharField(
        max_length=50, choices=CATEGORIES, default="OT")
    watch = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    a_id = models.ForeignKey(
        "Auction", on_delete=models.CASCADE, null=True, blank=True)
    auction_id = models.IntegerField(default=False)
    user = models.CharField(max_length=150)
    bid_amount = models.FloatField()

    def __str__(self):
        return self.user


class Comment(models.Model):
    a_id = models.OneToOneField("Auction", on_delete=models.CASCADE)
    auction_id = models.IntegerField(default=False)
    user = models.CharField(max_length=150)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.user


class WatchList(models.Model):
    a_id = models.ForeignKey(
        "Auction", on_delete=models.CASCADE, null=True, blank=True)
    auction_id = models.IntegerField(default=False)
    user = models.CharField(max_length=150)

    def __str__(self):
        return self.user


class Winner(models.Model):
    new_owner = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', default=False)

    def __str__(self):
        return self.new_owner
