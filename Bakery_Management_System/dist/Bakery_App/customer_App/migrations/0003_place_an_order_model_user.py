# Generated by Django 4.0.6 on 2022-07-18 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer_App', '0002_loginmodel_place_an_order_model_delete_loginuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='place_an_order_model',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]