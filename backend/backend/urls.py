from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")), # Django REST framework provides a set of built-in views for handling basic actions such as listing, creating, and deleting objects.
    path("", include("users_app.urls")),  # Rutas de autenticación (usuarios)
    path("", include("nft_app.urls")),  # NFTs
    path("", include("cart_app.urls")),  # Carrito de compras
    path("", include("wishlist_app.urls")),  # Lista de deseos
    path("", include("payment_app.urls")),  # Métodos de pago
    path("", include('learnify_app.urls')), # Cursos externos
]
