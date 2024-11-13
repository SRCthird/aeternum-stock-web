from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:transaction_id>', views.index, name='index'),
    path('create_item/', views.create_item, name='create_item'),
    path('transfer/', views.transfer, name='transfer'),
    path('find_lot/', views.find_lot, name='find_lot'),
    path('print_transaction',
         views.print_transaction, name='print_transaction'),
    path('empty_print', views.empty_print, name='empty_print')
]
