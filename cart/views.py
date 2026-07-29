from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


def get_cart(request):
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def cart_view(request):
    cart = get_cart(request)
    items = []
    total = 0
    invalid_products = []

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            invalid_products.append(product_id)

    for product_id in invalid_products:
        del cart[product_id]

    save_cart(request, cart)

    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total
    })


def add_to_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    save_cart(request, cart)
    return redirect('view_cart')


def increase_qty(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
        save_cart(request, cart)

    return redirect('view_cart')


def decrease_qty(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]
        save_cart(request, cart)

    return redirect('view_cart')


def remove_item(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        save_cart(request, cart)

    return redirect('view_cart')


def clear_cart(request):
    save_cart(request, {})
    return redirect('view_cart')