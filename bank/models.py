from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import A_User_Manager
from .functions import get_currency_choices

class A_User(AbstractBaseUser, PermissionsMixin):
    username = None
    name = models.CharField(max_length=20, null=False, blank=False)
    surname = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone_number = models.CharField(max_length=12, null=False, blank=False, unique=True)
    IIN = models.CharField(max_length=12, null=False, blank=False, unique=True)
    bonus = models.PositiveIntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = A_User_Manager()

class Card(models.Model):
    number = models.CharField(max_length=19, null=False, blank=False, unique=True)
    expired = models.DateField(null=False, blank=False)
    owner = models.OneToOneField("A_User", on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=3, choices=get_currency_choices())
    cvv = models.CharField(max_length=3, null=False, blank=False)






