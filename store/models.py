import uuid
from django.db import models
from django.core.validators import MinValueValidator

class Collection(models.Model):
    title = models.CharField(max_length=200)
        
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
    

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    inventory = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # def __str__(self) -> str:
    #     return self.title
    
    class Meta:
        ordering = ['title']

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=200)
    description = models.TextField()
    last_update = models.DateTimeField(auto_now_add=True)
    
    
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        unique_together = [['cart', 'product']]
