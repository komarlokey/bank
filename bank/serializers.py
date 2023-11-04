from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = A_User
        fields = ["name", "surname", "email", "phone_number", "IIN", "bonus"]

    # def to_representation(self, instance):
        # representation = dict()
        # representation["name"] = instance.name
        # representation["surname"] = instance.surname
        # representation["email"] = instance.email
        # representation["phone_number"] = instance.phone_number
        # return representation


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["owner"] = UserSerializer(instance.owner).data
        representation["number"] = (representation["number"][0:4] + " " + representation["number"][4:8] + " "
                                    + representation["number"][8:12] + " " + representation["number"][12:16])
        return representation
