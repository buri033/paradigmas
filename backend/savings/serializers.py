from rest_framework import serializers
from .models import SavingsBox, SavingsBoxInterestLog


class SavingsBoxInterestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsBoxInterestLog
        fields = ['id', 'period_start', 'period_end', 'interest_earned', 'balance_before', 'balance_after', 'created_at']


class SavingsBoxSerializer(serializers.ModelSerializer):
    projected_annual_earnings = serializers.SerializerMethodField()

    class Meta:
        model = SavingsBox
        fields = ['id', 'name', 'balance', 'interest_rate', 'is_active', 'projected_annual_earnings', 'created_at']
        read_only_fields = ['id', 'balance', 'created_at']

    def get_projected_annual_earnings(self, obj):
        rate = float(obj.interest_rate) / 100
        projected = obj.balance * ((1 + rate / 365) ** 365 - 1)
        return int(projected)


class DepositToBoxSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    account_id = serializers.UUIDField()


class WithdrawFromBoxSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    account_id = serializers.UUIDField()