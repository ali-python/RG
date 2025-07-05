from django.db import models
from django.utils import timezone
from django.db.models import Sum
import uuid

class ProductCategory(models.Model):
    category = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.category


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='product_category')
    name = models.CharField(max_length=200, null=True, blank=True)
    litre = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                null=True, blank=True)
    quantity = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                   null=True, blank=True)
    unit_price = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                     null=True, blank=True)
    amount = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                 null=True, blank=True)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    notify_qty = models.DecimalField(
        max_digits=65, decimal_places=2, default=0,
        null=True, blank=True
    )
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.barcode:
            print("Generating barcode...")
            self.barcode = self.generate_barcode()
            print(f"Generated barcode: {self.barcode}")
        super().save(*args, **kwargs)
        
    def generate_barcode(self):
        """
        Generate a unique barcode.
        You can customize this logic — for example, add prefix or time-based codes.
        """
        while True:
            code = str(uuid.uuid4().int)[:12]  # 12-digit numeric barcode
            if not Product.objects.filter(barcode=code).exists():
                return code

    def __str__(self):
        return self.name or "Unnamed Product"

    def total_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum('stock_quantity'))
            stock_in = float(obj_stock_in.get('stock_quantity__sum'))
        except:
            stock_in = 0

        return stock_in

    def product_available_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum('stock_quantity'))
            stock_in = float(obj_stock_in.get('stock_quantity__sum'))
        except:
            stock_in = 0
        try:
            obj_stock_out = self.stockout_product.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0

        return stock_in - stock_out


class StockIn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='stockin_product')
    stock_quantity = models.CharField(max_length=200, null=True, blank=True)
    price_per_item = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                         null=True, blank=True)
    total_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                       null=True, blank=True)
    selling_percent = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                       null=True, blank=True)

    buying_price_item = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                            null=True, blank=True,
                                            help_text='Buying Price for a Single Item')
    total_buying_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                              null=True, blank=True)
    buying_percent = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                       null=True, blank=True)
    dated_order = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.product)


class StockOut(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='stockout_product')
    invoice = models.ForeignKey(
        'sales.Invoice', related_name='invoice_stockout', blank=True, null=True, on_delete=models.CASCADE)
    stock_out_quantity = models.DecimalField(max_digits=65, decimal_places=2,
                                             default=0, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                        null=True, blank=True)
    stock_out_store = models.BooleanField(default=False)
    buying_price = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                            null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.product)


class PurchasedItem(models.Model):
    item = models.ForeignKey(
        Product, related_name='purchased_item', on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        'sales.Invoice', related_name='invoice_purchased', on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=65, decimal_places=2, default=1, blank=True, null=True
    )
    price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    purchase_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    date = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.item.name or ''

class ShopProduct(models.Model):
    original_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)  # e.g. kg, litre

    def __str__(self):
        return f"{self.original_product}"
    
    def total_items(self):
        try:
            obj_stock_in = self.shop_stocks.aggregate(Sum('stock_quantity'))
            stock_in = float(obj_stock_in.get('stock_quantity__sum'))
        except:
            stock_in = 0

        return stock_in
    
    def total_pack(self):
        try:
            obj_stock_in = self.shop_stocks.aggregate(Sum('bulk_quantity_quantity'))
            stock_in = float(obj_stock_in.get('bulk_quantity_quantity__sum'))
        except:
            stock_in = 0

        return stock_in

    def product_available_items(self):
        try:
            obj_stock_in = self.shop_stocks.aggregate(Sum('stock_quantity'))
            stock_in = float(obj_stock_in.get('stock_quantity__sum'))
        except:
            stock_in = 0
        try:
            obj_stock_out = self.shop_stockout_product.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0

        return stock_in - stock_out
    
    def product_available_pack(self):
        try:
            obj_stock_in = self.shop_stocks.aggregate(Sum('bulk_quantity_quantity'))
            stock_in = float(obj_stock_in.get('bulk_quantity_quantity__sum'))
        except:
            stock_in = 0
        try:
            obj_stock_out = self.shop_stockout_product.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0

        return stock_in - stock_out
    
class ShopStockIn(models.Model):
    shop_product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, related_name='shop_stocks')
    stock_quantity = models.CharField(max_length=200, null=True, blank=True)
    bulk_quantity_quantity = models.CharField(max_length=200, null=True, blank=True)
    parcel_weight = models.CharField(max_length=200, null=True, blank=True)
    pack_weight = models.CharField(max_length=200, null=True, blank=True)
    number_of_parcel = models.CharField(max_length=200, null=True, blank=True)
    price_per_item = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                         null=True, blank=True)
    total_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                       null=True, blank=True)
    selling_percent = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                       null=True, blank=True)

    buying_price_item = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                            null=True, blank=True,
                                            help_text='Buying Price for a Single Item')
    total_buying_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                              null=True, blank=True)
    buying_percent = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                       null=True, blank=True)
    dated_order = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.shop_product)
    
class ShopStockOut(models.Model):
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='shop_stockout_product')
    invoice = models.ForeignKey(
        'sales.Invoice', related_name='shop_invoice_stockout', blank=True, null=True, on_delete=models.CASCADE)
    stock_out_quantity = models.DecimalField(max_digits=65, decimal_places=2,
                                             default=0, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                        null=True, blank=True)
    buying_price = models.DecimalField(max_digits=65, decimal_places=2, default=0,
                                            null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.product)

class ShopPurchasedItem(models.Model):
    shop_item = models.ForeignKey(
        ShopProduct, related_name='shop_purchased_item', on_delete=models.CASCADE)
    shop_invoice = models.ForeignKey(
        'sales.ShopInvoice', related_name='shop_invoice_purchased', on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=65, decimal_places=2, default=1, blank=True, null=True
    )
    price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    purchase_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    date = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.item.name or ''

class ProductTransfer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_transfers')
    quantity_transferred = models.DecimalField(max_digits=65, decimal_places=2)
    transfer_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Transferred {self.quantity_transferred} of {self.product.name}"