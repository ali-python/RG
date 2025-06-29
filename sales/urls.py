from sales.views import (
    InvoiceListView, CreateInvoiceTemplateView, ProductListAPIView,
    GenerateInvoiceAPIView, InvoiceDetailTemplateView, InvoiceInstallmentListView,
    InvoiceInstallmentFormView, InvoiceInstallmentDeleteView, ShopCreateInvoiceTemplateView, 
    ShopInvoiceListView, ShopProductListAPIView, ShopGenerateInvoiceAPIView, ShopInvoiceDetailTemplateView,
    thermal_print, find_item_by_barcode, find_shop_item_by_barcode)

from django.urls import path
from . import views
urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name='invoice_list'),
    path("invoice/create", CreateInvoiceTemplateView.as_view(), name='invoice_create'),
    path("invoice/<int:pk>/detail", InvoiceDetailTemplateView.as_view(), name='invoice_detail'),
    path("product/list/api/", ProductListAPIView.as_view(), name='product_list_api'),
    path("generate/invoice/api/", GenerateInvoiceAPIView.as_view(), name='generate_invoice_api'),
    path('find-item-by-barcode/', find_item_by_barcode, name='find_item_by_barcode'),
    path('find-shop-item-by-barcode/', find_shop_item_by_barcode, name='find_shop_item_by_barcode'),

    path(
        "invoice/<int:invoice_id>/installments",
        InvoiceInstallmentListView.as_view(),
        name='installment_list'
    ),

    path(
        "invoice/<int:invoice_id>/installment/add",
        InvoiceInstallmentFormView.as_view(),
        name='installment_add'
    ),

    path(
        'installment/<int:pk>/delete',
        InvoiceInstallmentDeleteView.as_view(),
        name='installment_delete')
    ,
    path("shop/invoice/create", ShopCreateInvoiceTemplateView.as_view(), name='shop_invoice_create'),
    path("shop/invoices", ShopInvoiceListView.as_view(), name='shop_invoice_list'),
    path("shop/product/list/api/", ShopProductListAPIView.as_view(), name='shop_product_list_api'),
    path("shop/generate/invoice/api/", ShopGenerateInvoiceAPIView.as_view(), name='shop_generate_invoice_api'),
    path("shop/invoice/<int:pk>/detail/", ShopInvoiceDetailTemplateView.as_view(), name='shop_invoice_detail'),
    path('print-thermal/<int:pk>/',thermal_print, name='thermal_print'),
    path('billchecker/', views.billchecker_page, name='billchecker_page'),
    path('billchecker/table/', views.billchecker_table_data, name='billchecker_table_data'),
    path('billchecker/scan/', views.scan_barcode, name='scan_barcode'),

]
