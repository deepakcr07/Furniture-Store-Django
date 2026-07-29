from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AddressForm
from .models import Address

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def account_view(request):
    from orders.models import Order
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/account.html', {
        'addresses': addresses,
        'orders': orders,
    })

@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('account')
    else:
        form = AddressForm()
    return render(request, 'accounts/add_address.html', {'form': form})

@login_required
def delete_address_view(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    return redirect('account')

@login_required
def set_default_address_view(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    Address.objects.filter(user=request.user).update(is_default=False)
    address.is_default = True
    address.save()
    return redirect('account')