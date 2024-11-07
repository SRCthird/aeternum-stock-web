from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.conf import settings

from simple_history.admin import SimpleHistoryAdmin
from csvexport.actions import csvexport
from more_admin_filters import MultiSelectDropdownFilter, BooleanAnnotationFilter
import csv

from . import models

admin.AdminSite.site_header = "Aeternum Stock - Admin Center"
admin.site.site_url = f"../../{settings.SITE_PREFIX}"


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    list_filter = ['user', 'content_type', 'action_flag']
    search_fields = ['object_repr', 'change_message']
    list_display = ['action_time', 'user',
                    'content_type', 'object_link', 'action_flag', ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' %
                        (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


@admin.register(models.Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'description',)
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
        'latest_history_user'
    )
    list_filter = (
        ('product_name__name', MultiSelectDropdownFilter),
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

    def latest_history_user(self, obj):
        latest_history = obj.history.first()
        return latest_history.history_user if latest_history and latest_history.history_user else "Unknown"
    latest_history_user.short_description = "Changed by"


@admin.register(models.Warehouse)
class WarehouseAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'active',)
    list_filter = (
        'active',
    )
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
        ('warehouse_name__name', MultiSelectDropdownFilter),
        ('max_unique_lots', MultiSelectDropdownFilter),
        'active',
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


# @admin.register(models.InventoryBayLot)
class InventoryBayLotAdmin(SimpleHistoryAdmin):
    list_display = (
        'inventory_bay', 'product_lot', 'quantity',
    )
    list_filter = (
        ('inventory_bay__warehouse_name__name', MultiSelectDropdownFilter),
    )
    search_fields = (
        'inventory_bay__name', 'inventory_bay__friendly_name', 'product_lot__lot_number',
    )

    actions = [csvexport]
    csvexport.short_description = "Export Selected Items as CSV"

    fieldsets = (
        (None, {
            'fields': ('inventory_bay', 'product_lot', 'quantity',)
        }),
    )


class InventoryLot(models.InventoryBayLot):
    class Meta:
        proxy = True


@admin.register(InventoryLot)
class ActiveLotAdmin(InventoryBayLotAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            quantity__gt=0,
        ).exclude(
            inventory_bay__name="Released"
        ).exclude(
            inventory_bay__name="Scrapped"
        )


class ReleasedLot(models.InventoryBayLot):
    class Meta:
        proxy = True


@admin.register(ReleasedLot)
class ReleasedLotAdmin(InventoryBayLotAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            quantity__gt=0,
            inventory_bay__name="Released"
        )


class ScrappedLot(models.InventoryBayLot):
    class Meta:
        proxy = True


@admin.register(ScrappedLot)
class ScrappedLotAdmin(InventoryBayLotAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            quantity__gt=0,
            inventory_bay__name="Scrapped"
        )


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
        ('transfer_date', admin.DateFieldListFilter),
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

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def latest_history_user(self, obj):
        latest_history = obj.history.first()
        return latest_history.history_user if latest_history and latest_history.history_user else "Unknown"
    latest_history_user.short_description = "Changed by"
