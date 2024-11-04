from django.db import models
from django.db.models import CASCADE, RESTRICT
from django.conf import settings
from simple_history.models import HistoricalRecords


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

    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'{self.name}'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


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

    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'{self.lot_number}'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=191,
        unique=True,
    )
    active = models.BooleanField(default=True)

    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'{self.name}'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


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

    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'{self.friendly_name}'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def get_lot_quantity(self, product_lot):
        """Get the current quantity of a specific ProductLot in this InventoryBay."""
        try:
            lot_quantity = self.lot_quantities.get(product_lot=product_lot)
            return lot_quantity.quantity
        except InventoryBayLot.DoesNotExist:
            return 0

    def adjust_quantity(self, product_lot, quantity_change):
        """Adjust the quantity of a specific ProductLot in this InventoryBay."""
        lot_quantity, created = InventoryBayLot.objects.get_or_create(
            inventory_bay=self,
            product_lot=product_lot
        )

        lot_quantity.quantity += quantity_change

        if lot_quantity.quantity < 0:
            raise ValueError(f"Quantity for {product_lot} in {
                             self.name} cannot be negative.")

        lot_quantity.save()


class InventoryBayLot(models.Model):
    inventory_bay = models.ForeignKey(
        InventoryBay,
        on_delete=models.CASCADE,
        related_name="lot_quantities"
    )
    product_lot = models.ForeignKey(
        ProductLot,
        on_delete=models.CASCADE,
        related_name="inventory_bays"
    )
    quantity = models.IntegerField(default=0)

    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = ('inventory_bay', 'product_lot')

    def __str__(self):
        return f'{self.product_lot} in {self.inventory_bay} with quantity {self.quantity}'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class InventoryTransfer(models.Model):
    id = models.AutoField(primary_key=True)
    product_lot = models.ForeignKey(
        ProductLot,
        on_delete=models.CASCADE,
        related_name="transfers"
    )
    from_inventory_bay = models.ForeignKey(
        InventoryBay,
        on_delete=models.RESTRICT,
        related_name="outgoing_transfers",
        null=True,
        blank=True
    )
    to_inventory_bay = models.ForeignKey(
        InventoryBay,
        on_delete=models.RESTRICT,
        related_name="incoming_transfers"
    )
    quantity = models.PositiveIntegerField()
    transfer_date = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        if self.from_inventory_bay:
            current_quantity = self.from_inventory_bay.get_lot_quantity(
                self.product_lot)
            if self.quantity > current_quantity:
                raise ValueError(
                    f"Insufficient quantity in {
                        self.from_inventory_bay} for transfer of {self.product_lot}."
                )

        existing_lots_with_quantity = self.to_inventory_bay.lot_quantities.filter(
            quantity__gt=0)

        if existing_lots_with_quantity.count() >= self.to_inventory_bay.max_unique_lots and self.to_inventory_bay.max_unique_lots != -1:
            if not existing_lots_with_quantity.filter(product_lot=self.product_lot).exists():
                raise ValueError(
                    f"Cannot transfer {self.product_lot} to {
                        self.to_inventory_bay}. "
                    f"Exceeds max unique lots limit of {
                        self.to_inventory_bay.max_unique_lots}."
                )

        super().save(*args, **kwargs)

        if self.from_inventory_bay:
            self.from_inventory_bay.adjust_quantity(
                self.product_lot, -self.quantity)
        self.to_inventory_bay.adjust_quantity(self.product_lot, self.quantity)

    def __str__(self):
        return f'Transfer of {self.quantity} from {self.from_inventory_bay} to {self.to_inventory_bay}'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
