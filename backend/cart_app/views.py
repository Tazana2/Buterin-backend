from abc import ABC, abstractmethod
from io import BytesIO
from datetime import datetime
from django.http import FileResponse
from reportlab.pdfgen import canvas

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer
from nft_app.models import Nft

# Interfaces
class InvoiceGenerator(ABC):
    @abstractmethod
    def generate(self, user, items):
        """Generate a PDF invoice buffer for the given user and items."""
        pass

class CartRepository(ABC):
    @abstractmethod
    def get_or_create_cart(self, user):
        pass

    @abstractmethod
    def clear_cart(self, cart):
        pass

    @abstractmethod
    def delete_items(self, items):
        pass

    @abstractmethod
    def add_item(self, cart, nft):
        pass

    @abstractmethod
    def remove_item(self, cart, nft):
        pass

# Implementations
class PDFInvoiceGenerator(InvoiceGenerator):
    def generate(self, user, items):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Invoice for {user.username}")
        y = 770
        total = 0
        for item in items:
            p.drawString(100, y, f"NFT ID: {item.nft_id}, Name: {item.name}, Price: {item.price}")
            total += item.price
            y -= 20
        p.drawString(100, y - 20, f"Total: {total} ETH")
        p.drawString(100, y - 40, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

class DjangoCartRepository(CartRepository):
    def get_or_create_cart(self, user):
        cart, _ = ShoppingCart.objects.get_or_create(user=user)
        return cart

    def clear_cart(self, cart):
        cart.items.clear()
        cart.save()

    def delete_items(self, items):
        for item in items:
            item.delete()

    def add_item(self, cart, nft):
        cart.items.add(nft)
        cart.save()

    def remove_item(self, cart, nft):
        cart.items.remove(nft)
        cart.save()

# Refactored ViewSet
class ShoppingCartViewSet(viewsets.ViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, *args, invoice_generator: InvoiceGenerator = PDFInvoiceGenerator(), cart_repo: CartRepository = DjangoCartRepository(), **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice_generator = invoice_generator
        self.cart_repo = cart_repo

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cart = self.cart_repo.get_or_create_cart(request.user)
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        cart = self.cart_repo.get_or_create_cart(request.user)
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request, *args, **kwargs):
        nft_id = request.data.get("nft_id")
        if not nft_id:
            return Response({"error": "Must give a NFT id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nft = Nft.objects.get(nft_id=nft_id)
        except Nft.DoesNotExist:
            return Response({"error": "The NFT does not exist"}, status=status.HTTP_404_NOT_FOUND)

        cart = self.cart_repo.get_or_create_cart(request.user)
        self.cart_repo.add_item(cart, nft)
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def remove_item(self, request, *args, **kwargs):
        nft_id = request.data.get("nft_id")
        if not nft_id:
            return Response({"error": "Must give a NFT id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nft = Nft.objects.get(nft_id=nft_id)
        except Nft.DoesNotExist:
            return Response({"error": "The NFT does not exist"}, status=status.HTTP_404_NOT_FOUND)

        cart = self.cart_repo.get_or_create_cart(request.user)
        self.cart_repo.remove_item(cart, nft)
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def checkout(self, request, *args, **kwargs):
        cart = self.cart_repo.get_or_create_cart(request.user)
        items = list(cart.items.all())
        if not items:
            return Response({"error": "No items in the cart"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate invoice using injected generator
        pdf_buffer = self.invoice_generator.generate(request.user, items)

        # Clean up
        self.cart_repo.delete_items(items)
        self.cart_repo.clear_cart(cart)

        return FileResponse(pdf_buffer, as_attachment=True, filename="invoice.pdf")