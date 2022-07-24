"""Bakery_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Admin_App.views import welcome, display_all_items, inventory, admin_Page,addItem,addIngredientsToStock, itemsRequiredForBakeryItem
from customer_App.views import signup, index, thanks, dashboard, loginViewFunction, view_all_items_function, Cart, get_bill, see_order_history, sellingPrice, payment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('all_items', display_all_items),
    path('inventory', inventory),
    path('index', index ),
    path('signup', signup),
    path('thanks', thanks),
    path('dashboard', dashboard),
    path('login', loginViewFunction),
    path('view_all_items', view_all_items_function),
    path('place_an_order', Cart),
    path('get_bill', get_bill),
    path('see_order_history', see_order_history),

    path('addItem', addItem),
    # path('addIngredients', addIngredientsToBakeryItems),
    path('addIngredients', itemsRequiredForBakeryItem),
    path('addIngredientsInStock', addIngredientsToStock),
    path('satyam', sellingPrice),

    path('payment', payment),
]
