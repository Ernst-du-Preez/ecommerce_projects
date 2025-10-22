from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "ecommerce"

# ----------------------------
# API router
# ----------------------------
router = routers.DefaultRouter()
router.register(r"stores", views.StoreViewSet, basename="store")
router.register(r"products", views.ProductViewSet, basename="product")
router.register(r"reviews", views.ReviewViewSet, basename="review")

# ----------------------------
# URL patterns
# ----------------------------
urlpatterns = [
    # API endpoints
    path("api/", include(router.urls)),
    path("api/v1/", include(router.urls)),   # optional legacy prefix

    # User authentication
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Dashboards
    path("vendor-dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path("buyer-dashboard/", views.buyer_dashboard, name="buyer_dashboard"),

    # Products
    path("", views.product_list, name="product_list"),  # homepage → product list
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/<int:pk>/edit/", views.edit_product, name="edit_product"),
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),

    # Cart
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),

    # Checkout
    path("checkout/", views.checkout, name="checkout"),

    # Reviews
    path("products/<int:pk>/review/", views.add_review, name="add_review"),

    # Stores
    path("stores/create/", views.create_store, name="create_store"),
    path("stores/<int:pk>/delete/", views.delete_store, name="delete_store"),

    # Password reset
    path("send-password-reset/", views.send_password_reset, name="send_password_reset"),
    path("reset-password/<str:token>/", views.reset_password, name="reset_password"),
    
    # Additional store paths
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('store/<int:store_id>/edit/', views.edit_store, name='edit_store'),
    path('store/<int:store_id>/add_product/', views.add_product_to_store, name='add_product_to_store'),
]
