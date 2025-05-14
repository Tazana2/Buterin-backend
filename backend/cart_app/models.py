from django.db import models
from django.contrib.auth.models import User
from nft_app.models import Nft

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Nft, blank=True)