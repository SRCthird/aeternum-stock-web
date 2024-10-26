# Generated by Django 5.1.2 on 2024-10-25 11:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_inventorybay_warehouse_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='from_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_from_location', to='inventory.inventorybay'),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('comments', models.CharField(max_length=191, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_objects', to=settings.AUTH_USER_MODEL)),
                ('from_location', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='inventory_from_location', to='inventory.inventorybay')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='current_location', to='inventory.inventorybay')),
                ('lot_number', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='inventory.productlot')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_objects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]