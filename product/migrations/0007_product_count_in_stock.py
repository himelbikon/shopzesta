# Generated by Django 4.0.6 on 2022-07-20 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count_in_stock',
            field=models.IntegerField(default=15),
        ),
    ]