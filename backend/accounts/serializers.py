from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    display_balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'account_type', 'account_number', 'alias', 'balance', 'display_balance', 'currency', 'created_at', 'updated_at']
        read_only_fields = ['id', 'account_number', 'balance', 'created_at', 'updated_at']

    def get_display_balance(self, obj):
        if obj.user.hide_balance:
            return '***'
        return obj.balance