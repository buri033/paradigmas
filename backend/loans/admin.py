from django.contrib import admin
from .models import Loan, Card


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['loan_name', 'user', 'total_amount', 'remaining', 'status', 'next_due_date']
    list_filter = ['status']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['card_name', 'user', 'last_four', 'card_type', 'status', 'used_amount', 'credit_limit']
    list_filter = ['status', 'card_type', 'card_network']