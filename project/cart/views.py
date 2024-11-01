from decimal import Decimal
import email
from django.conf import settings
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import razorpay
from project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from userdetails.models import *
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest


@login_required(login_url='login')
def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    cart.discnt=0
    cart.summarycart()
    cartitems = CartItem.objects.filter(cart=cart)
    count = cartitems.count()
    cart.discnt=0
    return render(request, 'user/cart.html', {'cartitems': cartitems, 'cart': cart, 'count': count})



@login_required(login_url='login')
def add_to_cart(request, id):
    current_url = request.path
    
    user = request.user
    variant = get_object_or_404(Variant, id=id)
    cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    cart.discnt=0
    wishlist_item = Wishlist.objects.filter(user=user, variant=variant).first()
    print(variant.stock)
    if variant.stock == 0:
        messages.error(request, "Product out of stock")
        return redirect('product_details', variant.product.id)
    
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, variant=variant)
    if cart_item.quantity < variant.stock:
        if wishlist_item:
            wishlist_item.delete()

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            
            messages.success(request, 'Item added to cart')
    else:
        messages.error(request, "Product out of stock")
      
    source = request.POST.get('source')
    if source == 'wishlist':
        return redirect('wishlist')
    else:
        return redirect('product_details', variant.product.id)

@login_required(login_url='login')
def remove_item(request, item_id):
    user=request.user
    cart=Cart.objects.get(user=user)
    cart.discnt=0
    cart.summarycart()
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def update_quantity(request, cart_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=cart_id)

        if action == 'decrement':
            cart_item.quantity = max(1, cart_item.quantity - 1)
        elif action == 'increment':
            if cart_item.quantity < cart_item.variant.stock:
                cart_item.quantity += 1
        
        cart_item.save()
        item_total = cart_item.variant.price * cart_item.quantity
        user = request.user
        cart = Cart.objects.get(user=user)
        cart.discnt=0
        cart.summarycart()

    return redirect('cart')

