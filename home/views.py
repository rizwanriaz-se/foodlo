from turtle import title
from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, UserInfoForm
from .models import User, Category, Product, Order, OrderInfo, UserInfo
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, JsonResponse
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
    def get_success_url(self, user):
        return redirect('/home/')

    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):

        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             'Congratulations! Registered successfully')
            form.save()
            self.get_success_url(user=request.user)

    #return HttpResponseRedirect(self.get_success_url())
        return render(request, 'registration/register.html', {'form': form})
    """
  if request.method =="POST":
    form=RegisterForm(request.POST)
    if form.is_valid:
      username=form.cleaned_data["username"]
      password=form.cleaned_data["password1"]
      form.save()
      new_user=authenticate(
        username=username,
        password=password
      )
      
      if new_user is not None:
        Users.username=username
        Users.password=password
        Users.username.save_form_data(username)
        Users.password.save_form_data(password)
        new_user.save()
        login(request,new_user)
        return redirect('home/index.html')
      
  form=RegisterForm()
  

  
  return render(request, "registration/register.html",{
    "form": form
  })
"""


#def login(request):
#   return render(request, "registration/login.html")


def about(request):
    return render(request, "home/about.html")


#def products(request):
#    return render(request, #"home/products.html")

#def productspecific(request):
#   return render(request, "home/productspecific.html")

carts=[]
def addtocart(request):
    user = request.user
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
        if cartitem['id'] in request.session['cartdata']:
            already_in_cart=True
        else:
            already_in_cart=False
            carts.append(cartitem)
            request.session['cartdata'] = carts
    else:

        already_in_cart=False
        carts.append(cartitem)
        request.session['cartdata'] = carts
    print(carts)
    return redirect('/cart')

class ProductSpecificView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=int(pk))
        already_in_cart = False

        
    #    already_in_cart_user = Order.objects.filter(
    #         user=request.user).exists()
    #    already_in_cart_item= OrderInfo.objects.filter(items=product.id).exists()
    #    already_in_cart = already_in_cart_user & already_in_cart_item
    #    print(already_in_cart)
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
    #if request.user.is_authenticated:
     #   user = request.user
        
    #    cartitems = Order.objects.filter(user=user)
    #    print(cartitems)
    if len(carts) >0:
        shipping_amount = 2
        
  #  cart_product = [p for p in OrderInfo.objects.all() if p.orderid.user == user]
  #  print(cart_product)
        
        print(carts)
        amount=0
        total_amount=0
        for i in range(0,len(carts)):
            amount=carts[i]['price']
            total_amount+=amount
  #      print(len(carts))
  #      print(amount)
  #      print(total_amount)

        #print(request.session['item'])
    #for i in request.session['item']:
        #val = Product.objects.get(id=int(i))
        #val = {'prod': Product.objects.get(id=int(i))}

        #print(int(i))
    #    prod={'foodname':val.foodname, 'price':val.price}
    #    print(prod)
    #    print(prod['foodname'])
        
    #print(val['prod'])
    
        return render(request, 'home/cart.html', {
            
            'cart': carts,
            
            'totalamount': total_amount+shipping_amount,
            'shipping_amount':shipping_amount,
            'amount': total_amount
        })
    else:
        return render(request, 'home/emptycart.html')


def pluscart(request):
    if request.method == 'GET':
        id = request.GET['prodid']
        item_qty=1
        amount = 0
        shipping_amount = 2
        total_amount = 0

        for i in range(0,len(carts)):
            print(id)
            print(int(carts[i]['id']) == int(id))
            print(i)
            if int(carts[i]['id']) == int(id):
                carts[i]['quantity'] +=1
                item_qty = carts[i]['quantity']
                print(item_qty)
                print(carts)
                print(carts[i]['quantity'])
                print(carts[i]['id'])
            
            amount=carts[i]['price'] * item_qty
            total_amount+=amount
       #return render(request, 'home/cart.html',{
        #        
         #   'cart': carts,
     #       
      #      'totalamount': total_amount+shipping_amount,
       #     'shipping_amount':shipping_amount,
        #    'amount': total_amount
        
      #  })    
            data = {
                'quantity': item_qty,
                'amount': amount,
                'totalamount': total_amount + shipping_amount
                }
        return JsonResponse(data)


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
                #item_qty = carts[i]['quantity']
                #print(item_qty)
                print(carts)
                print(carts[i]['quantity'])
                print(carts[i]['id'])
            
            amount=carts[i]['price'] * item_qty
            total_amount+=amount
       #return render(request, 'home/cart.html',{
        #        
         #   'cart': carts,
     #       
      #      'totalamount': total_amount+shipping_amount,
       #     'shipping_amount':shipping_amount,
        #    'amount': total_amount
        
      #  })    
            data = {
                'quantity': item_qty,
                'amount': amount,
                'totalamount': total_amount + shipping_amount
                }
        return JsonResponse(data)
    

