from django.db import models
from django.contrib.auth.models import User

STATE = (
    ("Sd", "Sindh"),
    ("Pjb", "Punjab"),
    ("Bal", "Balochistan"),
    ("Kp", "Khyber PakhtunKhwa"),
)
"""
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    address = models.CharField(choices=STATE, max_length=64)

    def __str__(self):
        return self.user
"""

CATEGORY_CHOICE = (
    ("Pizza", "Pizza"),
    ("Pasta", "Pasta"),
    ("Milk Shake", "Milk Shake"),
)


class Category(models.Model):

    foodtype = models.CharField(choices=CATEGORY_CHOICE, max_length=64)
    typedesc = models.CharField(max_length=64)

    def __str__(self):
        return self.foodtype


class Product(models.Model):
    foodcategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    foodname = models.CharField(max_length=64)
    foodimg = models.ImageField()
    fooddesc = models.TextField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.foodname


STATUS_CHOICE = (
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On the way", "On the way"),
    ("Delivered", "Delivered"),
    ("Cancel", "Cancel"),
)

#def __str__(self):
# return self.user + str(self.date)
"""
class OrderDetails(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    foodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
      return str(self.orderid)
"""

"""
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartInfo(models.Model):
    cartid = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.items.foodname
"""

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    cartid = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class OrderInfo(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE,
                              default="Pending",
                              max_length=30)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    #cartid=models.ForeignKey(Cart,on_delete=models.CASCADE)


class UserInfo(models.Model):
    #  user = models.ForeignKey(User, on_delete=models.CASCADE,default="1")
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip = models.IntegerField()
    phone = models.CharField(max_length=16)
    email = models.EmailField()
