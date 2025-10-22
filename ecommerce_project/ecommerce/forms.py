# ecommerce/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Store, Review


# ----------------------------
# User Registration
# ----------------------------
class UserRegisterForm(UserCreationForm):
    ACCOUNT_TYPE_CHOICES = (
        ('Vendor', 'Vendor'),
        ('Buyer', 'Buyer')
    )
    email = forms.EmailField()
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'account_type']


# ----------------------------
# Product Form
# ----------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['store', 'name', 'description', 'price', 'stock', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass user from view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['store'].queryset = Store.objects.filter(vendor=user)


# ----------------------------
# Store Form
# ----------------------------
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'logo']


# ----------------------------
# Review Form
# ----------------------------
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']

class UserRegisterForm(UserCreationForm):
    ACCOUNT_TYPE_CHOICES = (
        ('Vendor', 'Vendor'),
        ('Buyer', 'Buyer')
    )
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    account_type = forms.ChoiceField(label="Account Type", choices=ACCOUNT_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'account_type']