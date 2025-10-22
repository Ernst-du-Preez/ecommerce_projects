from rest_framework import serializers
from .models import Store, Product, Review

# Compact Store serializer with vendor username
class StoreSerializer(serializers.ModelSerializer):
    vendor = serializers.ReadOnlyField(source="vendor.username")

    class Meta:
        model = Store
        fields = ["id", "name", "description", "vendor"]


# Full Store serializer with all fields
class StoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "store", "image"]


# Review serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ["id", "product", "user", "text", "verified", "created_at"]
