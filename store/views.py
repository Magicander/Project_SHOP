from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions, status
from .forms import ProductForm 
from .models import Product, Category, Brand, Cart, CartItem
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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

    return render(request, 'store/product-list.html', {'products': products})

def product_detail_html(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'store/product-detail.html', {'product': product})

def product_create_html(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if request.user.is_authenticated:
                product.owner = request.user
                product.save()
                return redirect('product-list-html')
            else:
                pass 
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
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart-detail')

@login_required
def remove_from_cart_view(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('cart-detail')

@login_required
def cart_detail_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    return render(request, 'store/cart/detail.html', {'cart': cart})