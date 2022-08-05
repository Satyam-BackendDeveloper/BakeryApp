from rest_framework import serializers
from .models import Bakery_Item, IngredientsRequiredForItem, IngredientsInStock

class AddIngredientsToStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsInStock
        fields = ['ingredients', 'quantity', 'cost_price']

class BakeryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bakery_Item
        fields = '__all__'

class IngredientsRequiredForItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsRequiredForItem
        fields = ['ingredients', 'quantity', 'bakery_item']





