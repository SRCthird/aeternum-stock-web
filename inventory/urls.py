from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin/', admin.site.urls),
]
