from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


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

    return render(request, 'registration/register.html', {'form': form})