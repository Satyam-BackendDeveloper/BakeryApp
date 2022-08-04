from .models import Bakery_Item, IngredientsRequiredForItem, IngredientsInStock
from django.forms import ModelForm, HiddenInput

class BakeryItemForm(ModelForm):
    selling_price = 0
    class Meta:
        model = Bakery_Item
        fields = ['title', 'quantity', 'profit']

class IngredientsForm(ModelForm):
    class Meta:
         model = IngredientsRequiredForItem
         fields = ['ingredients', 'quantity', 'bakery_item']


class IngredientsInStockForm(ModelForm):
    class Meta:
         model = IngredientsInStock
         fields = ['ingredients', 'quantity', 'cost_price']