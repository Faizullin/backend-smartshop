from django import forms
from shop_app.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description','shop', 'price','type','image']