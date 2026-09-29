from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms


# ---------- Custom Registration Form ----------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose a username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('username', 'email')


# ---------- Register View ----------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect('dashboard:home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# ---------- Login View ----------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard:home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    # form fields এ Bootstrap class add করা
    form.fields['username'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Username'
    })
    form.fields['password'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Password'
    })

    return render(request, 'accounts/login.html', {'form': form})


# ---------- Logout View ----------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


# ---------- Profile View (Login required) ----------
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})