def emptycart(request):
    return render(request,'home/emptycart.html')

def removecart(request):
    if request.method == 'GET':
        user = request.user
        if len(carts) > 0:
            item_qty=1
            id = request.GET['prodid']
            product=Product.objects.get(id=id)
            cartitem={
            'id':product.id,
            'foodname':product.foodname,
            'foodimg':product.foodimg.url,
            'price':product.price,
            'quantity':1
        }
   
            if 'cartdata' in request.session:
#            if cartitem['id'] in request.session['cartdata']:

 #               carts_filtered = list(filter(lambda item: int(item['id']) != int(id), carts))
                
                for index, item in enumerate(carts):
                #print(item['id'])
                #print(id)
                    print(int(item['id']) == int(id))
                     
                    if int(item['id']) == int(id):
                        print(item['id'])
                        print(id)
                        print(item['id'] == id)
                        del carts[index]
                request.session['cartdata'] = carts
                already_in_cart=False
            

                print(carts)
    
    #    prodid = request.GET['prodid']
     #   c = Order.objects.get(Q(items=prodid) & Q(user=user))
      #  c.delete()

            amount = 0
            shipping_amount = 2
            total_amount = 0
    #    cart_product = [
     #       p for p in Order.objects.all() if p.user == request.user
      #  ]
    #    if cart_product:
     #       for p in cart_product:
        #        tempamount = (p.quantity * p.items.price)
        #        amount += tempamount

            for i in range(0,len(carts)):
        #    print(id)
         #   print(int(carts[i]['id']) == int(id))
          #  print(i)
                if int(carts[i]['id']) == int(id):
                    item_qty = carts[i]['quantity']
            #    print(item_qty)
           #     print(carts)
            #    print(carts[i]['quantity'])
             #   print(carts[i]['id'])
            
                amount=carts[i]['price'] * item_qty
                total_amount+=amount
       #return render(request, 'home/cart.html',{
        #        
         #   'cart': carts,
     #       
      #      'totalamount': total_amount+shipping_amount,
       #     'shipping_amount':shipping_amount,
        #    'amount': total_amount
        
      #  }) 
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

      

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
""" prod_id = request.GET.get('prod_id')
    product = Product.objects.get(id = prod_id)
    cart ={}
    cart[str(prod_id)]={
        'foodname': product.foodname,
        'foodimg':product.foodimg.url,
       'price':product.price
    }
    if 'cartitem' in request.session:
        if str(prod_id) in request.session['cartitem']:
            already_in_cart= True
        else:
            already_in_cart=False
            request.session['cartitem']=cart

            cart.update(cart)
            print(cart)
#            cartdata=request.session['cartitem']
            
 #           cartdata.update(cartdata)
  #          request.session['cartitem'] =cartdata
    else:
   #
   #      request.session['cartdata'] = cart      
        request.session['cartitem']=cart
        already_in_cart=False

    #print(cart)
    print(request.session)

    print(request.session['cartitem'])
    print( already_in_cart)

    return redirect('/cart')
    
"""
    
































#    product_id = request.GET.get('prod_id')
 #   product = Product.objects.get(id=product_id)
  #  cart = Order.objects.filter(user=user)
   # cartid = Order(user=user)
#   cartid.save()

#    if user is  None:
#        request.session['item']=[]
#    else:
#        try:
#            request.session['item'].append(product)
#        except KeyError:
#            request.session['item']=[]

#    print(request.session['item'])

#    data = {'id': product.id, 'foodname': product.foodname , 'foodimg':product.foodimg.url, 'price':product.price}
#    #return JsonResponse(data)
#    print(data)
#    return render(request,'home/cart.html',{'cart':data})
  #  Order(user=user).save()
   # OrderInfo(order)
    #return redirect('/cart')


