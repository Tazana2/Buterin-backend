from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

class CartViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

    def test_get_cart_unauthorized(self):
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_get_cart_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': 1, 'user': 'testuser', 'items': []})