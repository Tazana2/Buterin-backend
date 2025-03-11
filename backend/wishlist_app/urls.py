from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet

router = DefaultRouter()
router.register("api/wishlist", WishlistViewSet)  # Endpoint: /api/wishlist/

urlpatterns = router.urls
