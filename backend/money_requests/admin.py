from django.contrib import admin
from .models import MoneyRequest


@admin.register(MoneyRequest)
class MoneyRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'target', 'amount', 'status', 'created_at', 'responded_at']
    list_filter = ['status']