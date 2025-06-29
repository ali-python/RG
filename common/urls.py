from .views import IndexView, MonthlyReports, LoginView, LogoutView, RegisterView, ShopMonthlyReports
from common.stock_logs import DailyStockLogs, MonthlyStockLogs, ShopDailyStockLogs, ShopMonthlyStockLogs
from django.urls import path
from product.views import ProductList

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('reports/monthly', MonthlyReports.as_view(), name='reports'),
    path('reports/shop_monthly', ShopMonthlyReports.as_view(), name='shop_reports'),
    path('logs/daily', DailyStockLogs.as_view(), name='daily_logs'),
    path('shop/logs/daily', ShopDailyStockLogs.as_view(), name='shop_daily_logs'),
    path('logs/monthly', MonthlyStockLogs.as_view(), name='monthly_logs'),
    path('shop/logs/monthly', ShopMonthlyStockLogs.as_view(), name='shop_monthly_logs'),
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
]
