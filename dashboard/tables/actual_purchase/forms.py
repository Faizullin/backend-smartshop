from django import forms
from shop_app.models import Purchase

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['user', 'products','status','total_price']