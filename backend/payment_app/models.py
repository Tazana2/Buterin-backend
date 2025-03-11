from django.db import models
from django.contrib.auth.models import User
from nft_app.models import Nft

class PaymentMethod(models.Model):
    METHOD_TYPES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'Paypal'),
        ('crypto', 'Crypto'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method_type  = models.CharField(max_length=100, choices=METHOD_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)