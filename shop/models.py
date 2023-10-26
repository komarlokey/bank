from django.db import models
from .functions import get_rating_choices


class Category(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)


class Review(models.Model):
    rating = models.CharField(max_length=5, choices=get_rating_choices())
    text = models.TextField(null=True, blank=True)
    author = models.ForeignKey("bank.A_User", on_delete=models.CASCADE)


class Good(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    reviews = models.ManyToManyField("Review", blank=True)


class Favourite(models.Model):
    buyer = models.OneToOneField("bank.A_User", on_delete=models.CASCADE)
    goods = models.ManyToManyField("Good", blank=True)

