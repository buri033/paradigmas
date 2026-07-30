from django.urls import path
from .views import AccountListView, AccountDetailView

urlpatterns = [
    path('accounts/', AccountListView.as_view(), name='account-list'),
    path('accounts/<uuid:pk>/', AccountDetailView.as_view(), name='account-detail'),
]