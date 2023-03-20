from django import forms
from shop_app.models import Product, Shop

class ProductForm(forms.ModelForm):
    image = forms.ImageField(label = "Image",required=False)
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['shop'].queryset = Shop.objects.filter(owner=user)
            if self.instance.pk:
                self.fields['shop'].initial = self.instance.shop

    class Meta:
        model = Product
        fields = ['name', 'description','shop', 'price','type','image']