from django.contrib import admin
from .models import *

admin.site.register([
    A_User,
    Card,
])

