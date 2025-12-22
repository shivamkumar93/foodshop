from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(RecipeType)
admin.site.register(RecipeVariant)