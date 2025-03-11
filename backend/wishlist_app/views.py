from rest_framework import viewsets, permissions
from .serializers import WishlistSerializer
from .models import Wishlist

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Only show the user's own wishlists
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)