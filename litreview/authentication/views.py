from django.shortcuts import render
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages


def login_page(request):
    form = forms.LoginForm()

    # Supprimer les anciens messages pour éviter les doublons après une redirection
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie.')
                return redirect('flux')
            else:
                messages.error(request, 'Identifiants invalides.')

    return render(request, 'authentication/login.html', {'form': form})


def logout_user(request):

    logout(request)
    messages.success(request, 'Déconnexion réussie.')
    return redirect('login')


def signup_page(request):

    form = forms.SignupForm()

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'authentication/signup.html', context={'form': form})
