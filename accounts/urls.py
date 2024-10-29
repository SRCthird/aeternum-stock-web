from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('logout', views.login_view, name='logout'),
    path('register/', views.register_view, name='register')
]
