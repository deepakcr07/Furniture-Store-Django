from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    order_number = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='COD')
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=20, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"FS{timezone.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number