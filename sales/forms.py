from django import forms
from sales.models import Invoice, InvoiceInstallment, ShopInvoice, BillChecker


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

class BillCheckerForm(forms.ModelForm):
    class Meta:
        model = BillChecker
        fields = '__all__'


class ShopInvoiceForm(forms.ModelForm):
    class Meta:
        model = ShopInvoice
        fields = '__all__'

class InvoiceInstallmentForm(forms.ModelForm):
    class Meta:
        model = InvoiceInstallment
        fields = '__all__'
