from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, RESTRICT, SET_NULL
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=191,
        unique=True,
        blank=False,
        null=False,
    )
    description = models.CharField(
        max_length=191,
        blank=False,
        null=False,
    )


class ProductLot(models.Model):
    id = models.AutoField(primary_key=True)
    lot_number = models.CharField(
        max_length=191,
        unique=True,
    )
    internal_reference = models.CharField(
        max_length=191,
        unique=True,
    )
    product_name = models.ForeignKey(
        Product,
        on_delete=CASCADE,
    )
    quantity = models.IntegerField(default=0)


class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=191,
        unique=True,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'


class InventoryBay(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=191,
        unique=True,
    )
    warehouse_name = models.ForeignKey(
        Warehouse,
        on_delete=RESTRICT,
        to_field='name'
    )
    max_unique_lots = models.IntegerField(default=1)
    friendly_name = models.CharField(
        max_length=191,
        unique=True,
    )
    active = models.BooleanField(default=True)


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    lot_number = models.ForeignKey(
        ProductLot,
        on_delete=RESTRICT,
    )
    location = models.ForeignKey(
        InventoryBay,
        on_delete=RESTRICT,
        related_name='current_location',
    )
    from_location = models.ForeignKey(
        InventoryBay,
        on_delete=RESTRICT,
        related_name='inventory_from_location',
    )
    quantity = models.IntegerField(default=1)
    comments = models.CharField(
        max_length=191,
        unique=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=SET_NULL,
        related_name='created_objects',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='updated_objects',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not self.pk:
            self.created_by = user
            self.created_at = timezone.now()
        self.updated_by = user
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    # class Meta:
    #     abstract = True


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    from_location = models.ForeignKey(
        InventoryBay,
        on_delete=CASCADE,
        related_name='log_from_location',
    )
    to_location = models.ForeignKey(
        InventoryBay,
        on_delete=CASCADE,
        related_name='to_location',
    )
    date_time = models.DateTimeField(
        auto_now_add=True
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=SET_NULL,
        null=True,
        blank=True
    )
    lot_number = models.ForeignKey(
        ProductLot,
        on_delete=CASCADE,
    )
    quantity_moved = models.IntegerField(default=0)
    comments = models.CharField(
        max_length=191
    )
