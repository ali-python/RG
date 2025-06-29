from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from sales.models import Invoice, ShopInvoice
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import datetime
from customer.models import Customer
from product.models import StockOut
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView, RedirectView, UpdateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect,HttpResponse
from common.models import AdminConfiguration
from django.contrib.auth import authenticate



class RegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # register new user in the system
        user = form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        auth_user = authenticate(username=username, password=raw_password)
        auth_login(self.request, auth_user)

        return HttpResponseRedirect(reverse('common:login'))

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)

    def get_context_data(self, **kwargs):       
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context.update({
                'username': self.request.POST.get('username'),
                'password1': self.request.POST.get('password1'),
                'password2': self.request.POST.get('password2')
            })

        return 

class LoginView(FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        try:
            admin_config = AdminConfiguration.objects.get(id=1)
            context.update({
                'config': admin_config
            })
        except AdminConfiguration.DoesNotExist:
            pass
        return context


class LogoutView(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        auth_logout(self.request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('common:login'))


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class MonthlyReports(TemplateView):
    template_name = 'reports/reports.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            MonthlyReports, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MonthlyReports, self).get_context_data(**kwargs)
        data_result = []
        for month in range(60):
            data = {}
            date_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(
                date_month.year, date_month.month
            )
            start_month = datetime.datetime(
                date_month.year, date_month.month, 1)

            end_month = datetime.datetime(
                date_month.year, date_month.month, month_range[1]
            )

            invoice = Invoice.objects.filter(
                date__gt=start_month,
                date__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if invoice.exists():
                commission = invoice.aggregate(
                    Sum('grand_total'))
                grand_total = float(
                    commission.get('grand_total__sum') or 0
                )

            else:
                grand_total = 0

            if invoice.exists():
                cash_payment = invoice.aggregate(
                    Sum('cash_payment'))
                total_cash_payment = float(
                    cash_payment.get(
                        'cash_payment__sum') or 0
                )
            else:
                total_cash_payment = 0

            if invoice.exists():
                quantity = invoice.aggregate(
                    Sum('total_quantity'))
                total_quantity = float(
                    quantity.get(
                        'total_quantity__sum') or 0
                )
            else:
                total_quantity = 0

            customer = Customer.objects.filter(
                date__gt=start_month,
                date__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if customer.exists():
                total_customer = customer.count()

            else:
                total_customer = 0

            data.update({
               'grand_total': grand_total,
               'total_cash_payment': total_cash_payment,
               'total_quantity': total_quantity,
               'total_customer': total_customer,
               'date': start_month.strftime('%b-%y')
            })
            data_result.append(data)

        context.update({
            'results': data_result
        })
        return context

from django.utils.translation import gettext as _

def my_view(request):
    context = {
        'welcome_message': _("Welcome to our site"),
    }
    return render(request, 'my_template.html', context)



class ShopMonthlyReports(TemplateView):
    template_name = 'reports/shop_reports.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ShopMonthlyReports, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ShopMonthlyReports, self).get_context_data(**kwargs)
        data_result = []
        for month in range(60):
            data = {}
            date_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(
                date_month.year, date_month.month
            )
            start_month = datetime.datetime(
                date_month.year, date_month.month, 1)

            end_month = datetime.datetime(
                date_month.year, date_month.month, month_range[1]
            )

            invoice = ShopInvoice.objects.filter(
                date__gt=start_month,
                date__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if invoice.exists():
                commission = invoice.aggregate(
                    Sum('grand_total'))
                grand_total = float(
                    commission.get('grand_total__sum') or 0
                )

            else:
                grand_total = 0

            if invoice.exists():
                cash_payment = invoice.aggregate(
                    Sum('cash_payment'))
                total_cash_payment = float(
                    cash_payment.get(
                        'cash_payment__sum') or 0
                )
            else:
                total_cash_payment = 0

            if invoice.exists():
                quantity = invoice.aggregate(
                    Sum('total_quantity'))
                total_quantity = float(
                    quantity.get(
                        'total_quantity__sum') or 0
                )
            else:
                total_quantity = 0

            customer = Customer.objects.filter(
                date__gt=start_month,
                date__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if customer.exists():
                total_customer = customer.count()

            else:
                total_customer = 0

            data.update({
               'grand_total': grand_total,
               'total_cash_payment': total_cash_payment,
               'total_quantity': total_quantity,
               'total_customer': total_customer,
               'date': start_month.strftime('%b-%y')
            })
            data_result.append(data)

        context.update({
            'results': data_result
        })
        return context



