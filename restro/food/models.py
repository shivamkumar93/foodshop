from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_varified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.name

class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    price = models.IntegerField(default=0)
    is_veg = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email}"
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

  
    def __str__(self):
        return f"{self.recipe.price} x {self.quantity} -- {self.recipe.title}"