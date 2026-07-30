from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'account_type', 'user', 'balance', 'currency', 'created_at']
    list_filter = ['account_type', 'currency']
    search_fields = ['account_number', 'alias']