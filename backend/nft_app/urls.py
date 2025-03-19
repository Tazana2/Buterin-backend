from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NftViewSet, NftWalletView

router = DefaultRouter()
router.register("api/nfts", NftViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/nfts2/", NftWalletView.as_view(), name="nfts2")
]