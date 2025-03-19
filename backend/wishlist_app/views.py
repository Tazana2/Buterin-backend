from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import WishlistSerializer
from nft_app.models import Nft
from .models import Wishlist

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        cart, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        nft_id = request.data.get("nft_id")
        
        if not nft_id:
            return Response({"error": "Must give a NFT id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nft = Nft.objects.get(nft_id=nft_id)
        except Nft.DoesNotExist:
            return Response({"error": "The NFT does not exists"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Wishlist.objects.get_or_create(user=request.user)
        cart.wishlist_items.add(nft)
        cart.save()
        
        return Response(WishlistSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def remove_item(self, request):
        nft_id = request.data.get("nft_id")

        if not nft_id:
            return Response({"error": "Must give a NFT id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nft = Nft.objects.get(nft_id=nft_id)
        except Nft.DoesNotExist:
            return Response({"error": "The NFT does not exists"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Wishlist.objects.get_or_create(user=request.user)
        cart.wishlist_items.remove(nft)
        cart.save()
        
        return Response(WishlistSerializer(cart).data, status=status.HTTP_200_OK)