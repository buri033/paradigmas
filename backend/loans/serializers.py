from rest_framework import serializers
from .models import Loan, Card


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'loan_name', 'total_amount', 'remaining', 'monthly_fee',
                  'interest_rate', 'total_quotas', 'paid_quotas', 'next_due_date',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'card_name', 'card_type', 'last_four', 'cvv', 'credit_limit',
                  'used_amount', 'expiry_date', 'card_network', 'status', 'color',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PayLoanQuotaSerializer(serializers.Serializer):
    account_id = serializers.UUIDField()


class PayCardSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    account_id = serializers.UUIDField()


class SimulateLoanSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    term = serializers.IntegerField(min_value=1, max_value=360)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=1.15)