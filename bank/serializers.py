from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = A_User
        fields = ["name", "surname", "email", "phone_number", "IIN"]

    def to_representation(self, instance):
        representation = dict()
        representation["name"] = instance.name
        representation["surname"] = instance.surname
        representation["email"] = instance.email
        representation["phone_number"] = instance.phone_number
        return representation