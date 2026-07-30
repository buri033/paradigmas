from django.urls import path
from .views import (
    LoanListView, PayLoanQuotaView, SimulateLoanView,
    CardListView, ToggleCardLockView, PayCardView,
)

urlpatterns = [
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('loans/<uuid:pk>/pay-quota/', PayLoanQuotaView.as_view(), name='loan-pay-quota'),
    path('loans/simulate/', SimulateLoanView.as_view(), name='loan-simulate'),
    path('cards/', CardListView.as_view(), name='card-list'),
    path('cards/<uuid:pk>/toggle-lock/', ToggleCardLockView.as_view(), name='card-toggle-lock'),
    path('cards/<uuid:pk>/pay/', PayCardView.as_view(), name='card-pay'),
]