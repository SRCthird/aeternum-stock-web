from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from . import models

admin.AdminSite.site_header = "Aeternum Stock - Admin Center"


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
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
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active',)
    list_filter = ('name', 'active',)
    search_fields = ('name', 'active',)

    fieldsets = (
        (None, {
            'fields': ('name', 'active',)
        }),
    )


@admin.register(models.InventoryBay)
class InventoryBayAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'warehouse_name',
        'max_unique_lots', 'friendly_name', 'active',
    )
    list_filter = (
        'name', 'warehouse_name', 'max_unique_lots',
        'friendly_name', 'active',
    )
    search_fields = (
        'name', 'warehouse_name', 'max_unique_lots',
        'friendly_name', 'active',
    )

    fieldsets = (
        (None, {
            'fields': (
                'name', 'warehouse_name',
                'max_unique_lots', 'friendly_name', 'active',
            )
        }),
    )


@admin.register(models.Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'lot_number', 'location',
        'from_location', 'quantity', 'comments',
        'created_by', 'created_at', 'updated_by',
        'updated_at',
    )
    list_filter = (
        'lot_number', 'location', 'from_location',
        'quantity', 'comments', 'created_by',
        'created_at', 'updated_by', 'updated_at',
    )
    search_fields = (
        'lot_number', 'warehouse_name', 'from_location',
        'quantity', 'comments', 'created_by',
        'created_at', 'updated_by', 'updated_at',
    )

    fieldsets = (
        (None, {
            'fields': (
                'lot_number', 'location',
                'from_location', 'quantity', 'comments', 'created_by',
                'created_at', 'updated_by', 'updated_at',
            )
        }),
    )
