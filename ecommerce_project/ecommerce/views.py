from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import secrets
from datetime import datetime, timedelta

from .models import Store, Product, Review, Purchase
from .forms import UserRegisterForm, ProductForm, StoreForm, ReviewForm
from ecommerce.utils.twitter_api import tweet_store, tweet_product

# REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .serializers import (
    StoreSerializer,
    StoreDetailSerializer,
    ProductSerializer,
    ReviewSerializer,
)
from .permissions import IsOwnerOrReadOnly


# ----------------------------
# Helper functions
# ----------------------------
def is_vendor(user):
    return user.groups.filter(name="Vendor").exists()

def is_buyer(user):
    return user.groups.filter(name="Buyer").exists()


# ----------------------------
# Authentication
# ----------------------------
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            account_type = form.cleaned_data["account_type"]
            group, _ = Group.objects.get_or_create(name=account_type)
            user.groups.add(group)
            login(request, user)
            # Redirect based on account type
            if account_type == "Vendor":
                return redirect("ecommerce:vendor_dashboard")
            else:
                return redirect("ecommerce:product_list")
    else:
        form = UserRegisterForm()
    return render(request, "ecommerce/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on user role/group
            if user.groups.filter(name="Vendor").exists():
                return redirect("ecommerce:vendor_dashboard")
            else:
                return redirect("ecommerce:product_list")
        messages.error(request, "Invalid username or password")
    return render(request, "ecommerce/login.html")


def user_logout(request):
    logout(request)
    return redirect("ecommerce:login")


# ----------------------------
# Dashboards
# ----------------------------
@login_required
@user_passes_test(is_vendor, login_url="/login/")
def vendor_dashboard(request):
    stores = Store.objects.filter(vendor=request.user)
    products = Product.objects.filter(store__vendor=request.user)
    return render(
        request,
        "ecommerce/vendor_dashboard.html",
        {"stores": stores, "products": products},
    )


@login_required
@user_passes_test(is_buyer, login_url="/login/")
def buyer_dashboard(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, "ecommerce/buyer_dashboard.html", {"purchases": purchases})


# ----------------------------
# Products
# ----------------------------
@login_required
def product_list(request):
    products = Product.objects.select_related("store").all()
    stores = Store.objects.all()
    
    # Check if user is a vendor
    is_vendor = False
    if request.user.is_authenticated:
        is_vendor = request.user.groups.filter(name='Vendor').exists()
    
    return render(
        request,
        "ecommerce/product_list.html",
        {"products": products, "stores": stores, "is_vendor": is_vendor},
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.select_related("user").all()
    return render(
        request,
        "ecommerce/product_detail.html",
        {"product": product, "reviews": reviews},
    )


@login_required
@user_passes_test(is_vendor, login_url="/login/")
def add_product(request):
    store_id = request.GET.get("store")
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = form.cleaned_data["store"]
            product.save()
            tweet_product(product)
            messages.success(request, "Product added successfully!")
            return redirect("ecommerce:vendor_dashboard")
    else:
        form = ProductForm(user=request.user, initial={"store": store_id})

    return render(request, "ecommerce/product_form.html", {"form": form})


# ----------------------------
# Cart
# ----------------------------
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    qty = int(request.POST.get("quantity", 1))
    cart = request.session.get("cart", {})
    cart[str(product.pk)] = cart.get(str(product.pk), 0) + qty
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("ecommerce:view_cart")


@login_required
def view_cart(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            product = Product.objects.get(pk=int(pid))
            subtotal = product.price * qty
            items.append({"product": product, "quantity": qty, "subtotal": subtotal})
            total += subtotal
        except Product.DoesNotExist:
            continue
    return render(request, "ecommerce/cart.html", {"items": items, "total": total})


@login_required
def remove_from_cart(request, pk):
    cart = request.session.get("cart", {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session["cart"] = cart
        request.session.modified = True
    return redirect("ecommerce:view_cart")


@login_required
@user_passes_test(is_buyer, login_url="/login/")
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("ecommerce:view_cart")

    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.objects.get(pk=int(pid))
        if product.stock < qty:
            return HttpResponse(f"Not enough stock for {product.name}", status=400)

        product.stock -= qty
        product.save()
        Purchase.objects.create(user=request.user, product=product, quantity=qty)
        subtotal = product.price * qty
        items.append({"product": product, "quantity": qty, "subtotal": subtotal})
        total += subtotal

    request.session["cart"] = {}
    request.session.modified = True

    # Send invoice email
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    
    invoice_html = render_to_string('ecommerce/invoice.html', {
        'user': request.user,
        'items': items,
        'total': total,
        'date': datetime.now()
    })
    
    send_mail(
        subject='Your Order Invoice',
        message=f'Thank you for your order! Total: ${total}',
        from_email='noreply@ecommerce.com',
        recipient_list=[request.user.email],
        html_message=invoice_html,
        fail_silently=True,
    )

    return render(
        request,
        "ecommerce/checkout.html",
        {"items": items, "total": total, "date": datetime.now()},
    )


# ----------------------------
# Reviews
# ----------------------------
@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.verified = Purchase.objects.filter(
                user=request.user, product=product
            ).exists()
            review.save()
            return redirect("ecommerce:product_detail", pk=pk)
    else:
        form = ReviewForm()
    return render(
        request, "ecommerce/add_review.html", {"form": form, "product": product}
    )


# ----------------------------
# Stores
# ----------------------------
@login_required
@user_passes_test(is_vendor, login_url="/login/")
def create_store(request):
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()
            # tweet_store(store)  # Disabled for now
            return redirect("ecommerce:vendor_dashboard")
    else:
        form = StoreForm()
    return render(request, "ecommerce/store_form.html", {"form": form})


@login_required
@user_passes_test(is_vendor, login_url="/login/")
def delete_store(request, pk):
    store = get_object_or_404(Store, pk=pk, vendor=request.user)
    if request.method == "POST":
        store.delete()
        return redirect("ecommerce:vendor_dashboard")
    return render(
        request, "ecommerce/store_confirm_delete.html", {"store": store}
    )


# ----------------------------
# API ViewSets
# ----------------------------
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsVendorOrReadOnly, IsOwnerOrReadOnly


class StoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint for stores.
    - Anyone can view stores (GET)
    - Only vendors can create/edit/delete their own stores
    """
    queryset = Store.objects.all()
    permission_classes = [IsVendorOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StoreDetailSerializer
        return StoreSerializer
    
    def perform_create(self, serializer):
        """Set the vendor to current user when creating"""
        serializer.save(vendor=self.request.user)
    
    def get_queryset(self):
        """Vendors see only their stores via API, others see all"""
        queryset = Store.objects.all()
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Vendor').exists():
            if self.action in ['list', 'update', 'partial_update', 'destroy']:
                # Vendors see only their own stores for modification
                queryset = queryset.filter(vendor=self.request.user)
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products.
    - Anyone can view products (GET)
    - Only vendors can create/edit/delete their own products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]
    
    def get_queryset(self):
        """Vendors see only products from their stores"""
        queryset = Product.objects.all()
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Vendor').exists():
            if self.action in ['update', 'partial_update', 'destroy']:
                # Vendors can only modify their own products
                queryset = queryset.filter(store__vendor=self.request.user)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for reviews.
    - Anyone can view reviews (GET)
    - Only authenticated buyers can create reviews
    - Users can only edit/delete their own reviews
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        """Set the user to current user when creating review"""
        serializer.save(user=self.request.user)


# ----------------------------
# Password Reset
# ----------------------------
RESET_TOKENS = {}


@csrf_exempt
def send_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            return render(request, "ecommerce/send_reset.html", {"error": "Email is required"})

        user = User.objects.filter(email=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            RESET_TOKENS[token] = {
                "user_id": user.id,
                "expires": datetime.now() + timedelta(hours=1),
            }
            reset_link = request.build_absolute_uri(f"/reset-password/{token}/")

            send_mail(
                subject="Password Reset Request",
                message=f"Hello {user.username},\n\nClick the link to reset your password:\n{reset_link}\n\nThis link expires in 1 hour.",
                from_email=settings.DEFAULT_FROM_EMAIL or "no-reply@example.com",
                recipient_list=[email],
                fail_silently=False,
            )
        
        # Always show success message (don't reveal if user exists)
        return render(request, "ecommerce/send_reset.html", {"sent": True})
    return render(request, "ecommerce/send_reset.html")


@csrf_exempt
def reset_password(request, token):
    token_data = RESET_TOKENS.get(token)
    if not token_data or datetime.now() > token_data["expires"]:
        return HttpResponse("Invalid or expired token", status=400)

    if request.method == "POST":
        password = request.POST.get("password")
        if not password:
            return JsonResponse({"error": "Password is required"}, status=400)
        user = get_object_or_404(User, id=token_data["user_id"])
        user.set_password(password)
        user.save()
        del RESET_TOKENS[token]
        return JsonResponse({"message": "Password reset successfully"})

    return render(
        request,
        "ecommerce/password_reset_confirm.html",
        {"token": token},
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Store, Product
from .forms import StoreForm, ProductForm




@login_required
def edit_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('ecommerce:store_detail', store_id=store.id)
    else:
        form = StoreForm(instance=store)
    return render(request, 'ecommerce/edit_store.html', {'form': form, 'store': store})


@login_required
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    return render(request, 'ecommerce/store_detail.html', {
        'store': store,
        'products': products
    })


@login_required
def add_product_to_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('ecommerce:store_detail', store_id=store.id)
    else:
        form = ProductForm()
    return render(request, 'ecommerce/add_product.html', {'form': form, 'store': store})


@login_required
@user_passes_test(is_vendor, login_url="/login/")
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, store__vendor=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("ecommerce:vendor_dashboard")
    else:
        form = ProductForm(instance=product)
    return render(request, "ecommerce/product_form.html", {"form": form, "product": product})


@login_required
@user_passes_test(is_vendor, login_url="/login/")
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, store__vendor=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("ecommerce:vendor_dashboard")
    return render(request, "ecommerce/product_confirm_delete.html", {"product": product})
