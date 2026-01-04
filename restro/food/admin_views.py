from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
User = get_user_model()
from django.http import HttpResponse, JsonResponse
import razorpay
from django.conf import settings
import json


@login_required
def home(request):
    data = {}
    data['recipes'] = Recipe.objects.all()
    data['categories'] = Category.objects.all()
    data['variants'] = RecipeVariant.objects.all()
    data['recipetypes'] = RecipeType.objects.all()
    data['orders'] = Order.objects.filter(user=request.user, status = 'pending').prefetch_related('items__recipevariant__recipe')
    data['orderitems'] = OrderItems.objects.all()
    return render(request, 'recipe/home.html', data)


@login_required
def address(request):
   
    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('address')
    else:
        form = AddressForm()
    return render(request, 'recipe/address.html',{'form':form, 'addresses':addresses})

def registerUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        conform_password = request.POST.get('conform_password')

        if not email or not password or not conform_password:
            messages.error(request, "all fields are required")

        user = User.objects.create_user(email=email, password=password)
        user.save()
        return redirect('loginuser')

    return render(request, 'auth/register.html')

def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            return HttpResponse(request,"I don`t why")
        
        login(request,user)

        return redirect('home')
    
    return render(request, 'auth/login.html')

def logoutuser(request):
    logout(request)
    return redirect('loginuser')


def category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(category)
    else:
        form = CategoryForm()
    return render(request, 'recipe/categoryform.html', {'form':form})

def recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(recipe)  
    else:
        form = RecipeForm()
    return render(request, 'recipe/recipeform.html', {'form':form})

def recipetype(request):
    if request.method == 'POST':
        form = RecipeTypeForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(recipetype)
    else:
        form = RecipeTypeForm()
    return render(request, 'recipe/recipetype.html', {'form':form})

def recipevariant(requset):
    if requset.method == 'POST':
        form = RecipeVariantForm(requset.POST or None)
        if form.is_valid():
            form.save()
            return redirect(recipevariant)
    else:
        form = RecipeVariantForm()
    return render(requset, 'recipe/recipevariantform.html', {'form':form})

def create_order(request, variant_id):
    recipe_variant = get_object_or_404(RecipeVariant, id=variant_id)

    order, order_create = Order.objects.get_or_create(user=request.user, status = 'pending')

    item, item_create = OrderItems.objects.get_or_create(order=order, recipevariant = recipe_variant)

    if not item_create:
        item.quantity += 1
        item.save()
    return redirect(home)

def deleteOrder(request, order_id):
    item = get_object_or_404(Order, id=order_id)
    item.delete()
    return redirect(home)

@login_required
def increaseitme(request, item_id):
    additem = get_object_or_404(OrderItems, id=item_id, order__user= request.user)
    
    additem.quantity += 1
    additem.save()
    return redirect(home)

# @login_required
# def decrease_item(request, id):
#     item = get_object_or_404(OrderItems, id=id)
#     if item.quantity > 1:
#         item.quantity -= 1
#         item.save()
#     else:
#         item.delete()
#     return redirect(home)

def payment(request, order_id):
    try:
        addresses = Address.objects.filter(user=request.user)
    except:
        return HttpResponse(request,"Hi here we are")
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':

        data = json.loads(request.body)   
        address_id = data.get("address_id")
        
        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)

        order.address = address
        order.save()

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        amount = int(order.get_total_price() * 100)

        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        payment = Payment.objects.create(order=order, razorpay_order_id= razorpay_order['id'], status = 'pending')


        # If request content is JSON (AJAX/fetch) return JSON so front-end can open Razorpay popup
        if request.content_type == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'order': order.id,
                'amount': amount,  # amount is in paise already
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'razorpay_order_id': razorpay_order['id'],
                'name': order.user.first_name,
            })

        return render(request, 'recipe/payment.html', {
            'order': order,
            'addresses': addresses,
            'amount': amount,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order['id'],
        })

    return render(request, 'recipe/payment.html', {
        'addresses': addresses,
        'order': order
    })


def payment_verify(request):
    if request.method == 'POST':
        # support both form POST and JSON POST
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_signature = data.get('razorpay_signature')
        else:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id':razorpay_order_id,
                'razorpay_payment_id':razorpay_payment_id,
                'razorpay_signature':razorpay_signature
            })
        except Exception as e:
            if request.content_type == 'application/json':
                return JsonResponse({'error':'payment failed', 'details': str(e)}, status=400)
            return HttpResponse('payment failed')
        
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        payment.razorpay_payment_id=razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'success'
        payment.save()

        order = payment.order
        order.status = 'paid'
        order.save()
        return redirect('order_success')


@login_required
def order_success(request):
    # Simple success page after payment
    return render(request, 'recipe/order_success.html')
    
