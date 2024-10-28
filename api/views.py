from django.http import JsonResponse
from inventory.models import InventoryBayLot


def get_inventory_bays_for_lot(request, product_lot_id):
    """Returns Inventory Bays where the given ProductLot has a quantity > 0."""
    inventory_data = []

    # Get Inventory Bays with quantities > 0 for the selected ProductLot
    bays_with_lot = InventoryBayLot.objects.filter(
        product_lot_id=product_lot_id,
        quantity__gt=0
    ).select_related('inventory_bay')

    for lot in bays_with_lot:
        inventory_data.append({
            'id': lot.inventory_bay.id,
            'name': lot.inventory_bay.name,
        })

    return JsonResponse({'bays': inventory_data})

