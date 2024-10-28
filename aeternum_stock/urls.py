"""
URL configuration for aeternum_stock project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .settings import SITE_PREFIX

urlpatterns = [
    path(f'{SITE_PREFIX}', include("inventory.urls")),
    path(f'{SITE_PREFIX}accounts/', include('accounts.urls')),
    path(f'{SITE_PREFIX}api/', include('api.urls')),
    path(f'{SITE_PREFIX}admin/', admin.site.urls),
]
