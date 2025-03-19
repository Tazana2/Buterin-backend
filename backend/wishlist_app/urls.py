from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import WishlistViewSet

router = DefaultRouter()
router.register("wishlist", WishlistViewSet, basename="wishlist")

urlpatterns = [
    path("api/", include(router.urls)),
]