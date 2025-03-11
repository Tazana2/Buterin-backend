from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShoppingCartViewSet

router = DefaultRouter()
router.register("api/cart", ShoppingCartViewSet)  # Endpoint: /api/cart/

urlpatterns = router.urls