class checkout(View):
#    checkout = [p for p in OrderInfo.objects.all() if p.orderid.user == user]
#    total_price = 0.0
#    item_price = [price for price in checkout]
#    for val in item_price:
#       total_price += val.items.price * val.quantity
    

    def post(self,request):  

        user = request.user    
        form = UserInfoForm(request.POST)
        if form.is_valid():

            #messages.success(request, "info saved")
            form.save()
            print("ds")
            print(request.user)
            print(Order(user=user))
        #    order=Order(user=user)
            order=Order.objects.create(user=user)
            print(order)
        #    order.save()
        return redirect('orders')    
    def get(self,request):
        amount = 0
        shipping_amount = 2
        total_amount = 0

        for i in range(0,len(carts)):
            item_qty = carts[i]['quantity']
            
            amount=carts[i]['price'] * item_qty
            total_amount+=amount
 #   print("-----------")
  #  print(carts)        
   # print(total_amount)

        form = UserInfoForm()
        return render(request, 'home/checkout.html', {
            'form': form,
            'incheckout': carts,
            'total_price': total_amount + shipping_amount
        })


#  return render(request, 'home/checkout.html', {
#       'incheckout': checkout,
#      'total_price': total_price
# })

#def confirm_order(request):
 #   if request.method=="POST":
  #      user=request.user
        
   #     order = Order(user=user)
    #    order.save()

    #return redirect('/orders')
        

def OrdersView(request):
    
        user = request.user
        shipping_amount = 2
        
  #  cart_product = [p for p in OrderInfo.objects.all() if p.orderid.user == user]
  #  print(cart_product)
        
    #    print(carts)
        amount=0
        total_amount=0

 #       order=Order(user=user)
  #      order.save()
        for i in range(0,len(carts)):
            item_qty = carts[i]['quantity']
            amount=carts[i]['price'] * item_qty
            total_amount+=amount
            product=Product.objects.get(id=carts[i]['id'])

            for val in Order.objects.filter(user=user):
                OrderInfo.objects.create(orderid=val,items=product,quantity=item_qty)
                       

        #for i in range(0,len(carts)):
         #   item_qty = carts[i]['quantity']
          #  product_id=carts[i]['id']
            
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
        del request.session['cartdata']
        return render(
            request, 'home/orders.html', {
                'user': str(user).title(),
                'orderid': recent_order,
                'incheckout': carts,
                'total_price': total_amount + 2,
               'status': status
            })
        return render(request, 'home/cart.html', {
            
            'cart': carts,
            
            'totalamount': total_amount+shipping_amount,
            'shipping_amount':shipping_amount,
            'amount': total_amount
        })
    #else:
    #return render(request, 'home/emptycart.html')




    #    person = [user for user in checkout]
    #   order_id = person[0].id
    #  orders=Order(checkout)
    #  order_id = (orders)
     #   orderinfo = OrderInfo(user=user, orderid=order)
      #  orderinfo.save()
        #order_id=2
        #    order=[]
        # for i in range(0,len(checkout)):
        #  checkout[i].items.foodname
      #  order_id = order.id
     #   status = orderinfo.status
        #  cartlater = Cart.objects.filter(user=user)
        #  cartlater.delete()

        return render(
            request, 'home/orders.html', {
                'user': str(user).title(),
       #         'orderid': order_id,
                'incheckout': checkout,
                'total_price': total_price + 2,
        #        'status': status
            })
        #            return render(request, 'home/orders.html',{'form':form})
        # else:
        #  form = UserInfoForm()
        # return render(request,'home/checkout.html',{'form':form})


"""
  def post(self, request):

        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             'Congratulations! Registered successfully')
            form.save()
        return render(request, 'registration/register.html', {'form': form})
"""


def profile(request):
    user = request.user
    #  print(user)
    #  userinfo = UserInfo.objects.get()
    #  print(userinfo)
    # print(userinfo)
    #userinfo = 1
    for order in Order.objects.filter(user=user):
        order.orderid.quantity
    return render(
        request,
        'home/profile.html',
        {
            #   'userinfo': userinfo,
            'user': user
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
