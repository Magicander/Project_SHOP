from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions, status
from .forms import ProductForm, ReviewForm
from .models import Product, Category, Brand, Cart, CartItem, Review
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = ProductPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Product.objects.all()
        name_param = self.request.query_params.get('name', None)
        if name_param:
            queryset = queryset.filter(name__icontains=name_param)
        return queryset
    
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

def welcome_view(request):
    return render(request, 'store/welcome.html')

def product_list_html(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/product-list.html', {'products': page_obj})

def product_detail_html(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ReviewForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product-detail-html', id=id)
        else:
            form = ReviewForm()
    reviews = product.reviews.all().order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating
    }
    return render(request, 'store/product-detail.html', context)

@login_required
def product_create_html(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('product-list-html')
    else:
        form = ProductForm()

    return render(request, 'store/product-form.html', {'form': form})

def product_delete_html(request, id):
    product = get_object_or_404(Product, pk=id) 
    
    if request.method == 'POST':
        if request.user == product.owner:
            product.delete()
        return redirect('product-list-html')
    
    return render(request, 'store/product-confirm-delete.html', {'product': product})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product-list-html')
    else:
        form = UserCreationForm()
    
    return render(request, 'store/registration/register.html', {'form': form})

@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock_count <= 0:
        messages.warning(request, "Brak produktu na stanie")
        return redirect('product-list-html')
    cart, created = Cart.objects.get_or_create(user=request.user, is_ordered=False)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart-detail')

@login_required
def remove_from_cart_view(request, item_id):
    cart = get_object_or_404(Cart, user=request.user, is_ordered=False)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('cart-detail')

@login_required
def cart_detail_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_ordered=False)
    return render(request, 'store/cart/detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user, is_ordered=False).first()
    if not cart:
        return redirect('product-list-html')
    items = cart.cart_items.all()
    for item in items:
        if item.product.stock_count < item.quantity:
            messages.error(request, f"Niestety, produkt {item.product.name} jest już niedostępny w tej ilości.")
            return redirect('cart-detail')
    for item in items:
        item.product.stock_count -= item.quantity
        item.product.save()
        
    if cart:
        cart.is_ordered = True
        cart.ordered_at = timezone.now()
        cart.save()
        Cart.objects.create(user=request.user, is_ordered=False)
    return redirect('product-list-html')

@login_required
def profile_view(request):
    orders = Cart.objects.filter(user=request.user, is_ordered=True).prefetch_related('cart_items__product').order_by('-ordered_at')
    reviews = Review.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    context = {
        'orders': orders,
        'reviews': reviews,
    }
    return render(request, 'store/profile.html', context)