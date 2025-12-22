from django.shortcuts import render, redirect
from .forms import *
from .models import *

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

