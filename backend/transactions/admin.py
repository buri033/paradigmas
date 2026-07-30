from django.contrib import admin
from .models import Transaction, Contact


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'amount', 'description', 'created_at']
    list_filter = ['type', 'category']
    search_fields = ['description', 'destination_name']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank', 'account_number', 'user', 'created_at']
    search_fields = ['name', 'rut']