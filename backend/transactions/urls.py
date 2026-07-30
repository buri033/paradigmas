from django.urls import path
from .views import (
    TransactionListView, ContactListCreateView, ContactDeleteView,
    TransferView, DepositView, WithdrawalView,
)

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transfers/', TransferView.as_view(), name='transfer'),
    path('deposits/', DepositView.as_view(), name='deposit'),
    path('withdrawals/', WithdrawalView.as_view(), name='withdrawal'),
    path('contacts/', ContactListCreateView.as_view(), name='contact-list'),
    path('contacts/<uuid:pk>/', ContactDeleteView.as_view(), name='contact-delete'),
]