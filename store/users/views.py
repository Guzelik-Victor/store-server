from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Подзравляем! Вы успешно зарегистрировались.'
            )
            return redirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            form.save()
            return redirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Store - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user)

    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))
