from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse

from .models import InventoryBay, InventoryBayLot, ProductLot
from .forms import ProductLotForm, InventoryTransferForm


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def index(request):
    return render(request, 'home/base.html', {'title': 'Actions'})


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def create_item(request):
    if request.method == "POST":
        form = ProductLotForm(request.POST)
        if form.is_valid():
            new_product_lot = form.save()

            starting_bay = get_object_or_404(InventoryBay, name="Production")

            InventoryBayLot.objects.create(
                inventory_bay=starting_bay,
                product_lot=new_product_lot,
                quantity=new_product_lot.quantity
            )

            return redirect(reverse('index'))
    else:
        form = ProductLotForm()

    return render(request, 'home/create_item.html', {
        'title': 'Create Product Lot',
        'form': form
    })


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def transfer(request):
    product_lot_id = request.GET.get('product_lot')
    from_inventory_bay_id = request.GET.get('from_inventory_bay')
    action = request.GET.get('action')
    to_inventory_bay_name = None
    if action == 'release':
        to_inventory_bay_name = 'Released'
    elif action == 'scrapped':
        to_inventory_bay_name = 'Scrapped'
    quantity = request.GET.get('quantity')

    initial_data = {}
    if product_lot_id:
        initial_data['product_lot'] = get_object_or_404(
            ProductLot, id=product_lot_id)
    if from_inventory_bay_id:
        initial_data['from_inventory_bay'] = get_object_or_404(
            InventoryBay, id=from_inventory_bay_id)
    if to_inventory_bay_name:
        initial_data['to_inventory_bay'] = get_object_or_404(
            InventoryBay, name=to_inventory_bay_name)
    if quantity:
        initial_data['quantity'] = quantity

    if request.method == 'POST':
        form = InventoryTransferForm(request.POST, initial=initial_data)
        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = InventoryTransferForm(initial=initial_data)

    return render(request, 'home/transfer.html', {
        'form': form,
        'title': 'Inventory Transfer'
    })


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def find_lot(request):
    query = request.GET.get('q', '')
    inventory_bay_lots = InventoryBayLot.objects.filter(
        quantity__gt=0).select_related('inventory_bay__warehouse_name', 'product_lot')

    if query:
        inventory_bay_lots = inventory_bay_lots.filter(
            Q(product_lot__lot_number__icontains=query) |
            Q(inventory_bay__friendly_name__icontains=query) |
            Q(inventory_bay__warehouse_name__name__icontains=query)
        )

    return render(request, 'home/inventory_bay_lots_list.html', {
        'title': 'Inventory Bay Lots',
        'inventory_bay_lots': inventory_bay_lots,
        'search_query': query
    })
