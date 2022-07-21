from django.db import models
from django import forms
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .utils import *

class LoginModel(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Place_an_order_model(models.Model):
    Item = models.CharField(max_length=10 )
    Quantity = models.IntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.Item}, {self.Quantity}"




