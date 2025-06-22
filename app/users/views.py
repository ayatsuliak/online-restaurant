from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    CustomUserUpdateForm,
)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu:menu_list')
        else:
            messages.error(request, "Please correct the registration form.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu:menu_list')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST,
                                    instance=request.user,
                                    user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserUpdateForm(instance=request.user, user=request.user)

    return render(request, 'users/profile.html', {'form': form})
