from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "category", "price", "stock", "image", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Product name"}),
            "sku": forms.TextInput(attrs={"class": "input", "placeholder": "SKU"}),
            "category": forms.Select(attrs={"class": "input"}),
            "price": forms.NumberInput(attrs={"class": "input", "min": "0.01", "step": "0.01"}),
            "stock": forms.NumberInput(attrs={"class": "input", "min": "0", "step": "1"}),
            "image": forms.ClearableFileInput(attrs={"class": "input"}),
            "description": forms.Textarea(attrs={"class": "input", "rows": 4}),
            "is_active": forms.CheckboxInput(attrs={"class": "checkbox"}),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data["stock"]
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock
