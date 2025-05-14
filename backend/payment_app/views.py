from rest_framework import viewsets, permissions
from .serializers import PaymentMethodSerializer
from .models import PaymentMethod

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]