@login_required(login_url='login')   
def apply_coupon(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    
    if request.method == 'POST':
        code = request.POST.get('code')
        
        if not code or code.isspace():
            messages.error(request, "Enter a valid Coupon code")
            return redirect('address')
        
        try:
            coupon = Coupon.objects.get(code=code)      
            order_exists = Order.objects.filter(user=user).exists()
            
            if coupon.active and cart.total > coupon.minimum_amount:
                if code == 'TiaraFirst' and not order_exists:
                    grand_total = cart.grand_total
                    discount = (grand_total * coupon.dis_per) / 100
                    cart.discnt = discount
                    grand_total -= discount
                    cart.summarycart()
                    
                    request.session['code'] = code
                    return redirect('address')
                
                elif code != 'TiaraFirst':
                    grand_total = cart.grand_total
                    discount = (grand_total * coupon.dis_per) / 100  
                    cart.discnt = discount
                    grand_total -= discount
                    cart.summarycart()
                    request.session['code'] = code
                    return redirect('address')
            
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid Coupon Code or coupon not available')
            return redirect('address')

    return redirect('address')


@login_required(login_url='login')
def cancel_coupon(request):
    user=request.user
    cart=Cart.objects.get(user=user)
    cart.discnt=0
    cart.save()
    return redirect('address')

    

@login_required(login_url='login')
def address_page(request):
    user = request.user
    addresses=Address.objects.filter(user=user)
    cartitem=CartItem.objects.all()
    cart=Cart.objects.get(user=user)
    cart.summarycart()
    code=request.session.get('code')
    coupon = None
    try:
        coupon=Coupon.objects.get(code=code)
    except:
        if cartitem:
            return render(request, 'user/address.html', {'addresses': addresses, 'cart':cart, 'coupon':coupon})

        messages.error(request,"Your cart is empty. Add items to the cart before proceeding to the checkout.")
        return redirect('cart')
    return render(request, 'user/address.html', {'addresses': addresses, 'cart':cart, 'coupon':coupon})


@login_required(login_url='login')
def add_address(request):
    referer = request.META.get('HTTP_REFERER')
    print(referer)
    if request.method=='POST':
        
        fullname=request.POST.get("name",'')
        address=request.POST.get('address','')
        city=request.POST.get('city','')
        pincode=request.POST.get('zip','')
        country=request.POST.get('country','')
        phone_no=request.POST.get('phone','')
        if  not fullname or not address or not city or not pincode or not country or not phone_no:
            messages.error(request,"fill the all  fields")
            if source == 'profile':
                return redirect('profile')
            else:
                return redirect('address')
        elif fullname.isspace() or address.isspace() or city.isspace() or country.isspace() or len(phone_no)!=10:
            messages.error(request,"Enter the valid inputs")
            if source == 'profile':
                return redirect('profile')
            else:
                return redirect('address')
                            
        address=Address.objects.create(user=request.user,full_name=fullname,address=address,city=city,pincode=pincode,country=country,phone_No=phone_no)
        address.save()
        source = request.POST.get('source')
        if source == 'profile':
            return redirect('profile')
        else:
            return redirect('address')
        
    
@login_required(login_url='login')
def remove_address(request,id):
    current_url = request.path
    address=Address.objects.get(id=id)
    address.delete()
    source = request.POST.get('source')
    if source == 'profile':
        return redirect('profile')
    else:
        return redirect('address')
    
   
    
@login_required(login_url='login')
def get_address(request,id):
    address=Address.objects.get(id=id)
    
    return render(request, 'user/edit_address.html',{'address':address})


@login_required(login_url='login')
def update_address(request,id):
    address=Address.objects.get(id=id)
    if request.method=="POST":
        address.full_name=request.POST.get("name")
        address.address=request.POST.get("address")
        address.city=request.POST.get("city")
        address.pincode=request.POST.get("pincode")
        address.country=request.POST.get("country")
        address.phone_No=request.POST.get("phone")
        if not address.full_name or not address.address or not address.city or not address.pincode or not address.country or not address.phone_No:
            messages.error(request,"fill the all  field")
            return redirect('get_address',id)
        elif address.full_name.isspace() or address.address.isspace() or address.city.isspace() or address.country.isspace() or len(address.phone_No)!=10 or len(address.pincode)!=6:
            messages.error(request,"Enter the valid inputs")
            return redirect('get_address',id)
        address.save()
        if 'profile' in request.META.get('HTTP_REFERER'):
    
            return redirect('profile')
        else:
            return redirect('address')   

@login_required(login_url='login')
def cod(request,address_id):
    user=request.user
    cart=Cart.objects.get(user=user)
    cart.summarycart()
    address = Address.objects.get(id=address_id)
    return render(request,'user/cod.html',{ 'cart':cart, 'address':address})

@login_required(login_url='login')
def place_order(request,id):
    user=request.user
    email=user.email
    address = Address.objects.get(id=id)
    cart_items = CartItem.objects.all()
    cart=Cart.objects.get(user=user)
    cart.summarycart()
    address1=request.session.get('shipping_address')
    shipping_address = Shipping_address.objects.create(
        full_name=address.full_name,
        address=address.address,
        city=address.city,
        country=address.country,
        pincode=address.pincode,
        phone_No=address.phone_No,
    )
    
    order ,created = Order.objects.get_or_create(
        user=request.user, 
        shipping_address=shipping_address,
        total_amount=cart.total,
        Grand_total=cart.grand_total,
        payment_status=3,  
        status='confirmed',
        payment_method='Cash On Delivery',
        discount=cart.discnt,
        # quantity=cart.quantity
    )
    order.save()
    cart.discount=0
    for cart_item in cart_items:
        order_item=OrderItem.objects.create(order=order, variant=cart_item.variant, quantity=cart_item.quantity, product_price=cart_item.variant.price)
        product = order_item.variant
        product.stock -= order_item.quantity
        product.save()
    cart_items.delete()
    send_mail("Your Order is Confirmed", 'Message body goes here', EMAIL_HOST_USER, [email], fail_silently=True)
    return redirect('order_confirmation', order.id)


@login_required(login_url='login')
def wallet_payment(request,id):
    user=request.user
    address = Address.objects.get(id=id)
    print(address.id)
    cart=Cart.objects.get(user=user)
    return render(request, 'user/walletpayment.html', {'cart': cart, 'address': address})

@login_required(login_url='login')
def pay_wallet(request,id):
    address=Address.objects.get(id=id)
    user=request.user
    shipping_address = Shipping_address.objects.create(
        full_name=address.full_name,
        address=address.address,
        city=address.city,
        country=address.country,
        pincode=address.pincode,
        phone_No=address.phone_No,
    )
    cartitems=CartItem.objects.all()
    cart=Cart.objects.get(user=user)
    wallet=Wallet.objects.get(user=user)
    if wallet.balance>=cart.grand_total:
        wallet.balance=wallet.balance-cart.grand_total
        wallet.save()

        order ,created = Order.objects.get_or_create(
        user=request.user, 
        shipping_address=shipping_address,
        total_amount=cart.total,
        Grand_total=cart.grand_total,
        payment_status=1,  
        status='confirmed',
        payment_method='Wallet',
        discount=cart.discnt
        )
        order.save()
        WalletTransaction.objects.create(user=user, amount=order.Grand_total, transaction_type='debit',transaction_details="Tiara"+str(order.id) + " ordered by wallet")

        cart.discount=0
        for cart_item in cartitems:
            order_item=OrderItem.objects.create(order=order, variant=cart_item.variant, quantity=cart_item.quantity, product_price=cart_item.variant.price)
            product = order_item.variant
            product.stock -= order_item.quantity
            product.save()
        cartitems.delete()
        return redirect('order_confirmation', order.id)
    messages.error(request,'Insufficient balance on your wallet')
    return redirect('wallet_payment',id)
    
@login_required(login_url='login')
def order_confirmation(request,order_id):
    order=Order.objects.get(id=order_id)
    transaction= request.GET.get('transaction_id')
    return render(request, 'user/orderconfirmation.html', {'order':order, 'transaction':transaction})

# @login_required(login_url='login')
# def cancel_order(request, order_id):
#     order=order.object.get(id=order_id)
#     if order.payment_status=='1':
#         order.status="False"
#         order.save()
#         for order_item in order.items.all():
#             product = order_item.variant
#             product.stock += order_item.quantity
#             product.save()
    
#     return redirect('orderdetails')

@login_required(login_url='login')
def razor_pay(request,id):
    address=Address.objects.get(id=id)
    return render(request, 'user/onlinepayment.html', {'address': address})


@login_required(login_url='login')
def online_payment(request,id):
    user=request.user
    cart_items = CartItem.objects.all()
    address = Address.objects.get(id=id)
    shipping_address = Shipping_address.objects.create(
        full_name=address.full_name,
        address=address.address,
        city=address.city,
        country=address.country,
        pincode=address.pincode,
        phone_No=address.phone_No,
    )
    cart=Cart.objects.get(user=user)
    cart.summarycart()
    
    client = razorpay.Client(auth=(settings.KEY,  settings.SECRET))
    amount = float(cart.grand_total)*100

    payment = {
        'amount': amount,
        'currency': 'INR',
        'payment_capture': 1  # Auto capture payment
    }
    clnt_order = client.order.create(data=payment)
    return render(request, 'user/onlinepayment.html', {'address': address, 'clnt_order': clnt_order, 'cart':cart})

@csrf_exempt
def payment_verification(request):
    if request.method == "POST":
        # Extract payment details from the POST request
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        # Verify the payment using Razorpay's utility function
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            # Verify the signature to ensure payment integrity
            client.utility.verify_payment_signature(params_dict)

            # Once verified, update your payment records (e.g., mark the order as paid)
            # Here you would update your cart or order model to reflect payment success
            # cart.order_status = 'PAID'
            # cart.save()

            # Return success response to the frontend
            redirect(create_order)
        except razorpay.errors.SignatureVerificationError:
            # In case verification fails, return an error
            return JsonResponse({'status': 'Payment verification failed'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request")

    
@login_required(login_url='login')
def create_order(request,id):

    address=Address.objects.get(id=id)
    user=request.user
    cart_items = CartItem.objects.all()
    address = Address.objects.get(id=id)
    cart=Cart.objects.get(user=user)
    
    cart.summarycart()
    shipping_address = Shipping_address.objects.create(
        full_name=address.full_name,
        address=address.address,
        city=address.city,
        country=address.country,
        pincode=address.pincode,
        phone_No=address.phone_No,
    )
    # if cart_item.product.stock>=cart_item.product.qunatity:
    order = Order.objects.create(
        user=request.user,  
        shipping_address=shipping_address,
        total_amount=cart.total,
        Grand_total=cart.grand_total,
        payment_status=1,  
        status='confirmed',
        payment_method='Online Payment',
        discount=cart.discnt
        )
    for cart_item in cart_items:
        order_item=OrderItem.objects.create(order=order, variant=cart_item.variant, quantity=cart_item.quantity, product_price=cart_item.variant.price)
        product = order_item.variant
        product.stock -= order_item.quantity
        product.save()
        cart_items.delete()
    return redirect(order_confirmation,  order.id)
    
   