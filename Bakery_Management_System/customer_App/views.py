from django.contrib.auth import authenticate, login, logout, get_user_model
from Admin_App.models import Bakery_Item, IngredientsRequiredForItem, IngredientsInStock
from .models import Place_an_order_model, LoginModel
from django.contrib.auth.models import User
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from .serializers import LoginModelSerializer, PlaceAnOrderModelSerializer, SignupUserSerializer, SeeOrderHistorySerializer

class PlaceAnOrderAPI(APIView):
    def get(self, request):
        item = Place_an_order_model.objects.filter(user = request.user.id)
        item_serializer = PlaceAnOrderModelSerializer(item, many=True)
        return Response(item_serializer.data)

    def post(self, request):
        # placedOrder = Place_an_order_model.objects.filter(user=request.data['user'])
        # products = []
        # for item in placedOrder:
        #     products.append(item.Item)


        item_serializer = PlaceAnOrderModelSerializer(data=request.data)

        bakery_item = Bakery_Item.objects.get(id=request.data['Item'])

        if item_serializer.is_valid() and request.data['user'] == request.user.id:
            if bakery_item.quantity >= int(request.data['Quantity']):
                bakery_item.quantity = bakery_item.quantity - int(request.data['Quantity'])
                bakery_item.save()

                # if bakery_item in products:
                #     return Response({'item': 'already Present'}, status = status.HTTP_208_ALREADY_REPORTED)
                item_serializer.save()
                return Response(item_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'bakery_item' : 'out_of_stock'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'serializer' : 'invalid'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        placedOrder = Place_an_order_model.objects.get(user=request.data['user'], Item = request.data['Item'])
        item_serializer = PlaceAnOrderModelSerializer(data=request.data)
        if item_serializer.is_valid():
                if placedOrder is not None:
                    placedOrder.Quantity = int(request.data['Quantity'])
                    placedOrder.save()
                    return Response(item_serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response({'item' : 'not found'}, status=status.HTTP_302_FOUND)
        return Response({'serializer' : 'invalid'}, status=status.HTTP_400_BAD_REQUEST)



class SignupAPI(APIView):
    def get(self, request):
        item = User.objects.all()
        item_serializer = SignupUserSerializer(item, many=True)
        return Response(item_serializer.data)

    def post(self, request):
        user_serializer = SignupUserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
class LoginAPI(APIView):
    def post(self, request):
        user_serializer = LoginModelSerializer(data = request.data)
        if user_serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(request, username=username, password = password)

            if user is not None:
                login(request, user)
                return Response(user_serializer.data, status=status.HTTP_302_FOUND)
            else:
                return Response({'user' : 'un-authenticated'}, status=status.HTTP_403_FORBIDDEN)

class SeeOrderHistoryAPI(APIView):
    def get(self, request):
        placed = Place_an_order_model.objects.filter(user=request.user.id)
        item_serializer = SeeOrderHistorySerializer(placed, many=True)
        return Response(item_serializer.data)

class GetBillAPI(APIView):
    def get(self, request):

        items = Bakery_Item.objects.all()
        placed = Place_an_order_model.objects.filter(user=request.user.id)

        sp = sellingPrice()

        amount = 0
        billAmount = {}
        for p in placed:
            billAmount[p.Item.title] = sp[p.Item.title] * p.Quantity
            amount += (sp[p.Item.title] * p.Quantity)

        billAmount['Total Amount'] = amount

        return Response(billAmount, status=status.HTTP_200_OK)



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