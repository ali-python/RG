from product.forms import (
    ProductCategoryForm, ProductForm, StockInForm, StockOutForm
)
from product.models import (
    ProductCategory, Product, StockIn, StockOut, ProductTransfer, ShopStockOut
)
from django.db import transaction
from django.views.generic import ListView, FormView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, ShopProduct, ShopStockIn
from django.utils import timezone
from decimal import Decimal

class AddProductCategory(FormView):
    form_class = ProductCategoryForm
    template_name = 'product/add_category.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddProductCategory, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:add'))

    def form_invalid(self, form):
        return super(AddProductCategory, self).form_invalid(form)


class AddProduct(FormView):
    form_class = ProductForm
    template_name = 'product/add_product.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddProduct, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        print(form.errors)
        return super(AddProduct, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddProduct, self).get_context_data(**kwargs)
        category = ProductCategory.objects.all()
        context.update({
            'category': category
        })
        return context


class UpdateProduct(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/update_product.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            UpdateProduct, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        return super(UpdateProduct, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateProduct, self).get_context_data(**kwargs)
        categories = ProductCategory.objects.all()
        context.update({
            'categories': categories
        })
        return context


class ProductList(ListView):
    model = Product
    template_name = 'product/product_list.html'
    paginate_by = 100
    ordering = '-id'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ProductList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Product.objects.all().order_by('-id')

        if self.request.GET.get('product_name'):
            queryset = queryset.filter(
                name__contains=self.request.GET.get('product_name')
            )

        if self.request.GET.get('product_category'):
            queryset = queryset.filter(
                category__category__contains=self.request.GET.get('product_category')
            )

        return queryset.order_by('-id')


class StockInProduct(FormView):
    form_class = StockInForm
    template_name = 'product/add_stock_item.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            StockInProduct, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(reverse('product:stockin_detail',
                                            kwargs={'pk': obj.product.id}))

    def form_invalid(self, form):
        return super(StockInProduct, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StockInProduct, self).get_context_data(**kwargs)
        try:
            product = (
                Product.objects.get(id=self.kwargs.get('pk'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found')
        context.update({
            'product': product
        })
        return context


class StockOutProduct(FormView):
    form_class = StockOutForm
    template_name = 'product/stock_out_item.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            StockOutProduct, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(reverse('product:stockout_detail',
                                            kwargs={'pk': obj.product.id}))

    def form_invalid(self, form):
        return super(StockOutProduct, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StockOutProduct, self).get_context_data(**kwargs)

        try:
            product = (
                Product.objects.get(id=self.kwargs.get('pk'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found')

        context.update({
            'product': product
        })
        return context


class StockInDetail(ListView):
    template_name = 'product/stockin_detail.html'
    paginate_by = 100
    model = StockIn

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            StockInDetail, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = self.queryset

        if not queryset:
            queryset = self.model.objects.filter(
                product__id=self.kwargs.get('pk'))

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                dated_order__icontains=self.request.GET.get('date')
            )

        return queryset.order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            StockInDetail, self).get_context_data(**kwargs)

        try:
            product = Product.objects.get(id=self.kwargs.get('pk'))
        except Product.DoesNotExist:
            raise Http404('Product does not exits!')

        context.update({
            'product': product
        })
        return context


class StockOutDetail(ListView):
    template_name = 'product/stockout_detail.html'
    paginate_by = 100
    model = StockOut

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            StockOutDetail, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = self.queryset

        if not queryset:
            queryset = self.model.objects.filter(
                product__id=self.kwargs.get('pk')).order_by('-date')

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                date__icontains=self.request.GET.get('date')
            )

        return queryset.order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            StockOutDetail, self).get_context_data(**kwargs)

        try:
            product = Product.objects.get(id=self.kwargs.get('pk'))
        except Product.DoesNotExist:
            raise Http404('Product does not exits!')

        context.update({
            'product': product
        })
        return context


@transaction.atomic
def add_shop_product_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        unit = request.POST.get('unit')
        bulk_quantity = Decimal(request.POST.get('bulk_quantity') or 0)
        pack_weight = Decimal(request.POST.get('pack_weight') or 0)
        number_of_parcel = Decimal(request.POST.get('number_of_parcel') or 0)
        parcel_weight = Decimal(request.POST.get('parcel_weight') or 0)
        stock_quantity = Decimal(request.POST.get('stock_quantity') or 0)
        price_per_item = Decimal(request.POST.get('price_per_item') or 0)
        selling_percent = Decimal(request.POST.get('selling_percent') or 0)
        buying_price_item = Decimal(request.POST.get('buying_price_item') or 0)
        buying_percent = Decimal(request.POST.get('buying_percent') or 0)
        dated_order = request.POST.get('dated_order') or timezone.now().date()
        print(number_of_parcel)
        print("___________________________________")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('product:add_shop_product')

        shop_product, created = ShopProduct.objects.get_or_create(
            original_product=product,
            defaults={'unit': unit}
        )

        if not created and unit:
            shop_product.unit = unit
            shop_product.save()
        
        total_amount = price_per_item * bulk_quantity
        total_buying_amount = buying_price_item * bulk_quantity

        # Create ShopStockIn
        ShopStockIn.objects.create(
            shop_product=shop_product,
            bulk_quantity_quantity = stock_quantity,
            parcel_weight = parcel_weight,
            pack_weight = pack_weight,
            number_of_parcel = number_of_parcel,
            stock_quantity=bulk_quantity,
            price_per_item=price_per_item,
            total_amount=total_amount,
            selling_percent=selling_percent,
            buying_price_item=buying_price_item,
            total_buying_amount=total_buying_amount,
            buying_percent=buying_percent,
            dated_order=dated_order
        )

        # Deduct from StockIn and create StockOut (FIFO)
        remaining_qty = stock_quantity
        stockins = StockIn.objects.filter(product=product).order_by('dated_order')
        for stockin in stockins:
            # available_qty = Decimal(stockin.stock_quantity)
            # deduct_qty = min(available_qty, remaining_qty)

            # # Reduce quantity in StockIn
            # stockin.stock_quantity = str(Decimal(stockin.stock_quantity) - deduct_qty)
            # stockin.save()

            # Create StockOut
            StockOut.objects.create(
                product=product,
                stock_out_quantity=bulk_quantity,
                selling_price=price_per_item,
                stock_out_store=True,
                buying_price=buying_price_item,
                date=timezone.now().date()
            )

            remaining_qty -= stock_quantity
            if remaining_qty <= 0:
                break

        if remaining_qty > 0:
            messages.warning(request, f"{remaining_qty} units couldn't be deducted due to low stock.")

        # Create ProductTransfer
        ProductTransfer.objects.create(
            product=product,
            quantity_transferred=stock_quantity,
            transfer_date=timezone.now().date()
        )

        messages.success(request, "Shop product added and transfer completed.")
        return redirect('product:shop_list')

    products = Product.objects.all()
    return render(request, 'product/shop_products_add.html', {'products': products})


class ShopProductList(ListView):
    model = ShopProduct
    template_name = 'product/shop_product_list.html'
    paginate_by = 100
    ordering = '-id'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ShopProductList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = ShopProduct.objects.all().order_by('-id')

        if self.request.GET.get('product_name'):
            queryset = queryset.filter(
                name__contains=self.request.GET.get('product_name')
            )

        if self.request.GET.get('product_category'):
            queryset = queryset.filter(
                category__category__contains=self.request.GET.get('product_category')
            )

        return queryset.order_by('-id')
    

class ShopStockInDetail(ListView):
    template_name = 'product/shop_stockin_detail.html'
    paginate_by = 100
    model = ShopStockIn

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ShopStockInDetail, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = self.queryset

        if not queryset:
            queryset = self.model.objects.filter(
                shop_product__id=self.kwargs.get('pk'))

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                dated_order__icontains=self.request.GET.get('date')
            )

        return queryset.order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            ShopStockInDetail, self).get_context_data(**kwargs)

        try:
            product = ShopProduct.objects.get(id=self.kwargs.get('pk'))
        except ShopProduct.DoesNotExist:
            raise Http404('Product does not exits!')

        context.update({
            'product': product
        })
        return context


class ShopStockOutDetail(ListView):
    template_name = 'product/shop_stockout__detail.html'
    paginate_by = 100
    model = ShopStockOut

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ShopStockOutDetail, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = self.queryset

        if not queryset:
            queryset = self.model.objects.filter(
                product__id=self.kwargs.get('pk')).order_by('-date')

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                date__icontains=self.request.GET.get('date')
            )

        return queryset.order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            ShopStockOutDetail, self).get_context_data(**kwargs)

        try:
            product = ShopProduct.objects.get(id=self.kwargs.get('pk'))
        except ShopProduct.DoesNotExist:
            raise Http404('Product does not exits!')

        context.update({
            'product': product
        })
        return context