from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ShoppingCart
from .serializers import ShoppingCartSerializer
from nft_app.models import Nft

class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """ En lugar de devolver una lista, devuelve solo el carrito del usuario autenticado. """
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)  # Devuelve solo el objeto sin lista []

    def retrieve(self, request, *args, **kwargs):
        """ Devuelve el carrito del usuario autenticado o lo crea si no existe. """
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        """ Agrega un NFT al carrito sin borrar los anteriores. """
        nft_id = request.data.get("nft_id")
        
        if not nft_id:
            return Response({"error": "Debe proporcionar un ID de NFT"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nft = Nft.objects.get(nft_id=nft_id)
        except Nft.DoesNotExist:
            return Response({"error": "El NFT no existe"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        cart.items.add(nft)
        cart.save()
        
        return Response(ShoppingCartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def remove_item(self, request):
        """ Elimina un NFT del carrito. """
        nft_id = request.data.get("nft_id")

        if not nft_id:
            return Response({"error": "Debe proporcionar un ID de NFT"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nft = Nft.objects.get(nft_id=nft_id)
        except Nft.DoesNotExist:
            return Response({"error": "El NFT no existe"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        cart.items.remove(nft)
        cart.save()
        
        return Response(ShoppingCartSerializer(cart).data, status=status.HTTP_200_OK)