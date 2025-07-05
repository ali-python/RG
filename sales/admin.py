from django.contrib import admin
from sales.models import Invoice, InvoiceInstallment, BillChecker, ShopInvoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'customer', 'total_quantity', 'sub_total', 'grand_total', 'date'
    )

    @staticmethod
    def invoice(obj):
        return str(obj.id).zfill(7)

class InvoiceInstallmentAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'paid_amount', 'description', 'date'
    )


admin.site.register(Invoice, InvoiceAdmin)

admin.site.register(ShopInvoice)
admin.site.register(InvoiceInstallment, InvoiceInstallmentAdmin)
admin.site.register(BillChecker)