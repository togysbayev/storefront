from dataclasses import field
from rest_framework import serializers
from .models import Collection, Product, Review
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)    
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField()
    
    def get_price_with_tax(request, product):
        return product.unit_price * Decimal(1.1)
    
    class Meta:
        model = Product
        fields = ['id','title', 'description', 'inventory', 'last_update', 
                  'unit_price', 'price_with_tax', 'collection']
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
        