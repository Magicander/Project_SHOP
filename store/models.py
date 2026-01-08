import uuid
from django.db import models
from django.contrib.auth.models import User

GENDER = (
    ('K', 'Kobieta'),
    ('M', 'Mężczyzna'),
    ('N', 'Nijaki'),
)

SIZES = (
    #T-shirt i kurtiki, 
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    #Skarpetki
    ('35-38', '35-38'),
    ('39-42', '39-42'),
    ('43-46', '43-46'),
    #Spodnie
    ('30', '30'),
    ('32', '32'),
    ('34', '34'),
    ('36', '36'),
)

FABRIC_TYPES = (
    ('C', 'Bawełna (Cotton)'),
    ('P', 'Poliester'),
    ('L', 'Len'),
    ('S', 'Jedwab (Silk)'),
    ('W', 'Wełna (Wool)'),
    ('J', 'Jeans (Denim)'),
    ('K', 'Skóra (Leather)'),
    ('E', 'Elastan (Elastane)'),
)

COLORS = (
    ('C', 'Czarny'),
    ('B', 'Biały'),
    ('N', 'Niebieski'),
    ('Z', 'Zielony'),
    ('R', 'Czerwony'),
    ('G', 'Szary'),
)


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, help_text="Krótki opis kategorii.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Model reprezentujący producenta ubrania"""
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=2, help_text="Kod kraju producenta, np. PL, IT, FR")
    

    def __str__(self):
        return self.name


class Product(models.Model):
    """Model reprezentujący koszulkę w sklepie."""
    name = models.CharField(max_length=50)
    sku = models.CharField(max_length=30, unique=True, db_index=True, blank=True )
    description = models.TextField(blank=True, help_text="Opis Produktu")
    gender = models.CharField(max_length=1, choices=GENDER, default='N')
    size = models.CharField(max_length=10, choices=SIZES, default='M')
    fabric = models.CharField(max_length=1, choices=FABRIC_TYPES, default='C')
    colors = models.CharField(max_length=1, choices=COLORS, default='B')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    stock_count = models.PositiveIntegerField(default=1, help_text="Ilość sztuk w magazynie.")
    sale = models.BooleanField(default=False, help_text="Czy produkt jest na wyprzedaży?")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cena w PLN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)    

    def save(self, *args, **kwargs):
        if not self.sku:
            safe_size = str(self.size).replace("-", "")
            base_code = f"{self.gender}-{self.fabric}-{self.colors}-{self.size}"
            random_suffix = str(uuid.uuid4())[:8].upper()
            self.sku = f"{base_code}-{random_suffix}"
        if self.price < 0:
            raise ValueError("Nie moze być ujemna")
        if self.sku:
            self.sku = self.sku.upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.sku}] {self.name} ({self.get_size_display()})"
    
    class Meta:
        ordering = ['-created_at']

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Koszyk użytkownika: {self.user.username}"
    
    def get_total_cart_price(self):
        total = 0
        for item in self.cart_items.all():
            total += item.get_total_price()
        return total
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total_price(self):
        return self.product.price * self.quantity