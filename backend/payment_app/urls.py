from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet

router = DefaultRouter()
router.register("api/payments", PaymentMethodViewSet)  # Endpoint: /api/payments/

urlpatterns = router.urls