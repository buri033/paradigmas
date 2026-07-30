from django.urls import path
from .views import (
    MoneyRequestListView, CreateMoneyRequestView,
    AcceptMoneyRequestView, RejectMoneyRequestView,
)

urlpatterns = [
    path('money-requests/', MoneyRequestListView.as_view(), name='money-request-list'),
    path('money-requests/create/', CreateMoneyRequestView.as_view(), name='money-request-create'),
    path('money-requests/<uuid:pk>/accept/', AcceptMoneyRequestView.as_view(), name='money-request-accept'),
    path('money-requests/<uuid:pk>/reject/', RejectMoneyRequestView.as_view(), name='money-request-reject'),
]