from turtle import title
from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, UserInfoForm
from .models import  Product, Order, OrderInfo
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail as sm
from django.db import connection


# Create your views here.
def home(request):
    return render(request, "home/index.html")


class ProductView(View):
    def get(self, request, data=None):
        if data == None:
            products = Product.objects.all()
            print(products.query)
        elif data == 1 or data == 2 or data == 3:
            products = Product.objects.filter(foodcategory=data)
            print(products.query)
        return render(request, 'home/products.html', {'products': products})



class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):

        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             'Congratulations! Registered successfully')
            form.save()
            
        return render(request, 'registration/register.html', {'form': form})

def about(request):
    return render(request, "home/about.html")

carts=[] 
def addtocart(request):
    prod_id= request.GET.get('prod_id')
    product=Product.objects.get(id=prod_id)
    cartitem={
        'id':product.id,
        'foodname':product.foodname,
        'foodimg':product.foodimg.url,
        'price':product.price,
        'quantity':1
    }
    
    if 'cartdata' in request.session:
        if cartitem['id'] not in request.session['cartdata']:
            carts.append(cartitem)
            request.session['cartdata']=carts

    else:

        carts.append( cartitem)
        request.session['cartdata']=carts
    print(carts)
    return redirect('/cart')

class ProductSpecificView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=int(pk))
        already_in_cart = False

        for cart in carts:
            if product.id == cart['id']:
                already_in_cart=True
            else:
                already_in_cart=False 
        return render(request, 'home/productspecific.html', {
            'product': product,
            "already_in_cart": already_in_cart
        })

   
def cart(request):
    if len(carts)>0:
        shipping_amount = 2
        amount=0
        total_amount=0
        for i in range(0,len(carts)):
            amount=carts[i]['price']
            total_amount+=amount
        return render(request, 'home/cart.html', {
            
            'cart': carts,
            
            'totalamount': total_amount+shipping_amount,
            'shipping_amount':shipping_amount,
            'amount': total_amount
        })
    else:
        return render(request, 'home/emptycart.html')

# to increment item
def pluscart(request): 
    if request.method == 'GET':
        id = request.GET['prodid']
        item_qty=1
        amount = 0
        shipping_amount = 2
        total_amount = 0

        for i in range(0,len(carts)):
            if int(carts[i]['id']) == int(id):
                carts[i]['quantity'] +=1
                item_qty=carts[i]['quantity']
            
            amount=carts[i]['price'] * item_qty
            total_amount+=amount
            data = {
                'quantity': item_qty,
                'amount': amount,
                'totalamount': total_amount + shipping_amount
                }
        return JsonResponse(data)

# to decrement item
def minuscart(request):

    if request.method == 'GET':
        id = request.GET['prodid']
        amount = 0
        shipping_amount = 2
        total_amount = 0
        item_qty=1
        for i in range(0,len(carts)):
            print(id)
            print(int(carts[i]['id']) == int(id))
            print(i)
            if int(carts[i]['id']) == int(id):
                if carts[i]['quantity'] >1:
                    carts[i]['quantity'] -=1
                    item_qty=carts[i]['quantity'] 
                print(carts)
                print(carts[i]['quantity'])
                print(carts[i]['id'])
            
            amount=carts[i]['price'] * item_qty
            total_amount+=amount
            data = {
                'quantity': item_qty,
                'amount': amount,
                'totalamount': total_amount + shipping_amount
                }
        return JsonResponse(data)
    

def emptycart(request):
    return render(request,'home/emptycart.html')

#to remove item
def removecart(request):
    if request.method == 'GET':
        user = request.user
        if len(carts) > 0:
            item_qty=1
            id = request.GET['prodid']
   
            if 'cartdata' in request.session:
                for index, item in enumerate(carts):
                    print(int(item['id']) == int(id))
                     
                    if int(item['id']) == int(id):
                        del carts[index]
                carts = carts
            
            amount = 0
            shipping_amount = 2
            total_amount = 0
            for i in range(0,len(carts)):
                if int(carts[i]['id']) == int(id):
                    item_qty = carts[i]['quantity']
            
                amount=carts[i]['price'] * item_qty
                total_amount+=amount
            if len(carts) >0:    
                data = {
                'quantity': item_qty,
                'amount': amount,
                'totalamount': total_amount + shipping_amount
                }
                return JsonResponse(data)
            else:
                return redirect('/emptycart')
        else:
            return render(request,"home/emptycart.html")


class checkout(View):    
    def post(self,request):  

        user = request.user    
        form = UserInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders')    
    def get(self,request):
        amount = 0
        shipping_amount = 2
        total_amount = 0

        for i in range(0,len(carts)):
            item_qty = carts[i]['quantity']
            
            amount=carts[i]['price'] * item_qty
            total_amount+=amount

        form = UserInfoForm()
        return render(request, 'home/checkout.html', {
            'form': form,
            'incheckout': carts,
            'total_price': total_amount + shipping_amount
        })


def OrdersView(request):
    
        user = request.user
        shipping_amount = 2
        amount=0
        total_amount=0
        for i in range(0,len(carts)):
            item_qty = carts[i]['quantity']
            amount=carts[i]['price'] * item_qty
            total_amount+=amount
            product=Product.objects.get(id=carts[i]['id'])

            for val in Order.objects.filter(user=user):
                OrderInfo.objects.create(orderid=val,items=product,quantity=item_qty)
                       
            
        person = user.email
        print(person)
        order_of_user = Order.objects.filter(user=user)
        recent_order = order_of_user.last()
        print(Order.objects.filter(user=user))
        print(recent_order)
        print([p for p in carts])
        status="Pending"
        res = sm(
            subject="Order Info",
            message=(f"You order {recent_order} has been confirmed. It contains {str([p['foodname'] for p in carts])}"),
            
            from_email='foodlo.mail.pk@gmail.com',
            recipient_list=[user.email],
            fail_silently=False)
        print(res)
        return render(
            request, 'home/orders.html', {
                'user': str(user).title(),
                'orderid': recent_order,
                'incheckout': carts,
                'total_price': total_amount + shipping_amount,
               'status': status
            })

def profile(request):
    user = request.user
    history=[]
    for order in Order.objects.filter(user=user):
        for item in OrderInfo.objects.filter(orderid=order):
            history.append({'name':item.items.foodname,'id':item.orderid,'quantity':item.quantity})
    return render(
        request,
        'home/profile.html',
        {
            'user': user,
            'history':history
        })


    

def send_mail(request):
    person = request.GET['email']
    print(person)
    res = sm(
        subject="Thanks for subscribing to our newletter",
        message=
        "Thanks for subscribing to our newsletter. We will keep you updated about discounts.",
        from_email='foodlo.mail.pk@gmail.com',
        recipient_list=[person],
        fail_silently=False)
    print(res)
    return HttpResponse(f"Email sent to {res} members.")
