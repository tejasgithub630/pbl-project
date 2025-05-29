from django import forms
from .models import Product, Sale, Purchase

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description',  'price', 'min_stock_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity', 'price_per_unit']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        
        if product and quantity:
            stock = product.stock_set.first()
            if stock and quantity > stock.quantity:
                raise forms.ValidationError(
                    f"Not enough stock available. Current stock: {stock.quantity}"
                )
        return cleaned_data

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'quantity', 'price_per_unit']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all() 