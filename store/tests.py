from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, SIZES, Brand, Category

class ShirtAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpassword')
        self.brand = Brand.objects.create(name="TestBrand", country="PL")
        self.category = Category.objects.create(name="TestCategory")
        self.product = Product.objects.create(
            name="Test T-Shirt",
            price=50.00,
            size=3,        
            colors="B",    
            owner=self.user,
            brand=self.brand,
            category=self.category
        )
        self.url = reverse('shirt-list')

    def test_product_model_str(self):
        product = Product.objects.get(id=self.product.id)
        self.assertIn("Test Product", str(product))

    def test_get_products_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_shirt_unauthorized(self):
        """Próba dodania przez niezalogowanego"""
        data = {
            "name": "Hacker Shirt",
            "price": 10.00,
            "size": 3,     
            "colors": "C",
            "brand": self.brand.id,
            "category": self.category.id
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_authorized(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "New Jacket",
            "price": 120.00,
            "size": 4,
            "colors": "N",
            "brand": self.brand.id,
            "category": self.category.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
