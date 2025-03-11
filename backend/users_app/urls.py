from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers
from .views import RegisterViewSet
from django.urls import path

router = routers.DefaultRouter()
router.register("api/auth/register", RegisterViewSet, "register")

urlpatterns = router.urls + [
    path("api/auth/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/login/verify", TokenVerifyView.as_view(), name="token_verify"),
]