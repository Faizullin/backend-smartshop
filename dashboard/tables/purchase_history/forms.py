from django import forms
from shop_app.models import Purchase, PurchaseItem

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'price']

class PurchaseForm(forms.ModelForm):
    purchase_items = forms.inlineformset_factory(Purchase, PurchaseItem, form=PurchaseItemForm, extra=1)

    class Meta:
        model = Purchase
        fields = ['shop', 'user', 'products','status','total_price']

    # def __init__(self, *args, **kwargs):
    #     super(PurchaseForm, self).__init__(*args, **kwargs)
    #     self.fields['purchase_date'].widget.attrs['class'] = 'datepicker'