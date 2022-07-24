from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm, LoginForm, CartForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from Admin_App.models import Bakery_Item, IngredientsRequiredForItem, IngredientsInStock
from django.forms import formset_factory, modelformset_factory, inlineformset_factory, forms
from .models import Place_an_order_model
from django.contrib.auth.models import User


def index(request):
    #it's the Homepage of our webApp which contains signup and login links for our User
    # only user not admin can signup but admin also have functionality of login into the app
    return render(request, 'index.html' )

def signup(request):
    # it asks for username (unique), email, password, age, mobile Number and user data gets saved in database
    if request.method == 'POST':
            signupForm = SignupForm(request.POST)
            if signupForm.is_valid():
                user = signupForm.save()
                return render(request, 'thanks.html', {})
    else:
            signupForm = SignupForm()

    return render(request, 'signup.html', {'signupForm': signupForm.as_p})


def thanks(request):
    #it's the redirect page for signup User
    return render(request, 'thanks.html')

def loginViewFunction(request):
    #signup User can login into their dashboards acoording to their authority like admin or normal user
    # dashboard for admin is different and for normal user it's different
    #it authenticate from our database whether that is user is valid or not
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
    #it contains all the links to normal user like viewing items, placing orders, checking order history, getting Bill Amount
    return render(request, 'dashboard.html', {})

def view_all_items_function(request):
    # it views all details of items present in the bakery
    items = Bakery_Item.objects.all()
    return render(request,'view_all_items.html', {'items': items})

def Cart(request):
    # this function allows user to place their orders, update their order quantity
    # as well as decrease quantity from our bakery when its been placed by user in his cart
    # it also checks for the available item and its quantity in our bakery Stock
    # it also attached a particular order to the login user only




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

    # placedOrder = Place_an_order_model.objects.filter(user=request.user.id)
    # products = []
    # for item in placedOrder:
    #     products.append(item.Item.title)
    #
    # return HttpResponse(products)



    if(request.method == 'POST'):
        placedOrder = Place_an_order_model.objects.filter(user=request.user.id)
        products = []
        for item in placedOrder:
            products.append(item)

        c = CartForm(request.POST)
        bakery_item = Bakery_Item.objects.get(id=request.POST.get('Item'))

        if c.is_valid() and int(request.POST.get('user')) == request.user.id:
            if bakery_item.quantity >= int(request.POST.get('Quantity')):
                bakery_item.quantity = bakery_item.quantity - int(request.POST.get('Quantity'))
                bakery_item.save()
                for item in placedOrder:
                    if item.Item == bakery_item:
                        item.Quantity = int(request.POST.get('Quantity'))
                        item.save()
                        c = CartForm()
                        return render(request, 'place_an_order.html', {'formset': c.as_p})

                c.save()
                c = CartForm()
                return render(request, 'place_an_order.html', {'formset': c.as_p})

                # c.user = request.user.username
            else:
                return HttpResponse(f"Out of Stock")
        else:
            return HttpResponse("Invalid User or Invalid Form Entry")
    else:
        c = CartForm()
    return render(request, 'place_an_order.html', {'formset' : c.as_p})



def see_order_history(request):
    #it displays order history of the products placed by current login user

    placed = Place_an_order_model.objects.filter(user=request.user.id)
    return render(request, 'see_order_history.html', {'placed':placed})



def get_bill(request):
    #it generates bill according to orders placed
    # it takes cost_price from ingredients in stock available and ingredients required for that particular item
    # it takes profit from item input by admin when adding that item in bakery

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
            if item.title == ingredients.bakery_item:
                sp[item.title] += cp[ingredients.ingredients] * ingredients.quantity

    for item in bakery_item:
        sp[item.title] += (item.profit)
    return sp

def payment(request):
    #it leads user to payment gateway and once payment is successfull
    # all items from cart gets deleted


    placed = Place_an_order_model.objects.filter(user=request.user.id)

    for item in placed:
        item.delete()

    return render(request, "payment.html", {})