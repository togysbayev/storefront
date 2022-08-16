from ast import Delete
from typing import Collection
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from .models import Product, Collection
from .serializers import CollectionSerializer, ProductSerializer
from store import serializers


class ProductView(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CollectionView(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer


class CollectionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products_count > 0:
            return Response({'Error: Collection can not be deleted!'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

        
