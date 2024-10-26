from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


@login_required(login_url=f'/{settings.SITE_PREFIX}/login')
def index(request):
    response: str = "Hello, test inventory here"
    return HttpResponse(
        response.encode("utf-8")
    )


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('index'))
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect(reverse_lazy('index'))
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
