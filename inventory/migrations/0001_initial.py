# Generated by Django 5.1.2 on 2024-10-24 16:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryBay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=191, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('max_unique_lots', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=191, unique=True)),
                ('description', models.CharField(max_length=191)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=191, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot_number', models.CharField(max_length=191, unique=True)),
                ('internal_reference', models.CharField(max_length=191, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('quantity_moved', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=191)),
                ('from_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_location', to='inventory.inventorybay')),
                ('to_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_location', to='inventory.inventorybay')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('lot_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.productlot')),
            ],
        ),
        migrations.AddField(
            model_name='inventorybay',
            name='warehouse_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='inventory.warehouse'),
        ),
    ]