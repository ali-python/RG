from django.db import models
from django.db.models import Sum
from django.utils import timezone
import uuid
import uuid
import os
from io import BytesIO
from django.core.files import File
from django.db import models
from barcode import Code128
from barcode.writer import ImageWriter


def barcode_upload_path(instance, filename):
    return f'barcodes/invoice_{instance.pk}.png'

class Invoice(models.Model):

    PAYMENT_CASH = 'Cash'
    PAYMENT_INSTALLMENT = 'Installment'
    PAYMENT_CHECK = 'Check'

    PAYMENT_TYPES = (
        (PAYMENT_CASH, 'Cash'),
        (PAYMENT_INSTALLMENT, 'Installment'),
        (PAYMENT_CHECK, 'Check'),
    )

    customer = models.ForeignKey(
        'customer.Customer',
        related_name='customer_sales',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    payment_type = models.CharField(
        choices=PAYMENT_TYPES, default=PAYMENT_CASH, max_length=100)

    bank_details = models.ForeignKey(
        'banking_system.Bank', related_name='bank_detail_payments',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    total_quantity = models.CharField(
        max_length=10, blank=True, null=True, default=1
    )

    sub_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    paid_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    remaining_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    discount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    shipping = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    grand_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    cash_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    cash_returned = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    date = models.DateField(default=timezone.now, blank=True, null=True)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    barcode_image = models.ImageField(upload_to=barcode_upload_path, null=True, blank=True)
    def __str__(self):
        return str(self.id).zfill(7)
    
    def generate_barcode(self):
        unique_id = uuid.uuid4().hex[:10].upper()
        return f"INV{timezone.now().strftime('%Y%m%d')}{unique_id}"

    def generate_barcode_image(self):
        buffer = BytesIO()
        barcode_obj = Code128(self.barcode, writer=ImageWriter())
        barcode_obj.write(buffer)
        file_name = f'invoice_{self.pk}.png'
        self.barcode_image.save(file_name, File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = self.generate_barcode()
        super().save(*args, **kwargs)
        if not self.barcode_image:
            self.generate_barcode_image()
            super().save(update_fields=["barcode_image"])

    def is_installment(self):
        invoice_installments = InvoiceInstallment.objects.filter(
            invoice__id=self.id)

        grand_total = self.grand_total

        if invoice_installments.exists():
            total_paid_amount = invoice_installments.aggregate(
                Sum('paid_amount'))
            total_paid_amount = float(
                total_paid_amount.get('paid_amount__sum') or 0
            )

        else:
            total_paid_amount = 0

        if float(grand_total) <= total_paid_amount:
            return True

        return False

    def remaining_installment(self):
        invoice_installments = InvoiceInstallment.objects.filter(
            invoice__id=self.id)

        grand_total = self.grand_total

        if invoice_installments.exists():
            total_paid_amount = invoice_installments.aggregate(
                Sum('paid_amount'))
            total_paid_amount = float(
                total_paid_amount.get('paid_amount__sum') or 0
            )

        else:
            total_paid_amount = 0

        return float(grand_total) - total_paid_amount

    def has_installment(self):
        if self.invoice_installment.all().exists():
            return True

        return False




class InvoiceInstallment(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name='invoice_installment', on_delete=models.CASCADE)
    paid_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateField(
        default=timezone.now, blank=True, null=True)

    def __str__(self):
        return (
            '%s Installment' % self.invoice.customer.name if
            self.invoice.customer else ''
        )
##################################################Shop Saes Models ##################################
#####################################################################################################

class ShopInvoice(models.Model):

    PAYMENT_CASH = 'Cash'
    PAYMENT_INSTALLMENT = 'Installment'
    PAYMENT_CHECK = 'Check'

    PAYMENT_TYPES = (
        (PAYMENT_CASH, 'Cash'),
        (PAYMENT_INSTALLMENT, 'Installment'),
        (PAYMENT_CHECK, 'Check'),
    )

    customer = models.ForeignKey(
        'customer.Customer',
        related_name='shop_customer_sales',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    payment_type = models.CharField(
        choices=PAYMENT_TYPES, default=PAYMENT_CASH, max_length=100)

    bank_details = models.ForeignKey(
        'banking_system.Bank', related_name='shop_bank_detail_payments',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    total_quantity = models.CharField(
        max_length=10, blank=True, null=True, default=1
    )

    sub_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    paid_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    remaining_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    discount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    shipping = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    grand_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    cash_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    cash_returned = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    date = models.DateField(default=timezone.now, blank=True, null=True)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    barcode_image = models.ImageField(upload_to=barcode_upload_path, null=True, blank=True)
    def __str__(self):
        return str(self.id).zfill(7)
    
    def generate_barcode(self):
        unique_id = uuid.uuid4().hex[:10].upper()
        return f"INV{timezone.now().strftime('%Y%m%d')}{unique_id}"

    def generate_barcode_image(self):
        buffer = BytesIO()
        barcode_obj = Code128(self.barcode, writer=ImageWriter())
        barcode_obj.write(buffer)
        file_name = f'invoice_{self.pk}.png'
        self.barcode_image.save(file_name, File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = self.generate_barcode()
        super().save(*args, **kwargs)
        if not self.barcode_image:
            self.generate_barcode_image()
            super().save(update_fields=["barcode_image"])

    def is_installment(self):
        invoice_installments = InvoiceInstallment.objects.filter(
            invoice__id=self.id)

        grand_total = self.grand_total

        if invoice_installments.exists():
            total_paid_amount = invoice_installments.aggregate(
                Sum('paid_amount'))
            total_paid_amount = float(
                total_paid_amount.get('paid_amount__sum') or 0
            )

        else:
            total_paid_amount = 0

        if float(grand_total) <= total_paid_amount:
            return True

        return False

    def remaining_installment(self):
        invoice_installments = InvoiceInstallment.objects.filter(
            invoice__id=self.id)

        grand_total = self.grand_total

        if invoice_installments.exists():
            total_paid_amount = invoice_installments.aggregate(
                Sum('paid_amount'))
            total_paid_amount = float(
                total_paid_amount.get('paid_amount__sum') or 0
            )

        else:
            total_paid_amount = 0

        return float(grand_total) - total_paid_amount

    def has_installment(self):
        if self.shop_invoice_installment.all().exists():
            return True

        return False




class ShopInvoiceInstallment(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name='shop_invoice_installment', on_delete=models.CASCADE)
    paid_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateField(
        default=timezone.now, blank=True, null=True)

    def __str__(self):
        return (
            '%s Installment' % self.invoice.customer.name if
            self.invoice.customer else ''
        )

class BillChecker(models.Model):
    store_invoice = models.ForeignKey(
        Invoice, related_name='store_invoice_checker', on_delete=models.CASCADE, null=True, blank=True)
    shop_invoice = models.ForeignKey(
        ShopInvoice, related_name='shop_invoice_checker', on_delete=models.CASCADE, null=True, blank=True)
    store_invoice_check = models.BooleanField(default=False)
    shop_invoice_check = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return (
            '%s invoice check' % self.created_at if
            self.created_at else ''
        )