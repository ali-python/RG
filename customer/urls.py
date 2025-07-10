from django.urls import path
from customer.views import (
    AddCustomer, CustomerList, UpdateCustomer,
    CustomerLedgerListView, DebitCustomerLedgerFormView,
    CreditCustomerLedgerFormView,CustomerLedgerUpdateView, CustomerLedgerCreditUpdateView
)

urlpatterns = [
    path('add/', AddCustomer.as_view(), name='add'),
    path('list/', CustomerList.as_view(), name='list'),
    path('update/<int:pk>/', UpdateCustomer.as_view(), name='update'),
    path(
        '<int:pk>/ledger/list/',
        CustomerLedgerListView.as_view(),
        name='ledger_list'
    ),
    path(
        '<int:pk>/ledger/debit/',
        DebitCustomerLedgerFormView.as_view(),
        name='ledger_debit'
    ),
    path(
        '<int:pk>/ledger/credit/',
        CreditCustomerLedgerFormView.as_view(),
        name='ledger_credit'
    ),
    path('ledger/update/<int:pk>/', CustomerLedgerUpdateView.as_view(), name='ledger_update'),
    path('ledger/credit/update/<int:pk>/', CustomerLedgerCreditUpdateView.as_view(), name='ledger_credit_update'),

]