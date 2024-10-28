from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from . import models

admin.AdminSite.site_header = "Aeternum Stock - Admin Center"


@admin.register(models.Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'description',)
    list_filter = ('name', 'description',)
    search_fields = ('name', 'description',)

    fieldsets = (
        (None, {
            'fields': ('name', 'description',)
        }),
    )


@admin.register(models.ProductLot)
class ProductLotAdmin(SimpleHistoryAdmin):
    list_display = (
        'id', 'lot_number', 'internal_reference', 'product_name', 'quantity',
    )
    list_filter = (
        'lot_number', 'internal_reference', 'product_name', 'quantity',
    )
    search_fields = (
        'lot_number', 'internal_reference', 'product_name__name',
    )

    fieldsets = (
        (None, {
            'fields': (
                'lot_number', 'internal_reference', 'product_name', 'quantity',
            )
        }),
    )


@admin.register(models.Warehouse)
class WarehouseAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'active',)
    list_filter = ('name', 'active',)
    search_fields = ('name', 'active',)

    fieldsets = (
        (None, {
            'fields': ('name', 'active',)
        }),
    )


@admin.register(models.InventoryBay)
class InventoryBayAdmin(SimpleHistoryAdmin):
    list_display = (
        'id', 'name', 'warehouse_name',
        'max_unique_lots', 'friendly_name', 'active',
    )
    list_filter = (
        'name', 'warehouse_name', 'max_unique_lots',
        'friendly_name', 'active',
    )
    search_fields = (
        'name', 'warehouse_name__name', 'friendly_name',
    )

    fieldsets = (
        (None, {
            'fields': (
                'name', 'warehouse_name',
                'max_unique_lots', 'friendly_name', 'active',
            )
        }),
    )


@admin.register(models.InventoryBayLot)
class InventoryBayLotAdmin(SimpleHistoryAdmin):
    list_display = (
        'inventory_bay', 'product_lot', 'quantity',
    )
    list_filter = (
        'inventory_bay', 'product_lot',
    )
    search_fields = (
        'inventory_bay__name', 'product_lot__lot_number',
    )

    fieldsets = (
        (None, {
            'fields': ('inventory_bay', 'product_lot', 'quantity',)
        }),
    )


@admin.register(models.InventoryTransfer)
class InventoryTransferAdmin(SimpleHistoryAdmin):
    list_display = (
        'id', 'product_lot', 'from_inventory_bay', 'to_inventory_bay',
        'quantity', 'transfer_date',
    )
    list_filter = (
        'product_lot', 'from_inventory_bay', 'to_inventory_bay',
        'transfer_date',
    )
    search_fields = (
        'product_lot__lot_number', 'from_inventory_bay__name', 'to_inventory_bay__name',
    )

    fieldsets = (
        (None, {
            'fields': (
                'product_lot', 'from_inventory_bay', 'to_inventory_bay',
                'quantity',
            )
        }),
    )
