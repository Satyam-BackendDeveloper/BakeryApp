from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.
""""
Bakery ADMIN should have the capability to:

Add Ingredients to bakery like Milk, Eggs etc
Create BakeryItem from a list of ingredients like Cupcake, Cake, Muffin etc
Get the detail of BakeryItem (ingredients with quantity percentage, cost price, selling price etc)
Manage inventory
CUSTOMER should have the capability to:

Register and Login
Get a list of available products
Place an Order and get the bill
See order history
"""

from .models import Ingredients, Bakery_Item, IngredientsInStock
from .forms import BakeryItemForm, IngredientsForm, IngredientsInStockForm


def welcome(request):
    return render(request, 'Admin_App/index.html')

def display_all_items(request):
    bakery_item = Bakery_Item.objects.all()
    ingredients_objects = Ingredients.objects.all()

    return render(request, 'Admin_App/all_items.html', {"bakery_item" : bakery_item, "ingredients" : ingredients_objects})


def inventory(request):
    bakery_item = Bakery_Item.objects.all()

    ingredients_objects = IngredientsInStock.objects.all()
    quantity_dict = {}
    #
    # for item in ingredients_objects:
    #     if item.ingredients in quantity_dict:
    #         quantity_dict[item.ingredients] += item.quantity
    #     else:
    #         quantity_dict[item.ingredients] = item.quantity
    #
    # for item in bakery_item :
    #     for x in ingredients_objects:
    #         if item == x.bakery_item :
    #             quantity_dict[x.ingredients] -= x.quantity


    for item in ingredients_objects:
        quantity_dict[item.ingredients] = item.quantity

    return render(request, 'Admin_App/inventory.html', {"inventory" : quantity_dict})

def admin_Page(request):
    user = request.user
    if user.is_active and user.is_superuser:
        return render(request, 'index.html', {})

def addItem(request):
    items = Bakery_Item.objects.all()
    item_title = []
    for x in items:
        item_title.append(x.title)

    if(request.method == 'POST'):
        form = BakeryItemForm(request.POST)
        if form.is_valid():
            if request.POST.get('title') in item_title:
                item = Bakery_Item.objects.get(title=request.POST.get('title'))
                item.quantity = int(item.quantity) + int(request.POST.get('quantity'))
                item.save()
            else:
                form.save()
                form = BakeryItemForm()
                return render(request, 'Admin_App/addItem.html', {'form': form.as_p})
    else:
        form = BakeryItemForm()

    return render(request, 'Admin_App/addItem.html', {'form' : form.as_p})


def addIngredientsToBakeryItems(request):
    ingredientInStock = IngredientsInStock.objects.all()
    ingredientInItem = Ingredients.objects.filter(bakery_item = request.POST.get('bakery_item'))

    item_titleInStock = []
    for x in ingredientInStock:
        item_titleInStock.append(x.ingredients)

    item_titleInBakeryObjects = []

    for x in ingredientInItem:
            item_titleInBakeryObjects.append(x.ingredients)

    if(request.method == 'POST'):
        form = IngredientsForm(request.POST)
        if form.is_valid():
            if request.POST.get('ingredients') in item_titleInStock:
                if request.POST.get('ingredients') not in item_titleInBakeryObjects:
                    item = IngredientsInStock.objects.get(ingredients = request.POST.get('ingredients'))
                    item.quantity = int(item.quantity) - int(request.POST.get('quantity'))
                    if item.quantity < 0:
                        return HttpResponse("Stock Empty !! Need to add Ingredients in Stock")
                    item.save()
                    form.save()


                    if len(item_titleInBakeryObjects) == 3:
                        pass

                    form = IngredientsForm()
                    return render(request, 'Admin_App/addIngredients.html', {'form': form.as_p})

                else:
                    item = Ingredients.objects.get(ingredients=request.POST.get('ingredients'), bakery_item = request.POST.get('bakery_item'))
                    item.quantity = int(item.quantity) + int(request.POST.get('quantity'))
                    item.save()

                    item = IngredientsInStock.objects.get(ingredients=request.POST.get('ingredients'))
                    item.quantity = int(item.quantity) - int(request.POST.get('quantity'))
                    item.save()


                    return HttpResponse("Item's Quantity Updated")

            else:
                return HttpResponse("Stock Empty !! Need to add Ingredients in Stock")
    else:
        form = IngredientsForm()

    return render(request, 'Admin_App/addIngredients.html', {'form' : form.as_p})

def addIngredientsToStock(request):
    items = IngredientsInStock.objects.all()
    item_title = []
    for x in items:
        item_title.append(x.ingredients)

    if(request.method == 'POST'):
        form = IngredientsInStockForm(request.POST)
        if form.is_valid():
            if request.POST.get('ingredients') in item_title:
                item = IngredientsInStock.objects.get(ingredients = request.POST.get('ingredients'))
                item.quantity = int(item.quantity) + int(request.POST.get('quantity'))
                item.cost_price = int(item.cost_price) + int(request.POST.get('cost_price'))
                item.save()
                form = IngredientsInStockForm()
                return render(request, 'Admin_App/addIngredientsInStock.html', {'form': form.as_p})

            else:
                form.save()
                form = IngredientsInStockForm()
                return render(request, 'Admin_App/addIngredientsInStock.html', {'form': form.as_p})
    else:
        form = IngredientsInStockForm()

    return render(request, 'Admin_App/addIngredientsInStock.html', {'form' : form.as_p})



def updateQuantity():
    ingredientsObjects = Ingredients.objects.all()
    ingredientsName = []
    for x in ingredientsObjects:
        ingredientsName.append(x.ingredients)

    for x in ingredientsObjects:
        if x.bakery_item is not None:
            x.quantity = 0
            x.save()

def sellingPrice():
    pass