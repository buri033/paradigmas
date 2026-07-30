from django.contrib import admin
from .models import SavingsBox, SavingsBoxInterestLog


@admin.register(SavingsBox)
class SavingsBoxAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'balance', 'interest_rate', 'is_active', 'created_at']
    list_filter = ['is_active', 'interest_rate']


@admin.register(SavingsBoxInterestLog)
class SavingsBoxInterestLogAdmin(admin.ModelAdmin):
    list_display = ['box', 'period_start', 'period_end', 'interest_earned', 'balance_before', 'balance_after']