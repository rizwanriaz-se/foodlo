from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
import json
import stripe
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import RegisterForm
from .models import  Product, Order, OrderInfo, OrderItem
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views import View
from django.core.mail import send_mail as sm
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Get the directory containing this script (settings.py)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct path to .env file relative to this script
env_path = os.path.join(base_dir, '..', '.env')

# Load environment variables from .env file
load_dotenv(env_path)

#API KEY for connecting to stripe account
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

#Home page view
def home(request):
    return render(request, "home/index.html")


#Product page view
@method_decorator(login_required, name='dispatch')
class ProductView(View):

    #Display all products along with filters
    def get(self, request, data=None):
        if data == None:
            products = Product.objects.all()
        elif data == 1 or data == 2 or data == 3:
            products = Product.objects.filter(foodcategory=data)

        return render(request, 'home/products.html', {'products': products})


#Register page view
class RegisterView(View):
    
    #Display register page
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})
    
    #Handle register form submission
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            request.session.setdefault('cartdata',[])
            
            return redirect('home')
        return render(request, 'registration/register.html', {'form': form})


#Change password view
def changePassword(request):

    #Handle form submission
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
    
    #Display change password page
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'home/changepassword.html', {'form': form, 'user':request.user})


#Password Reset View
def password_reset(request):

    #Handle form submission
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='registration/password_reset_email.txt',
                subject_template_name='registration/password_reset_subject.txt'
            )
            messages.success(request, 'An email has been sent to reset your password.')
            return redirect('password_reset_done')

    #Display reset password page
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset_form.html', {'form': form})

#New Password confirm view
def password_reset_confirm(request, uidb64, token):
    return auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='http://localhost:8000/reset/done',
        post_reset_login=False,
        post_reset_login_backend='django.contrib.auth.backends.ModelBackend'
    )(request, uidb64=uidb64, token=token)


#About page view
def about(request):
    return render(request, "home/about.html")


#View to handle adding items to cart functionality
@login_required
def addtocart(request):
    prod_id = request.GET.get('prod_id')
    product = Product.objects.get(id=prod_id)
    cartdata = request.session.setdefault('cartdata', [])
    cartitem = {
        'id': product.id,
        'foodname': product.foodname,
        'foodimg': product.foodimg.url,
        'price': product.price,
        'quantity': 1
    }
    for item in cartdata:
        if str(item['id']) == str(cartitem['id']):
            item['quantity'] += 1
            break
    else:
        cartdata.append(cartitem)
    request.session.modified = True

    return redirect('/cart')


#View to display information about specific product
@method_decorator(login_required, name='dispatch')
class ProductSpecificView(View):
    # @login_required
    def get(self, request, pk):
        product = Product.objects.get(pk=int(pk))
        return render(request, 'home/productspecific.html', {
            'product': product,
        })


#View to display cart page
@login_required
def cart(request):
    cartdata = request.session.setdefault('cartdata', [])
    if len(cartdata)>0:
        shipping_amount = 2
        amount = sum(item['price'] * item['quantity'] for item in cartdata)
        return render(request, 'home/cart.html', {
            'cart': cartdata,
            'totalamount': amount+shipping_amount,
            'shipping_amount':shipping_amount,
            'amount': amount
        })
    else:
        return render(request, 'home/emptycart.html')


#View to display order history of user
@login_required
def history(request):
    user = request.user
    history = {'completed': [], 'pending': []}
    for order in Order.objects.filter(user=user):
        order_items = []
        total_items_qty = 0
        for item in OrderItem.objects.filter(order=order):
            order_items.append({'name': item.product, 'quantity': item.quantity})
            total_items_qty += item.quantity
        if order.orderinfo_set.exists():
            order_info = {'id': order.id, 'date': order.orderinfo_set.first().date,
                          'status': order.orderinfo_set.first().status, 'items': order_items,
                          'total_items_qty': total_items_qty}
            if order_info['status'] == 'Delivered':
                history['completed'].append(order_info)
            else:
                history['pending'].append(order_info)
        else:
            order_info = {'id': order.id, 'status': 'Pending', 'items': order_items,
                          'total_items_qty': total_items_qty}
            history['pending'].append(order_info)

    return render(request, 'home/history.html', {'user': user, 'history': history})


#View to handle increment of cart item quantity
@login_required
def pluscart(request): 

    if request.method == 'GET':
        id = request.GET['prodid']
        cartdata = request.session.setdefault('cartdata', [])
        for item in cartdata:
            if str(id) == str(item['id']):
                item['quantity'] +=1
                request.session.modified= True
                break
        shipping_amount = 2
        amount = sum(item['price'] * item['quantity'] for item in cartdata)
        data = {
                'quantity': item['quantity'],
                'amount': amount,
                'totalamount': amount + shipping_amount
                }
        return JsonResponse(data)


#View to handle decrement of cart item quantity
@login_required
def minuscart(request):
    if request.method == 'GET':
        id = request.GET['prodid']
        cartdata = request.session.setdefault('cartdata', [])
        for item in cartdata:
            if str(id) == str(item['id']):
                if item['quantity'] > 1:
                    item['quantity'] -=1
                    request.session.modified= True
                break
        shipping_amount = 2
        amount = sum(item['price'] * item['quantity'] for item in cartdata)
        data = {
                'quantity': item['quantity'],
                'amount': amount,
                'totalamount': amount + shipping_amount
                }
        return JsonResponse(data)
    

