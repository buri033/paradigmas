from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'account_tier', 'hide_balance', 'created_at']
    list_filter = ['role', 'account_tier', 'hide_balance']
    search_fields = ['user__email', 'user__first_name', 'rut']