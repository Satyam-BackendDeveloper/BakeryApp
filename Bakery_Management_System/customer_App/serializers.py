from rest_framework import serializers
from .models import LoginModel, Place_an_order_model
from django.contrib.auth.models import User

class LoginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginModel
        fields = ['username', 'password']

class PlaceAnOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place_an_order_model
        fields = ['Item', 'Quantity', 'user']

class SignupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SeeOrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Place_an_order_model
        fields = ['Item', 'Quantity']






