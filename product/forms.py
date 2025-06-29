from django import forms
from product.models import (
    ProductCategory, Product, StockIn, StockOut, PurchasedItem, ShopStockOut, ShopPurchasedItem
)


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = '__all__'


class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = '__all__'

class ShopStockOutForm(forms.ModelForm):
    class Meta:
        model = ShopStockOut
        fields = '__all__'

class PurchasedItemForm(forms.ModelForm):
    class Meta:
        model = PurchasedItem
        fields = '__all__'


class ShopPurchasedItemForm(forms.ModelForm):
    class Meta:
        model = ShopPurchasedItem
        fields = '__all__'