#View to display empty cart page
def emptycart(request):
    return render(request,'home/emptycart.html')


#View to handle removal of item from cart
@login_required
def removecart(request):
    if request.method == 'GET':
        user = request.user
        cartdata = request.session.setdefault('cartdata', [])
        if len(cartdata) > 0:
            id = request.GET['prodid']
            for index, item in enumerate(cartdata):
                if str(item['id']) == str(id):
                    del cartdata[index]
                    request.session.modified=True
                    break 
            shipping_amount = 2
            amount = sum(item['price'] * item['quantity'] for item in cartdata)
            if len(cartdata) >0:    
                data = {
                'quantity': item['quantity'],
                'amount': amount,
                'totalamount': amount + shipping_amount
                }
                return JsonResponse(data)
            else:
                return redirect('/emptycart')
        else:
            return render(request,"home/emptycart.html")


#View to handle checkout page
@method_decorator([csrf_exempt, login_required], name='dispatch')
class checkout(View):

    #For submitting checkout form
    def post(self,request):
        user=request.user
        body_unicode = request.body.decode('utf-8')
        
        body = json.loads(body_unicode)
        billing_address = body['billingAddress']
        request.session['order_address'] = billing_address
        order = Order.objects.create(user=user)
        request.session['order_id'] = order.id
        try:
            lineItems = []
            cartdata = request.session.get('cartdata',[])
            for i in cartdata:
                id = i['id']
                quantity = i['quantity']
                product = Product.objects.get(id=id)
                stripe_price_id = product.stripe_price_id
                lineItems.append({'price':stripe_price_id, 'quantity':quantity})

            checkout_session = stripe.checkout.Session.create(
                payment_method_types = ['card'],
                shipping_options=[
                    {
                        "shipping_rate_data": {
                            "type": "fixed_amount",
                            "fixed_amount": {"amount": 200, "currency": "usd"},
                            "display_name": "Delivery Charges",
                        },
                    },
                  ],
                line_items = lineItems,
                mode=  'payment',
                success_url='http://localhost:8000/orders/',
                cancel_url='http://localhost:8000/checkout/', 
                metadata={
                     'address': billing_address,
                 }
            )
            request.session.save()
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    #View to display checkout page
    def get(self,request):
        user = request.user
        shipping_amount = 2
        cartdata=request.session.get('cartdata',[])
        if cartdata == []:
            messages.warning(request, 'Your cart is empty. Please add items to cart before proceeding to checkout.')
            return redirect('cart')
        amount = sum(item['price'] * item['quantity'] for item in cartdata)
        return render(request, 'home/checkout.html', {
            'user': user,
            'incheckout': cartdata,
            'total_price': amount + shipping_amount,
            'key': settings.STRIPE_PUBLISHABLE_KEY
        })


#View for handling stripe webhooks
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('STRIPE_SIGNATURE')
    endpoint_secret = os.environ.get('ENDPOINT_SECRET')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        order_id = event['data']['object']['client_reference_id']
        order = Order.objects.get(id=order_id)
        order.save()

    return redirect('orders')


#View to display orders page
@login_required
def OrdersView(request):
    user = request.user
    shipping_amount = 2
    cartdata=request.session.get('cartdata')
    
    # Check if cart is empty
    if cartdata == [] or None:
        return redirect('cart')
 
    #Retrieve address and order from session
    else:
        order_id = request.session.get('order_id')
        
        #Find order in session, if nothing found, redirect to cart page
        try:
            order = get_object_or_404(Order, id=order_id)
        except:
            return redirect('cart')
        address = request.session.get('order_address')
        total_quantity = 0


        # Save the OrderInfo and OrderItem object to the database
        for item_data in cartdata:
            product = Product.objects.get(id=item_data['id'])
            quantity = item_data['quantity']
            total_quantity += quantity

            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        OrderInfo.objects.create(orderid=order, status='Pending', total_items_qty=total_quantity, address=address)

        order_of_user = Order.objects.filter(user=user)
        recent_order = order_of_user.last()
        status="Pending"
        
        #Send email to user about ordder confirmation
        res = sm(
             subject="Order Info",
                     message=('You order has been confirmed.\nOrder ID: {}\nDelivery Address: {}\nIt contains:\n\t{}'.format(recent_order,address, "".join("{} - {}\n".format(i["quantity"], i["foodname"]) for i in cartdata))),

            
             from_email='foodlo.mail.pk@gmail.com',
             recipient_list=[user.email],
             fail_silently=False)
        
        amount = sum(item['price'] * item['quantity'] for item in cartdata)
        request.session['cartdata'] = []
        request.session.modified = True
        return render(
            request, 'home/orders.html', {
                'user': str(user).title(),
                'orderid': recent_order,
                'incheckout': cartdata,
                'total_price': amount + shipping_amount,
               'status': status
            })


#View for displaying profile page
@login_required
def profile(request):
    user = request.user
    return render(request, 'home/profile.html', {'user': user})


#View for handling newsletter subscription
def send_mail(request):
    person = request.GET['email']
    res = sm(
        subject="Thanks for subscribing to our newletter",
        message=
        "Thanks for subscribing to our newsletter. We will keep you updated about discounts.",
        from_email='foodlo.mail.pk@gmail.com',
        recipient_list=[person],
        fail_silently=False)
    return HttpResponse(f"Email sent to {res} members.")
