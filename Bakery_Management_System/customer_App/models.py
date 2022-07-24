from django.db import models
from django import forms
from datetime import datetime
from django.contrib.auth.models import User
from Admin_App.models import Bakery_Item
from django.contrib.auth import get_user_model
from .utils import *

class LoginModel(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Place_an_order_model(models.Model):

    Item = models.ForeignKey(Bakery_Item, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Item}, {self.Quantity}, {self.user}"




