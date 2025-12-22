from django.shortcuts import render, redirect
from .forms import *
from .models import *

def category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(category)
    else:
        form = CategoryForm()
    return render(request, 'recipe/categoryform.html', {'form':form})
