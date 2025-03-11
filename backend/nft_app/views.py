from rest_framework import viewsets, permissions
from .serializers import NftSerializer
from .models import Nft

class NftViewSet(viewsets.ModelViewSet):
    queryset = Nft.objects.all()
    serializer_class = NftSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]