from django.db.models import Sum, Count
from django.views.generic import ListView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from sales.models  import BillChecker
from product.models import StockOut, ShopStockOut


class DailyStockLogs(ListView):
    model = StockOut
    template_name = 'logs/daily_logs.html'
    paginate_by = 200
    is_paginated = True

    def __init__(self, *args, **kwargs):
        super(DailyStockLogs, self).__init__(*args, **kwargs)
        self.logs_date = ''
        self.today_date = ''

    def get_queryset(self):
        self.logs_date = self.request.GET.get('date')
        if self.logs_date:
            logs_date = self.logs_date.split('-')
            year = logs_date[0]
            month = logs_date[1]
            day = logs_date[2]

            try:
                queryset = StockOut.objects.filter(
                    date__year=year,
                    date__month=month,
                    date__day=day,
                ).values('product__name').annotate(
                    receipt_item=Count('product__name'),
                    total_qty=Sum('stock_out_quantity')

                )
            except:
                queryset = []
        else:
            self.today_date = timezone.now().date()
            queryset = StockOut.objects.filter(
                date__year=self.today_date.year,
                date__month=self.today_date.month,
                date__day=self.today_date.day,
            ).values('product__name').annotate(
                receipt_item=Count('product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        return queryset.order_by('product__name')

    def get_context_data(self, **kwargs):
        context = super(DailyStockLogs, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset:
            total = queryset.aggregate(Sum('selling_price'))
            total = total.get('selling_price__sum') or 0
        else:
            total = 0

        # Determine date for filtering BillChecker
        if self.logs_date:
            filter_date = self.logs_date
        else:
            filter_date = timezone.now().strftime('%Y-%m-%d')


        from datetime import datetime
        filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()

        # Filter BillChecker by date
        store_invoice_checked_count = BillChecker.objects.filter(
            store_invoice_check=True,
            created_at=filter_date_obj
        ).count()

        shop_invoice_checked_count = BillChecker.objects.filter(
            shop_invoice_check=True,
            created_at=filter_date_obj
        ).count()

        context.update({
            'total': total,
            'today_date': (
                timezone.now().strftime('%Y-%m-%d')
                if self.today_date else None),
            'logs_date': self.logs_date,
            'store_invoice_checked_count': store_invoice_checked_count,
            'shop_invoice_checked_count': shop_invoice_checked_count,
        })
        return context


class MonthlyStockLogs(ListView):
    model = StockOut
    template_name = 'logs/monthly_logs.html'
    paginate_by = 200
    is_paginated = True

    def __init__(self, *args, **kwargs):
        super(MonthlyStockLogs, self).__init__(*args, **kwargs)
        self.logs_month = ''
        self.current_month = ''
        self.year = ''

    def get_queryset(self):
        self.logs_month = self.request.GET.get('month')
        current_date = timezone.now().date()
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        if self.logs_month:
            self.year = current_date.year
            # month = self.logs_month
            # if month < months.index(self.logs_month) + 1:
            #     self.year = self.year - 1

            queryset = StockOut.objects.filter(
                date__year=self.year,
                date__month=months.index(self.logs_month) + 1,
            ).values('product__name').annotate(
                receipt_item=Count('product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        else:
            self.current_month = months[current_date.month - 1]
            self.year = current_date.year
            queryset = StockOut.objects.filter(
                date__year=current_date.year,
                date__month=current_date.month,
            ).values('product__name').annotate(
                receipt_item=Count('product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        return queryset.order_by('product__name')

    def get_context_data(self, **kwargs):
        context = super(MonthlyStockLogs, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset:
            total = queryset.aggregate(Sum('selling_price'))
            total = total.get('selling_price__sum') or 0
        else:
            total = 0

        context.update({
            'total': total,
            'month': self.logs_month or self.current_month,
            'year': self.year
        })
        return context


class ShopDailyStockLogs(ListView):
    model = ShopStockOut
    template_name = 'logs/shop_daily_logs.html'
    paginate_by = 200
    is_paginated = True

    def __init__(self, *args, **kwargs):
        super(ShopDailyStockLogs, self).__init__(*args, **kwargs)
        self.logs_date = ''
        self.today_date = ''

    def get_queryset(self):
        self.logs_date = self.request.GET.get('date')
        if self.logs_date:
            logs_date = self.logs_date.split('-')
            year = logs_date[0]
            month = logs_date[1]
            day = logs_date[2]

            try:
                queryset = ShopStockOut.objects.filter(
                    date__year=year,
                    date__month=month,
                    date__day=day,
                ).values('product__original_product__name').annotate(
                    receipt_item=Count('product__original_product__name'),
                    total_qty=Sum('stock_out_quantity')
                )
            except:
                queryset = []
        else:
            self.today_date = timezone.now().date()
            queryset = ShopStockOut.objects.filter(
                date__year=self.today_date.year,
                date__month=self.today_date.month,
                date__day=self.today_date.day,
            ).values('product__original_product__name').annotate(
                receipt_item=Count('product__original_product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        return queryset.order_by('product__original_product__name')

    def get_context_data(self, **kwargs):
        context = super(ShopDailyStockLogs, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset:
            total = queryset.aggregate(Sum('selling_price'))
            total = total.get('selling_price__sum') or 0
        else:
            total = 0
        context.update({
            'total': total,
            'today_date': (
                timezone.now().strftime('%Y-%m-%d')
                if self.today_date else None),
            'logs_date': self.logs_date,
        })
        return context


class ShopMonthlyStockLogs(ListView):
    model = ShopStockOut
    template_name = 'logs/shop_monthly_logs.html'
    paginate_by = 200
    is_paginated = True

    def __init__(self, *args, **kwargs):
        super(ShopMonthlyStockLogs, self).__init__(*args, **kwargs)
        self.logs_month = ''
        self.current_month = ''
        self.year = ''

    def get_queryset(self):
        self.logs_month = self.request.GET.get('month')
        current_date = timezone.now().date()
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        if self.logs_month:
            self.year = current_date.year
            # month = self.logs_month
            # if month < months.index(self.logs_month) + 1:
            #     self.year = self.year - 1

            queryset = ShopStockOut.objects.filter(
                date__year=self.year,
                date__month=months.index(self.logs_month) + 1,
            ).values('product__original_product__name').annotate(
                receipt_item=Count('product__original_product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        else:
            self.current_month = months[current_date.month - 1]
            self.year = current_date.year
            queryset = ShopStockOut.objects.filter(
                date__year=current_date.year,
                date__month=current_date.month,
            ).values('product__original_product__name').annotate(
                receipt_item=Count('product__original_product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        return queryset.order_by('product__original_product__name')

    def get_context_data(self, **kwargs):
        context = super(ShopMonthlyStockLogs, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset:
            total = queryset.aggregate(Sum('selling_price'))
            total = total.get('selling_price__sum') or 0
        else:
            total = 0

        context.update({
            'total': total,
            'month': self.logs_month or self.current_month,
            'year': self.year
        })
        return context
