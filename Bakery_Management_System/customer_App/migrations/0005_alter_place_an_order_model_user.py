# Generated by Django 4.0.6 on 2022-07-22 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_App', '0004_rename_sellingprice_place_an_order_model_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place_an_order_model',
            name='user',
            field=models.CharField(default=0, max_length=20),
        ),
    ]