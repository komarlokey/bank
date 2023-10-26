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


