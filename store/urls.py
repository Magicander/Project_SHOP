from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('html/products/', views.product_list_html, name='product-list-html'),
    path('html/products/<int:id>/', views.product_detail_html, name='product-detail-html'),
    path('html/products/add/', views.product_create_html, name='product-create-html'),
    path('html/products/<int:id>/delete/', views.product_delete_html, name='product-delete-html'),
    path('accounts/login/', LoginView.as_view(template_name='store/registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='product-list-html'), name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    path('cart/', views.cart_detail_view, name='cart-detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add-to-cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove-from-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile_view, name='profile'),
    path('api/reviews/', views.ReviewList.as_view(), name='api-review-list'),
    path('api/reviews/<int:id>/', views.ReviewDetail.as_view(), name='api-review-detail'),
]
