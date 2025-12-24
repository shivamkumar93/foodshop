from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
User = get_user_model()
from django.http import HttpResponse

def home(request):
    data = {}
    data['recipes'] = Recipe.objects.all()
    data['categories'] = Category.objects.all()
    data['variants'] = RecipeVariant.objects.all()
    data['recipetypes'] = RecipeType.objects.all()
    data['orders'] = Order.objects.filter(user=request.user)
    data['orderitems'] = OrderItems.objects.all()
    return render(request, 'recipe/home.html', data)

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

    order, create = Order.objects.get_or_create(user=request.user, status = 'pending')

    item, create = OrderItems.objects.get_or_create(order=order, recipevariant = recipe_variant)

    if not create:
        item.quantity += 1
        item.save()
    return redirect(home)

def deleteOrder(request, order_id):
    item = get_object_or_404(Order, id=order_id)
    item.delete()
    return redirect(home)

