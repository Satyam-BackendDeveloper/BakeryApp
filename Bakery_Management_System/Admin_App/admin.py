from django.contrib import admin

# Register your models here.
from .models import Ingredients, Bakery_Item, IngredientsInStock
from customer_App.models import Place_an_order_model


admin.site.register(Ingredients)
admin.site.register(Bakery_Item)
admin.site.register(Place_an_order_model)
admin.site.register(IngredientsInStock)

