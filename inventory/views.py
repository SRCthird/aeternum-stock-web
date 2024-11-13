from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse
from django.template.response import TemplateResponse
import datetime
import pytz

from .models import InventoryBay, InventoryBayLot, InventoryTransfer, Product, ProductLot
from .forms import ProductLotForm, InventoryTransferForm


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def index(request, transaction_id=0):
    response = TemplateResponse(
        request,
        'home/base.html',
        {
            'title': 'Actions',
            'transaction_id': transaction_id
        }
    )

    def callback(response):
        request.session['print_prompt'] = False

    response.add_post_render_callback(callback)
    return response


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def create_item(request):
    if request.method == "POST":
        form = ProductLotForm(request.POST)
        if form.is_valid():
            # Retrieve the comment from the form data
            comment = form.cleaned_data.get('comment')

            # Set the history change reason for ProductLot
            new_product_lot = form.save(commit=False)
            new_product_lot._change_reason = comment
            new_product_lot.save()

            starting_bay = get_object_or_404(InventoryBay, name="Production")

            # Set the history change reason for InventoryBayLot
            inventory_bay_lot = InventoryBayLot(
                inventory_bay=starting_bay,
                product_lot=new_product_lot,
                quantity=new_product_lot.quantity
            )
            inventory_bay_lot._change_reason = comment
            inventory_bay_lot.save()

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
    elif action == 'scrap':
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
                transaction = form.save(commit=False)
                transaction._change_reason = transaction.comments
                transaction.save()
                # request.session['print_prompt'] = True
                if request.session.get('print_list'):
                    request.session['print_list'] = f'{
                        request.session.get("print_list")},{transaction.id}'
                    print(request.session.get('print_list'))
                else:
                    request.session['print_list'] = transaction.id
                return redirect(reverse('index'))
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
    inventory_bay_lots = InventoryBayLot.objects \
        .filter(
            quantity__gt=0
        ) \
        .select_related(
            'inventory_bay__warehouse_name',
            'product_lot',
            'product_lot__product_name'
        )

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


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def print_transaction(request):
    def get_est_datetime_now():
        """Gets the current datetime in EST and formats it as 'dd-mmm-yy hh:mm'."""
        est_timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(est_timezone)
        return now.strftime('%d-%b-%y %H:%M')

    action = request.GET.get('action', None)
    transaction_ids: str = f'{request.session.get("print_list")}'
    transactions = []

    if transaction_ids is not None:
        if "," in transaction_ids:
            ids = transaction_ids.split(',')
        else:
            ids = [transaction_ids]
        for id in ids:
            transaction = get_object_or_404(InventoryTransfer, id=id)
            transactions.append({
                'transaction': transaction,
                'product': get_object_or_404(
                    Product, id=transaction.product_lot.product_name_id)
            })

    response = TemplateResponse(
        request,
        'home/print_transaction.html',
        {
            'transactions': transactions,
            'datetime': get_est_datetime_now()
        }
    )

    def callback(response):
        if action is None:
            request.session.pop('print_list', None)

    response.add_post_render_callback(callback)
    return response


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def empty_print(request):
    request.session.pop('print_list', None)
    return redirect(reverse('index'))
