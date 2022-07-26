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

from .models import IngredientsRequiredForItem, Bakery_Item, IngredientsInStock
from .forms import BakeryItemForm, IngredientsForm, IngredientsInStockForm
from customer_App.views import sellingPrice


def welcome(request):
    #This function will display the home page of our Adminapp
    #Only admin have permission to access this
    # which contains all links to other functions of Bakery Admin


    return render(request, 'Admin_App/index.html')

def display_all_items(request):
    #this function will display all items present in Our Bakery
    #with their required ingredients


    bakery_item = Bakery_Item.objects.all()
    ingredients_objects = IngredientsRequiredForItem.objects.all()
    return render(request, 'Admin_App/all_items.html', {"bakery_item" : bakery_item, "ingredients" : ingredients_objects})


def inventory(request):
    # this function will display the ingredients and their quantity left in stock
    # and the bakery items with their quantity present in our Bakery


    bakery_item = Bakery_Item.objects.all()

    ingredients_objects = IngredientsInStock.objects.all()
    ingredients_details = {}

    item_details = {}

    for item in ingredients_objects:
        ingredients_details[item.ingredients] = item.quantity

    for item in bakery_item:
        item_details[item.title] = item.quantity

    return render(request, 'Admin_App/inventory.html', {"inventory" : ingredients_details, "bakeryItem" : item_details})

def admin_Page(request):
    # it's an Validation function to check only superuser is allowed to visit
    #127.0.0.1:8000/admin interface

    user = request.user
    if user.is_active and user.is_superuser:
        return render(request, 'index.html', {})


def addItem(request):
    # this function will add Bakery Items Only When the required ingredients are present in
    # Stock with there required quantity and also it will update the quantity of ingredients
    # in stock when an item is added, if admin adds the same item again it will update its quantity
    # if item is not present in Bakery then new item will get added and required ingredients from
    # stock gets decreased

    items = Bakery_Item.objects.all()
    ingredientsInStock = IngredientsInStock.objects.all()

    item_title = []
    for x in items:
        item_title.append(x.title)



    if(request.method == 'POST'):
        form = BakeryItemForm(request.POST)
        if form.is_valid():
            item = IngredientsRequiredForItem.objects.filter(bakery_item=request.POST.get('title'))
            requiredIngredients = {}
            for x in item:
                requiredIngredients[x.ingredients] = x.quantity * int(request.POST.get('quantity'))

            if(len(requiredIngredients) == 0):
                return HttpResponse("No Ingredients defined for Item")


            item = request.POST.get('title')
            if item in item_title:
                item = Bakery_Item.objects.get(title=request.POST.get('title'))

            allIngredientsList = []
            for x in ingredientsInStock:
                allIngredientsList.append(x.ingredients)

            for x,y in requiredIngredients.items():
                if x in allIngredientsList:
                    ingredient = IngredientsInStock.objects.get(ingredients = x)
                    if ingredient.quantity >= y:
                        pass
                    else:
                        return HttpResponse(f"{ingredient.ingredients} Insufficient Quantity")

                else:
                    return HttpResponse("Insufficient Ingredients")

            for x, y in requiredIngredients.items():
                ingredient = IngredientsInStock.objects.get(ingredients = x)
                ingredient.quantity -= y
                ingredient.save()

            if item.title not in item_title:
                form.save()
            else:
                item.profit = request.POST.get('profit')
                if request.POST.get('title') in item_title:
                    item.quantity = int(item.quantity) + int(request.POST.get('quantity'))
                item.save()

    else:
        form = BakeryItemForm()
    return render(request, 'Admin_App/addItem.html', {'form' : form.as_p})


def itemsRequiredForBakeryItem(request):
    #this functions allows bakery admin to store the required ingredients
    # with their required quantity for a single bakery Item
    # if bakery admin wants to update the quantity of any ingredients
    # then on same ingredient it will get update


    ingredientInItem = IngredientsRequiredForItem.objects.filter(bakery_item=request.POST.get('bakery_item'))

    item_titleInBakeryObjects = []

    for x in ingredientInItem:
        item_titleInBakeryObjects.append(x.ingredients)

    if (request.method == 'POST'):
        form = IngredientsForm(request.POST)
        if form.is_valid():
            if request.POST.get('ingredients') in item_titleInBakeryObjects:
                item = IngredientsRequiredForItem.objects.get(ingredients=request.POST.get('ingredients'),
                                                              bakery_item=request.POST.get('bakery_item'))
                item.quantity = int(request.POST.get('quantity'))
                item.save()
                form = IngredientsForm()
                return render(request, 'Admin_App/addIngredients.html', {'form': form.as_p})

            else:
                form.save()
                form = IngredientsForm()
                return render(request, 'Admin_App/addIngredients.html', {'form': form.as_p})
    else:
        form = IngredientsForm()

    return render(request, 'Admin_App/addIngredients.html', {'form' : form.as_p})


def addIngredientsToStock(request):
    # This view function will add ingredients to Stock
    # If an ingredient is already present then it will add the new quantity with previous One
    # also it takes the cost price of each ingredient per unit
    # it also updates the cost price as per current Input, If its larger then update (override) else Previous
    # Cost Price will be saved

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

                if int(item.cost_price) < int(request.POST.get('cost_price')):
                    item.cost_price = request.POST.get('cost_price')

                item.save()
                form = IngredientsInStockForm()
                return render(request, 'Admin_App/addIngredientsInStock.html', {'form': form.as_p})

            else:
                form.save()
                item = IngredientsInStock.objects.get(ingredients=request.POST.get('ingredients'))
                item.cost_price = request.POST.get('cost_price')
                item.save()


                form = IngredientsInStockForm()
                return render(request, 'Admin_App/addIngredientsInStock.html', {'form': form.as_p})
    else:
        form = IngredientsInStockForm()

    return render(request, 'Admin_App/addIngredientsInStock.html', {'form' : form.as_p})
