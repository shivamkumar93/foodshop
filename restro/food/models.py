from django.db import models

# Create your models here.

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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipe} - {self.quantity}"