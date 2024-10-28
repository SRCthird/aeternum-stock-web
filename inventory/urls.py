from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_item/', views.create_item, name='create_item'),
    path('transfer/', views.transfer, name='transfer'),
    path('find_lot/', views.find_lot, name='find_lot'),
]
