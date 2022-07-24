from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm, LoginForm, CartForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from Admin_App.models import Bakery_Item, IngredientsRequiredForItem, IngredientsInStock
from django.forms import formset_factory, modelformset_factory, inlineformset_factory, forms
from .models import Place_an_order_model
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html' )

def signup(request):
    if request.method == 'POST':
            signupForm = SignupForm(request.POST)
            if signupForm.is_valid():
                user = signupForm.save()
                return render(request, 'thanks.html', {})
    else:
            signupForm = SignupForm()

    return render(request, 'signup.html', {'signupForm': signupForm.as_p})


def thanks(request):
    return render(request, 'thanks.html')

def loginViewFunction(request):
    if request.method == 'POST':
        loginPage= LoginForm(request.POST)

        if loginPage.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                if user.is_active and user.is_superuser:
                    return render(request, 'Admin_App/index.html', {})
                else:
                    return render(request, 'dashboard.html', {})
            else:
                return HttpResponse("Username or Password is incorrect")
    else:
        loginPage = LoginForm()

    return render(request, 'loginPage.html',{'form': loginPage.as_p})

def dashboard(request):
    return render(request, 'dashboard.html', {})

def view_all_items_function(request):

    items = Bakery_Item.objects.all()
    return render(request,'view_all_items.html', {'items': items})

def Cart(request):
    # OrderFormSet = inlineformset_factory(get_user_model(), Place_an_order_model, fields=['Item', 'Quantity'])
    # user = get_user_model().objects.get(username = request.user.username)
    # if(request.method == 'POST'):
    #     ff = OrderFormSet(request.POST, instance = user)
    #     if(ff.is_valid()):
    #         return HttpResponse(ff.get('Item'))
    #         ff.save()
    #         return render(request, 'dashboard.html', {})
    # else:
    #     ff = OrderFormSet(queryset = Place_an_order_model.objects.none(),
    #                       instance = user)
    # return render(request, 'place_an_order.html', {'formset' : ff})

    placedOrder = Place_an_order_model.objects.filter(user=request.user.id)
    products = []
    for item in placedOrder:
        products.append(item.Item)

    if(request.method == 'POST'):
        c = CartForm(request.POST)
        bakery_item = Bakery_Item.objects.get(id=request.POST.get('Item'))

        if c.is_valid():
            if bakery_item.quantity >= int(request.POST.get('Quantity')):
                bakery_item.quantity = bakery_item.quantity - int(request.POST.get('Quantity'))
                bakery_item.save()
                item = Place_an_order_model.objects.get(Item =request.POST.get('Item'))

                if item in products:
                    item.Quantity = int(item.Quantity) + int(request.POST.get('Quantity'))
                    item.save()

                # c.user = request.user.username
                else:
                    c.save()
                    c = CartForm()
                    return render(request, 'place_an_order.html', {'formset': c.as_p})

            else:
                return HttpResponse(f"Out of Stock")
    else:
        c = CartForm()
    return render(request, 'place_an_order.html', {'formset' : c.as_p})



def see_order_history(request):
    placed = Place_an_order_model.objects.filter(user=request.user.id)
    return render(request, 'see_order_history.html', {'placed':placed})



def get_bill(request):

    items = Bakery_Item.objects.all()
    # ingredients = Ingredients.objects.all()
    placed = Place_an_order_model.objects.filter(user = request.user.id)
    sp = sellingPrice()

    amount= 0
    billAmount = {}
    for p in placed:
        billAmount[p.Item.title] = sp[p.Item.title] * p.Quantity
        amount += (sp[p.Item.title] * p.Quantity)

    return render(request, 'get_bill.html', {'amount' : amount, 'dict': billAmount})


def sellingPrice():
    ingredientsInStock = IngredientsInStock.objects.all()
    bakery_item = Bakery_Item.objects.all()
    ingredientsAttachedToBakeryItem = IngredientsRequiredForItem.objects.all()

    cp = {}
    sp = {}

    for ingredients in ingredientsInStock:
        cp[ingredients.ingredients] = ingredients.cost_price

    for item in bakery_item:
        sp[item.title] = 0


    for item in bakery_item:
        for ingredients in ingredientsAttachedToBakeryItem:
            if item == ingredients.bakery_item:
                sp[item.title] += cp[ingredients.ingredients] * ingredients.quantity

    for item in bakery_item:
        sp[item.title] += (item.profit)
    return HttpResponse(sp.items())
    return sp