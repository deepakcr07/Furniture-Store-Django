from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.filter(is_featured=True).order_by('-created_at')[:4]
    return render(request, 'home.html', {'products': products})