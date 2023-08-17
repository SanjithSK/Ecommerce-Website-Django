from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserProfileUpdateForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required




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




# profile_update
@login_required(login_url='login')
def update_profile(request):
    profile = request.user.userprofile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Save the form
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
    else:
        form = UserProfileUpdateForm(instance=user_profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'account/profile.html', context)

