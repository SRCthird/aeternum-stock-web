# Generated by Django 5.1.2 on 2024-11-08 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_historicalinventorybaylot'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryLot',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('inventory.inventorybaylot',),
        ),
        migrations.CreateModel(
            name='ReleasedLot',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('inventory.inventorybaylot',),
        ),
        migrations.CreateModel(
            name='ScrappedLot',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('inventory.inventorybaylot',),
        ),
    ]
