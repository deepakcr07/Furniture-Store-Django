from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'full_name',
        'phone',
        'total_amount',
        'payment_method',
        'payment_status',
        'status',
        'created_at',
    )
    list_filter = ('payment_method', 'payment_status', 'status')
    search_fields = ('order_number', 'full_name', 'phone')