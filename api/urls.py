from django.urls import path

from . import views

urlpatterns = [
    path('inventory_bays/<int:product_lot_id>/',
         views.get_inventory_bays_for_lot, name='get_inventory_bays_for_lot'),
    path('product-search/', views.product_search, name='product_search'),
    path('to-inventory-bay-search/',
         views.to_inventory_bay_search, name='to_inventory_bay_search'),
    path('product-lot-search/',
         views.product_lot_search, name='product_lot_search'),
]
