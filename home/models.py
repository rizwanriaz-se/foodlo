from django.db import models
from django.contrib.auth.models import User

STATE = (
    ("Sd", "Sindh"),
    ("Pjb", "Punjab"),
    ("Bal", "Balochistan"),
    ("Kp", "Khyber PakhtunKhwa"),
)

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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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


class UserInfo(models.Model):
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip = models.IntegerField()
    phone = models.CharField(max_length=16)
    email = models.EmailField()
