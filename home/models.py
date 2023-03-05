from django.db import models
from django.contrib.auth.models import User

#Categories available
CATEGORY_CHOICE = (
    ("Pizza", "Pizza"),
    ("Pasta", "Pasta"),
    ("Milk Shake", "Milk Shake"),
)

#Foods Category table
class Category(models.Model):
    foodtype = models.CharField(choices=CATEGORY_CHOICE, max_length=64)
    typedesc = models.CharField(max_length=200)

    def __str__(self):
        return self.foodtype

#Food Products table
class Product(models.Model):
    foodcategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    foodname = models.CharField(max_length=64)
    foodimg = models.ImageField()
    fooddesc = models.TextField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.foodname

#Order table
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

#Order status, stored in Order Info
STATUS_CHOICE = (
    ("Pending", "Pending"),
    ("Delivered", "Delivered"),

)


#Order Info table
class OrderInfo(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE,
                              default="Pending",
                              max_length=30)
    total_items_qty = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=500)


#Order Items info table
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.__str__} in order {self.order.id}"
