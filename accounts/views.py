import json, requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginFormModelForm, RegisterFormModelForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:home")
    if request.POST:
        form = LoginFormModelForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('accounts:home')
    form = LoginFormModelForm()
    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:home")
    if request.POST:
        form = RegisterFormModelForm(request.POST)
        client_key = request.POST['g-recaptcha-response']
        secret_key = 'secret-key-here'
        captcha_data = {
            'secret': secret_key,
            'response': client_key,
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
        response = json.loads(r.text)
        captcha = response['success']

        if captcha and form.is_valid():
            form.save()
            return redirect("accounts:home")
    form = RegisterFormModelForm()
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def home_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    context = {
        'title': 'Home'
    }
    return render(request, 'accounts/home.html', context)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
