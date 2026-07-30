from django.urls import path
from .views import (
    SavingsBoxListView, SavingsBoxDetailView,
    DepositToBoxView, WithdrawFromBoxView, SavingsBoxInterestLogView,
)

urlpatterns = [
    path('savings-boxes/', SavingsBoxListView.as_view(), name='savings-box-list'),
    path('savings-boxes/<uuid:pk>/', SavingsBoxDetailView.as_view(), name='savings-box-detail'),
    path('savings-boxes/<uuid:pk>/deposit/', DepositToBoxView.as_view(), name='savings-box-deposit'),
    path('savings-boxes/<uuid:pk>/withdraw/', WithdrawFromBoxView.as_view(), name='savings-box-withdraw'),
    path('savings-boxes/<uuid:pk>/interest-log/', SavingsBoxInterestLogView.as_view(), name='savings-box-interest-log'),
]