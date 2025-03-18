from rest_framework import serializers
from .models import ShoppingCart
from nft_app.serializers import NftSerializer

class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = NftSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'items']
        read_only_fields = ['user']