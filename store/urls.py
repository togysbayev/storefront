from django.urls import path
from . import views

urlpatterns = [
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:id>/', views.ProductDetail.as_view()),
    path('products/', views.ProductView.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    path('collections/', views.CollectionView.as_view()),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view())
]