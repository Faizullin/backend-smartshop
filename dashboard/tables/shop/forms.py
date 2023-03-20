from django import forms
from shop_app.models import Shop, CustomUser

class ShopForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    class Meta:
        model = Shop
        fields = ['name','address']
