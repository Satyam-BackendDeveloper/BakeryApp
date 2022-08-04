from django.db import models

# Create your models here.





class Bakery_Item(models.Model):
    quantity = models.IntegerField()
    title = models.CharField(max_length=10, unique=True)
    profit = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"


class IngredientsRequiredForItem(models.Model):
    ingredients = models.CharField(max_length=25,)
    quantity = models.IntegerField()
    bakery_item = models.CharField(max_length=25)

    def __str__(self):
        return f"Bakery Item : {self.bakery_item}, \n" \
            f"Ingredient : {self.ingredients} \n" \
               f" , Quantity : {self.quantity} \n" \



class IngredientsInStock(models.Model):
    ingredients = models.CharField(max_length=25, unique=True)
    quantity = models.IntegerField()
    cost_price = models.IntegerField()

    def __str__(self):
        return f"Ingredient : {self.ingredients} \n" \
               f" , Quantity : {self.quantity} \n" \
                f" , Cost Price : {self.cost_price}"
















