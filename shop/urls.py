from django.urls import path
from .views import *

urlpatterns = [
    path("categories", CategoryApiView.as_view(), name="categories"),
    path("reviews", ReviewApiView.as_view(), name="reviews"),
    path("goods", GoodApiView.as_view(), name="goods"),
    path("goods_detail/<int:pk>", GoodDetailApiView.as_view(), name="goods_detail"),
    path("goods_by_category/<int:pk>", GoodsByCategoryApiView.as_view(), name="goods_by_category"),
    path("cart", CartApiView.as_view(), name="cart"),
    path("purchase", OrderApiView.as_view(), name="purchase"),
    path("cart_increase/<int:index>", CartIncreaseApiView.as_view(), name="cart_increase"),
    path("cart_decrease/<int:index>", CartDecreaseApiView.as_view(), name="cart_decrease"),
]
