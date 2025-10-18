from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, CustomUser, Subscription


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CustomUserSerializer(ModelSerializer):

    class Meta:
        model =CustomUser
        fields = "__all__"

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'