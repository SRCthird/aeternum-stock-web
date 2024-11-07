from django.http import JsonResponse
from inventory.models import InventoryBayLot, Product, InventoryBay


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:10]
    results = [{'id': product.id, 'name': product.name}
               for product in products]
    return JsonResponse(results, safe=False)


def to_inventory_bay_search(request):
    query = request.GET.get('q', '')
    bays = InventoryBay.objects.filter(friendly_name__icontains=query, active=True)[:10]
    results = [{'id': bay.id, 'name': bay.friendly_name} for bay in bays]
    return JsonResponse(results, safe=False)


def get_inventory_bays_for_lot(request, product_lot_id):
    """Returns Inventory Bays where the given ProductLot has a quantity > 0."""
    inventory_data = []

    bays_with_lot = InventoryBayLot.objects.filter(
        product_lot_id=product_lot_id,
        quantity__gt=0
    ).select_related('inventory_bay')

    for lot in bays_with_lot:
        inventory_data.append({
            'id': lot.inventory_bay.id,
            'name': lot.inventory_bay.friendly_name,
        })

    return JsonResponse({'bays': inventory_data})
