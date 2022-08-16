from typing import Collection
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from .models import Product, Collection
from .serializers import CollectionSerializer, ProductSerializer
from store import serializers

class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
        
class CollectionDetail(APIView):
    def get(self, request, id):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    def put(self, request, id):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=id)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=id)
        if collection.products_count > 0:
            return Response({'Error: Collection can not be deleted!'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
