from django.urls import path
from .views import *

urlpatterns = [
    path("auth", AuthApiView.as_view(), name="auth"),
    path("user_profile", UserApiView.as_view(), name="user_profile"),
    path("registration", UserApiView.as_view(), name="registration"),
]