from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Replace 'home' with your desired home page URL
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')
