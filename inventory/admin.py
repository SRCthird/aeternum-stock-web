from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from . import models
from csvexport.actions import csvexport
import csv
from django.http import HttpResponse
from django.conf import settings

admin.AdminSite.site_header = "Aeternum Stock - Admin Center"
admin.site.site_url = f"../../{settings.SITE_PREFIX}"


@admin.register(models.Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'description',)
    list_filter = ('name', 'description',)
    search_fields = ('name', 'description',)

    actions = [csvexport]
    csvexport.short_description = "Export Selected Items as CSV"

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

    actions = [csvexport]
    csvexport.short_description = "Export Selected Items as CSV"

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

    actions = [csvexport]
    csvexport.short_description = "Export Selected Items as CSV"

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

    actions = [csvexport]
    csvexport.short_description = "Export Selected Items as CSV"

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

    actions = [csvexport]
    csvexport.short_description = "Export Selected Items as CSV"

    fieldsets = (
        (None, {
            'fields': ('inventory_bay', 'product_lot', 'quantity',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(quantity__gt=0)


@admin.action(description="Export Selected Audit to CSV")
def ExportInventoryTransferAdmin(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="inventory_transfer.csv"'

    writer = csv.writer(response, quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow([
        'ID', 'Product Lot', 'From Inventory Bay', 'To Inventory Bay',
        'Quantity', 'Transfer Date', 'Changed By'
    ])

    for obj in queryset:
        latest_history = obj.history.first()
        changed_by = latest_history.history_user if latest_history and latest_history.history_user else "Unknown"
        writer.writerow([
            obj.id,
            obj.product_lot,
            obj.from_inventory_bay,
            obj.to_inventory_bay,
            obj.quantity,
            obj.transfer_date,
            changed_by
        ])

    return response


@admin.register(models.InventoryTransfer)
class InventoryTransferAdmin(SimpleHistoryAdmin):
    list_display = (
        'id', 'product_lot', 'from_inventory_bay', 'to_inventory_bay',
        'quantity', 'transfer_date', 'latest_history_user',
    )
    list_filter = (
        'product_lot', 'from_inventory_bay', 'to_inventory_bay',
        'transfer_date',
    )
    search_fields = (
        'product_lot__lot_number', 'from_inventory_bay__name', 'to_inventory_bay__name',
    )

    actions = [csvexport, ExportInventoryTransferAdmin]
    csvexport.short_description = "Export Selected Items as CSV"

    fieldsets = (
        (None, {
            'fields': (
                'product_lot', 'from_inventory_bay', 'to_inventory_bay',
                'quantity',
            )
        }),
    )

    def latest_history_user(self, obj):
        latest_history = obj.history.first()
        return latest_history.history_user if latest_history and latest_history.history_user else "Unknown"
    latest_history_user.short_description = "Changed by"
