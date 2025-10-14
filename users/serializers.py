from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, CustomUser


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CustomUserSerializer(ModelSerializer):

    class Meta:
        model =CustomUser
        fields = "__all__"
