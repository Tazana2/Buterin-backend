from rest_framework import viewsets, permissions
from .serializers import RegisterSerializer
from django.contrib.auth.models import User

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]