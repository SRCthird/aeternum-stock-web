from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from .forms import InventoryTransferForm

from .forms import ProductLotForm


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def index(request):
    return render(request, 'home/base.html', {'title': 'Actions'})


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def create_item(request):
    if request.method == "POST":
        form = ProductLotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('transfer'))
    else:
        form = ProductLotForm()
    return render(request, 'home/create_item.html', {
        'title': 'Create Product Lot',
        'form': form
    })


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
def inventory_transfer(request):
    action = request.GET.get('action', 'transfer')
    context = {'title': 'Inventory Transfer' if action ==
               'transfer' else 'Scrap or Release Item', 'action': action}
    return render(request, 'home/transfer.html', context)


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def find_lot(request):
    return "not implimented"
