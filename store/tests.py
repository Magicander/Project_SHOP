from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Product, Brand, Category, Review, Cart, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile

class ProductAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpassword')
        self.brand = Brand.objects.create(name="TestBrand", country="PL")
        self.category = Category.objects.create(name="TestCategory")
        self.product = Product.objects.create(
            name="Test T-Shirt",
            price=50.00,
            size=3,        
            colors="B",    
            stock_count=10,
            owner=self.user,
            brand=self.brand,
            category=self.category
        )
        self.url = reverse('product-list')

    def test_product_model_str(self):
        """Sprawdza czy stringowa reprezentacja produktu jest poprawna"""
        product = Product.objects.get(id=self.product.id)
        self.assertIn("Test T-Shirt", str(product))

    def test_get_products_list(self):
        """Sprawdza czy API zwraca listę produktów"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_shirt_unauthorized(self):
        """Próba dodania przez niezalogowanego - oczekiwane 403 Forbidden"""
        data = {
            "name": "Hacker Shirt",
            "price": 10.00,
            "size": "M",     
            "colors": "R",
            "stock_count": 5,
            "brand": self.brand.id,
            "category": self.category.id
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_authorized(self):
        self.client.force_authenticate(user=self.user)
        
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )

        data = {
            "name": "New Jacket",
            "price": 120.00,
            "size": "M",
            "colors": "B",
            "stock_count": 100,
            "brand": self.brand.id,
            "category": self.category.id,
            "image": image
        }
        
        response = self.client.post(self.url, data, format='multipart')
        
        if response.status_code != 201:
            print(f"\nBŁĄD API: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reviewer', password='password')
        self.brand = Brand.objects.create(name="BrandX")
        self.category = Category.objects.create(name="CatX")
        self.product = Product.objects.create(
            name="Super Produkt", 
            price=100, 
            owner=self.user,
            brand=self.brand,
            category=self.category
        )
    def test_create_review(self):
        """Sprawdza czy można dodać opinię"""
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            content="Świetny sprzęt!"
        )
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(str(review), f"reviewer - Super Produkt (5/5)")
    
class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='password')
        self.brand = Brand.objects.create(name="BrandY")
        self.category = Category.objects.create(name="CatY")
        self.p1 = Product.objects.create(name="P1", price=100.00, owner=self.user, brand=self.brand, category=self.category)
        self.p2 = Product.objects.create(name="P2", price=50.00, owner=self.user, brand=self.brand, category=self.category)
        self.cart = Cart.objects.create(user=self.user)
    def test_cart_total_price(self):
        """Sprawdza czy koszyk dobrze liczy sumę"""
        CartItem.objects.create(cart=self.cart, product=self.p1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.p2, quantity=1)
        self.assertEqual(self.cart.get_total_cart_price(), 250.00)
