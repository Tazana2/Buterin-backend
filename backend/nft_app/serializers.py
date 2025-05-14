from rest_framework import serializers
from .models import Nft

class NftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nft
        fields = '__all__'