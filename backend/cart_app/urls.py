from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import ShoppingCartViewSet

router = DefaultRouter()
router.register("cart", ShoppingCartViewSet, basename="shopping_cart")

urlpatterns = [
    path("api/", include(router.urls)),
]