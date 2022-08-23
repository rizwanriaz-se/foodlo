from django.contrib import admin
from .models import Category, Product, Order,OrderInfo, Cart,CartInfo

# Register your models here.
"""
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
  list_display=['id','user','name','address']
"""


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'foodtype', 'typedesc']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'foodcategory', 'foodname', 'foodimg', 'fooddesc', 'price'
    ]
  
"""
@admin.register(OrderDetails)
class OrderDetailsModelAdmin(admin.ModelAdmin):
    list_display = ['orderid', 'foodid', 'quantity']
"""


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(CartInfo)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'items', 'quantity']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'cartid','user']



@admin.register(OrderInfo)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id','orderid','user', 'date', 'status']

