from django.db import models

class Nft(models.Model):
    nft_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    rarible_url = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)

    def __str__(self):
        return self.name