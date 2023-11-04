from rest_framework.serializers import ModelSerializer
from .models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = instance.author.email
        return representation


class GoodsSerializer(ModelSerializer):
    class Meta:
        model = Good
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("description")
    #     representation.pop("reviews")
    #     return representation

    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["name"] = instance.name
        representation["price"] = instance.price
        representation["category"] = instance.category.name
        return representation


class GoodDetailSerializer(ModelSerializer):
    class Meta:
        model = Good
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["goods"] = OrderGoodsSerializer(instance.goods.all(), many=True).data
        return representation


class OrderGoodsSerializer(ModelSerializer):
    class Meta:
        model = OrderGoods
        fields = ["good", "count"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["good"] = GoodsSerializer(instance.good).data
        representation["sum"] = instance.count * instance.good.price
        return representation
