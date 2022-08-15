from django.db import models

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
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
    