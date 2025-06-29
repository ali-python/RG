from django.contrib import admin
from product.models import (
    ProductCategory, Product, StockIn, StockOut, PurchasedItem, ProductTransfer, ShopProduct,
    ShopStockIn,
    ShopStockOut
)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category', 'date'
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'name', 'category', 'litre', 'quantity', 'unit_price', 'notify_qty', 'date'
    )

    @staticmethod
    def category(obj):
        return obj.ProductCategory.category


class StockInAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'category_name', 'stock_quantity', 'price_per_item',
        'total_amount', 'buying_price_item', 'total_buying_amount', 'dated_order'
    )

    @staticmethod
    def category_name(obj):
        return obj.product.category


class StockOutAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'category', 'invoice', 'stock_out_quantity', 'selling_price', 'buying_price', 'date'
    )

    @staticmethod
    def category(obj):
        return obj.product.category

    @staticmethod
    def invoice(obj):
        return str(obj.invoice.id).zfill(7) if obj.invoice else ''


class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'invoice', 'quantity', 'price', 'purchase_amount', 'date'
    )

    @staticmethod
    def invoice(obj):
        return str(obj.invoice.id).zfill(7)


@admin.register(ProductTransfer)
class ProductTransferAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_transferred', 'transfer_date')
    list_filter = ('transfer_date',)
    search_fields = ('product__name',)
    date_hierarchy = 'transfer_date'


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('original_product', 'unit')
    search_fields = ('original_product', 'unit')


@admin.register(ShopStockIn)
class ShopStockInAdmin(admin.ModelAdmin):
    list_display = (
        'shop_product', 'stock_quantity', 'price_per_item', 'total_amount',
        'buying_price_item', 'total_buying_amount', 'dated_order'
    )
    list_filter = ('dated_order',)
    search_fields = ('shop_product__name',)
    date_hierarchy = 'dated_order'


@admin.register(ShopStockOut)
class ShopStockOutAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'invoice', 'stock_out_quantity', 'selling_price',
        'buying_price', 'date'
    )
    list_filter = ('date',)
    search_fields = ('product__name', 'invoice__invoice_number')
    date_hierarchy = 'date'

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
admin.site.register(PurchasedItem, PurchasedItemAdmin)
