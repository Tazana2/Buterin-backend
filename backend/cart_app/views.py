from rest_framework import viewsets, permissions
from .serializers import ShoppingCartSerializer
from .models import ShoppingCart

class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Only show the user's own shopping carts
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)