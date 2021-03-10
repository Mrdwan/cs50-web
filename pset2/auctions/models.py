from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Categories'

class Listing(models.Model):
    title = models.CharField(max_length=190)
    description = models.TextField()
    starting_bid = models.IntegerField(default=0)
    closing_bid = models.IntegerField(default=0)
    image_url = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_id')
    closed = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, related_name='watchlist')
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name='listings')

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    winner = models.BooleanField(default=False)
    bid = models.IntegerField()

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()