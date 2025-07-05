from django.shortcuts import render
from django.views.generic import ListView, FormView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from customer.models import Customer, CustomerLedger
from customer.forms import CustomerForm, CustomerLedgerForm


class AddCustomer(FormView):
    form_class = CustomerForm
    template_name = 'customer/add_customer.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddCustomer, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('customer:list'))

    def form_invalid(self, form):
        return super(AddCustomer, self).form_invalid(form)


class CustomerList(ListView):
    model = Customer
    template_name = 'customer/customer_list.html'
    paginate_by = 100
    ordering = '-id'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CustomerList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Customer.objects.all().order_by('-id')

        if self.request.GET.get('customer_name'):
            queryset = queryset.filter(
                name__icontains=self.request.GET.get('customer_name'))

        if self.request.GET.get('customer_id'):
            queryset = queryset.filter(
                cnic=self.request.GET.get('customer_id').lstrip('0')
            )

        return queryset.order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super(CustomerList, self).get_context_data(**kwargs)
        unpaid_total = Customer.total_unpaid_amount() 
        print(unpaid_total)
        print("_________________________")
        context.update({
            'unpaid_total': unpaid_total
        })
        return context





class UpdateCustomer(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/update_customer.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            UpdateCustomer, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('customer:list'))

    def form_invalid(self, form):
        return super(UpdateCustomer, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateCustomer, self).get_context_data(**kwargs)
        customer = Customer.objects.all()
        context.update({
            'customer': customer
        })
        return context


class CustomerLedgerListView(ListView):
    model = CustomerLedger
    template_name = 'customer_ledger/ledger_list.html'
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CustomerLedgerListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = self.queryset

        if not queryset:
            queryset = self.model.objects.filter(
                customer__id=self.kwargs.get('pk')).order_by('-date')

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                date__icontains=self.request.GET.get('date')
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            CustomerLedgerListView, self).get_context_data(**kwargs)

        try:
            customer = Customer.objects.get(id=self.kwargs.get('pk'))
        except Customer.DoesNotExist:
            raise Http404('Customer does not exits!')

        context.update({
            'customer': customer
        })
        return context


class DebitCustomerLedgerFormView(FormView):
    template_name = 'customer_ledger/debit.html'
    form_class = CustomerLedgerForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DebitCustomerLedgerFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse('customer:ledger_list',
                    kwargs={'pk': obj.customer.id}
            )
        )

    def get_context_data(self, **kwargs):
        context = super(
            DebitCustomerLedgerFormView, self).get_context_data(**kwargs)
        try:
            customer = Customer.objects.get(id=self.kwargs.get('pk'))
        except Customer.DoesNotExist:
            raise Http404('Customer does not exits!')

        context.update({
            'customer': customer
        })
        return context


class CreditCustomerLedgerFormView(DebitCustomerLedgerFormView):
    template_name = 'customer_ledger/credit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CreditCustomerLedgerFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            CreditCustomerLedgerFormView, self).get_context_data(**kwargs)
        try:
            customer = Customer.objects.get(id=self.kwargs.get('pk'))
        except Customer.DoesNotExist:
            raise Http404('Customer does not exits!')

        context.update({
            'customer': customer
        })
        return context
