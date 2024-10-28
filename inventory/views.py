from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages

from .models import InventoryBay, InventoryBayLot
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

            starting_bay = get_object_or_404(InventoryBay, name="Operations")

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
    if request.method == 'POST':
        form = InventoryTransferForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, "Inventory transfer completed successfully.")
                return redirect(reverse('index'))
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = InventoryTransferForm()

    return render(request, 'home/transfer.html', {
        'title': 'Inventory Transfer',
        'form': form
    })


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def find_lot(request):
    # Get the search query from the URL parameters
    query = request.GET.get('q', '')
    inventory_bay_lots = InventoryBayLot.objects.filter(
        quantity__gt=0).select_related('inventory_bay__warehouse_name', 'product_lot')

    if query:
        # Filter by Product Lot's lot number, Inventory Bay's name, or Warehouse's name
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
