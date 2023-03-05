from django.contrib import admin
from .models import Category, Product, Order,OrderInfo, OrderItem

# Register your models here.

#Category table admin
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'foodtype', 'typedesc'
        ]

#Product table admin
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'foodcategory', 'foodname', 'foodimg', 'fooddesc', 'price'
        ]
  
#Order table admin
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        'id' ,'user'
        ]

#OrderInfo table admin
@admin.register(OrderInfo)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        'id','orderid', 'date', 'status','total_items_qty'
        ]

#OrderItem table admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'id','order', 'product','quantity'
        ]

