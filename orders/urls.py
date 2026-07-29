from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/verify/', views.payment_verify_view, name='payment_verify'),
    path('success/', views.success_view, name='success'),
    path('success/<str:order_number>/', views.success_view, name='order_success'),
    path('history/', views.order_history, name='order_history'),
]