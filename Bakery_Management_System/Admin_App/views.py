from django.http import HttpResponse
from rest_framework import status


from .models import IngredientsRequiredForItem, Bakery_Item, IngredientsInStock
from .serializers import AddIngredientsToStockSerializer, BakeryItemSerializer, IngredientsRequiredForItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
import json

class AddIngredientsToStockAPI(APIView):
    # items = IngredientsInStock.objects.all()
    # item_title = []
    # for x in items:
    #     item_title.append(x.ingredients)

    def get_object(self, name):
        try:
            return IngredientsInStock.objects.get(ingredients=name)
        except IngredientsInStock.DoesNotExist:
            raise Http404

    # def get(self, request):
    #     ingredients = IngredientsInStock.objects.all()
    #     ingredients_serializer = AddIngredientsToStockSerializer(ingredients, many=True)
    #     return Response(ingredients_serializer.data)

    def get(self, request, name):
        ingredients = self.get_object(name)
        ingredients_serializer = AddIngredientsToStockSerializer(ingredients)
        return Response(ingredients_serializer.data)

    def post(self, request):
        ingredients_serializer = AddIngredientsToStockSerializer(data=request.data)

        if ingredients_serializer.is_valid():
            ingredients_serializer.save()
            return Response(ingredients_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'Serializer' : 'Invalid'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        ingredients_serializer = AddIngredientsToStockSerializer(data=request.data)

        if ingredients_serializer.is_valid:
                item = IngredientsInStock.objects.get(ingredients=request.data['ingredients'])
                if item is not None:
                    item.quantity = int(item.quantity) + int(request.data['quantity'])
                    if int(item.cost_price) < int(request.data['cost_price']):
                        item.cost_price = request.data['cost_price']
                    item.save()
                    return Response({'Item Quantity' : 'updated'}, status=status.HTTP_204_NO_CONTENT)
                return Response({'ingredient in Stock' : 'not present'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Serializer' : 'Invalid'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        item = self.get_object(name)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddBakeryItemAPI(APIView):
    # items = Bakery_Item.objects.all()
    # item_title = []
    # for x in items:
    #     item_title.append(x.title)


    def get_object(self, name):
        try:
            return Bakery_Item.objects.get(title=name)
        except Bakery_Item.DoesNotExist:
            raise Http404

    def get(self, request):
        item = Bakery_Item.objects.all()
        item_serializer = BakeryItemSerializer(item, many=True)
        return Response(item_serializer.data)

    def post(self, request):
        item_serializer = BakeryItemSerializer(data=request.data)

        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        item_serializer = BakeryItemSerializer(data=request.data)

        if item_serializer.is_valid:
                item = Bakery_Item.objects.get(title=request.data['title'])
                if item is not None:
                    item.quantity = int(item.quantity) + int(request.data['quantity'])

                    if int(item.profit) < int(request.data['profit']):
                        item.profit = request.data['profit']
                    item.save()
                    return Response(item_serializer.data, status=status.HTTP_204_NO_CONTENT)
                return Response({'item':'not present'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'serializer' : 'invalid'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        item = self.get_object(name)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddIngredientsRequiredForBakeryItemAPI(APIView):
    def get(self, request):
        item = IngredientsRequiredForItem.objects.all()
        item_serializer = IngredientsRequiredForItemSerializer(item, many=True)
        return Response(item_serializer.data)

    def post(self, request):
        ingredientInItem = IngredientsRequiredForItem.objects.filter(bakery_item=request.data['bakery_item'])
        item_titleInBakeryObjects = []
        for x in ingredientInItem:
            item_titleInBakeryObjects.append(x.ingredients)

        item_serializer = IngredientsRequiredForItemSerializer(data=request.data)


        if item_serializer.is_valid():
            if request.data['ingredients'] in item_titleInBakeryObjects:
                return Response(item_serializer.errors, status=status.HTTP_226_IM_USED)
            item_serializer.save()
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        ingredientInItem = IngredientsRequiredForItem.objects.filter(bakery_item=request.data['bakery_item'])
        item_titleInBakeryObjects = []
        for x in ingredientInItem:
            item_titleInBakeryObjects.append(x.ingredients)


        item_serializer = IngredientsRequiredForItemSerializer(data=request.data)

        if item_serializer.is_valid():
            if request.data['ingredients'] in item_titleInBakeryObjects:
                item = IngredientsRequiredForItem.objects.get(ingredients=request.data['ingredients'],
                                                              bakery_item=request.data['bakery_item'])
                item.quantity = int(request.data['quantity'])
                item.save()
                return Response(item_serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(item_serializer.errors, status=status.HTTP_404_NOT_FOUND)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        item = IngredientsRequiredForItem.objects.get(ingredients=request.data['ingredients'],
                                                      bakery_item=request.data['bakery_item'])
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class inventoryAPI(APIView):
    # this function will display the ingredients and their quantity left in stock
    # and the bakery items with their quantity present in our Bakery

    def get(self, request):
        bakery_item = Bakery_Item.objects.all()

        ingredients_objects = IngredientsInStock.objects.all()
        ingredients_details = {}

        item_details = {}

        for item in ingredients_objects:
            ingredients_details[item.ingredients] = item.quantity

        for item in bakery_item:
            item_details[item.title] = item.quantity

        dict = {}

        for key,values in ingredients_details.items():
            dict[key] = values
        for key,values in item_details.items():
            dict[key] = values
        return Response(dict, status=status.HTTP_200_OK)
