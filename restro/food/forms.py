from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"
class RecipeTypeForm(forms.ModelForm):
    class Meta:
        model = RecipeType
        fields = "__all__"
class RecipeVariantForm(forms.ModelForm):
    class Meta:
        model = RecipeVariant
        fields = "__all__"
    
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'street','phone','city', 'pincode']
        
    