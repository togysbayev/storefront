from math import prod
from msilib.schema import CustomAction
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from .models import Collection, Product


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))
    

class InventoryFilter(SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<60', 'Low'),
            ('>=60', 'Ok')
        ]
        
    def queryset(self, request, queryset):
        if self.value() == '<60':
            return Product.objects.filter(inventory__lt=60)
        elif self.value() == '>=60':
            return Product.objects.filter(inventory__gte=60)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    actions = ['clear_inventory', 'change_unit_price_to_default']
    list_display = ['title', 'description', 'unit_price', 'inventory_status', 'inventory', 'collection']
    ordering = ['unit_price']
    list_editable = ['unit_price']
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title__istartswith', 'description__istartswith']
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 60:
            return 'Low'
        return 'Ok'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were updated',
            messages
            .INFO
        )
        
        
        
    @admin.action(description='Change unit_price to default value')
    def change_unit_price_to_default(self, request, queryset):
        updated_count = queryset.update(unit_price=100.00)
        self.message_user(
            request,
            f'Unit-prices of {updated_count} products were successfully updated', 
            messages.ERROR
        )
        