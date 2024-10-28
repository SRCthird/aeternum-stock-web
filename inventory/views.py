from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

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


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def transfer(request):
    action = request.GET.get('action', 'transfer')
    context = {'title': 'Inventory Transfer' if action ==
               'transfer' else 'Scrap or Release Item', 'action': action}
    return render(request, 'home/transfer.html', context)


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def find_lot(request):
    return "not implimented"
