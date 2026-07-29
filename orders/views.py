import hashlib
import hmac
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from cart.views import get_cart, save_cart
from products.models import Product
from .models import Order

try:
    import razorpay
except Exception:
    razorpay = None


RAZORPAY_KEY_ID = getattr(settings, 'RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = getattr(settings, 'RAZORPAY_KEY_SECRET', '')

razorpay_client = None
if razorpay and RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    try:
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    except Exception:
        razorpay_client = None


def checkout_view(request):
    cart = get_cart(request)
    items = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address_line = request.POST.get('address_line', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'COD')

        if not all([full_name, phone, address_line, city, state, pincode]):
            return render(request, 'orders/checkout.html', {
                'items': items,
                'total': total,
                'error': 'Please fill all address fields.'
            })

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode,
            total_amount=total,
            payment_method=payment_method,
            payment_status='PENDING',
            status='Placed'
        )

        if payment_method == 'ONLINE':
            if razorpay_client is None:
                return render(request, 'orders/payment_failed.html', {
                    'order': order,
                    'message': 'Razorpay is not configured yet. Add your keys in settings.py.'
                })

            amount_in_paise = int(total * 100)

            razorpay_order = razorpay_client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": f"order_{order.order_number}",
                "payment_capture": 1
            })

            order.razorpay_order_id = razorpay_order['id']
            order.save()

            return render(request, 'orders/payment.html', {
                'order': order,
                'razorpay_key_id': RAZORPAY_KEY_ID,
                'razorpay_order_id': razorpay_order['id'],
                'amount': amount_in_paise,
            })

        # COD
        save_cart(request, {})
        return render(request, 'orders/order_success.html', {'order': order})

    return render(request, 'orders/checkout.html', {'items': items, 'total': total})


def payment_verify_view(request):
    if request.method != 'POST':
        return redirect('checkout')

    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)

    generated_signature = hmac.new(
        RAZORPAY_KEY_SECRET.encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    if generated_signature == razorpay_signature:
        order.razorpay_payment_id = razorpay_payment_id
        order.payment_status = 'PAID'
        order.status = 'Placed'
        order.save()

        save_cart(request, {})
        return render(request, 'orders/order_success.html', {'order': order})

    order.payment_status = 'FAILED'
    order.save()
    return render(request, 'orders/payment_failed.html', {
        'order': order,
        'message': 'Payment signature verification failed.'
    })


def success_view(request, order_number=None):
    order = None
    if order_number:
        order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_success.html', {'order': order})


def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        orders = Order.objects.none()

    return render(request, 'orders/order_history.html', {'orders': orders})