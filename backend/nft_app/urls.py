from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NftViewSet

router = DefaultRouter()
router.register("api/nfts", NftViewSet)

urlpatterns = router.urls