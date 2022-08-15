from dataclasses import field
from rest_framework import serializers
from .models import Collection, Product
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField()
    
    def get_price_with_tax(request, product):
        return product.unit_price * Decimal(1.1)
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'inventory', 'last_update', 'unit_price', 'price_with_tax', 'collection']