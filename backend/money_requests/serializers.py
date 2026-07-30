from rest_framework import serializers
from .models import MoneyRequest


class MoneyRequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.user.get_full_name', read_only=True)
    requester_email = serializers.CharField(source='requester.user.email', read_only=True)
    target_name = serializers.CharField(source='target.user.get_full_name', read_only=True)
    target_email = serializers.CharField(source='target.user.email', read_only=True)

    class Meta:
        model = MoneyRequest
        fields = ['id', 'requester', 'requester_name', 'requester_email',
                  'target', 'target_name', 'target_email',
                  'amount', 'description', 'status', 'created_at', 'responded_at']
        read_only_fields = ['id', 'requester', 'status', 'created_at', 'responded_at']


class CreateMoneyRequestSerializer(serializers.Serializer):
    target_email = serializers.EmailField()
    amount = serializers.IntegerField(min_value=1)
    description = serializers.CharField(max_length=200)