from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from Admin_App.models import Bakery_Item, Ingredients
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
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

    return render(request, 'loginPage.html',{'form' : loginPage.as_p})

def dashboard(request):
    return render(request, 'dashboard.html', {})

def view_all_items_function(request):

    items = Bakery_Item.objects.all()
    return render(request,'view_all_items.html', {'items' : items})

def place_an_order(request):
    OrderFormSet = inlineformset_factory(get_user_model(), Place_an_order_model, fields=['Item', 'Quantity'])

    user = get_user_model().objects.get(username = request.user.username)

    if(request.method == 'POST'):
        ff = OrderFormSet(request.POST, instance = user)
        if(ff.is_valid()):
            ff.save()
            return render(request, 'dashboard.html', {})
    else:
        ff = OrderFormSet(queryset = Place_an_order_model.objects.none(),
                          instance = user)
    return render(request, 'place_an_order.html', {'formset' : ff})


def get_bill(request):

    items = Bakery_Item.objects.all()
    ingredients = Ingredients.objects.all()
    placed = Place_an_order_model.objects.filter(user = request.user.id)


    amount= 0
    for p in placed:
        if p.Item in items:
            return HttpResponse(p.Item is None)
        else:
            return HttpResponse("Hello")




    # return HttpResponse(placed[0].Item)

    # return HttpResponse(placed[0].user)
    # return HttpResponse(request.user.username)





    # return render(request, 'get_bill.html', {'amount' : amount})






def see_order_history(request):
    placed = Place_an_order_model.objects.filter(user = request.user.id)

    return render(request, 'see_order_history.html', {'placed':placed})


















