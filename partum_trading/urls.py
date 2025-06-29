"""partum_trading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Non-internationalized URLs (admin, api, etc.)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Internationalized URLs (your app URLs)
urlpatterns += i18n_patterns(
    path('', include(('common.urls', 'common'), namespace='common')),
    path('product/', include(('product.urls', 'product'), namespace='product')),
    path('customer/', include(('customer.urls', 'customer'), namespace='customer')),
    path('expense/', include(('expense.urls', 'expense'), namespace='expense')),
    path('sales/', include(('sales.urls', 'sales'), namespace='sales')),
    path('bank_detail/', include(('banking_system.urls', 'bank'), namespace='bank')),
    prefix_default_language=True,  # Don't prefix default language (English)
)

# Static and media files for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)