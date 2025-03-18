from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShoppingCartViewSet

router = DefaultRouter()
router.register("cart", ShoppingCartViewSet, basename="shopping_cart")  # Se accede como /api/cart/

urlpatterns = [
    path("api/", include(router.urls)),  # Incluir todas las rutas del ViewSet
]