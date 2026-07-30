from rest_framework import serializers
from .models import Transaction, Contact


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'type', 'amount', 'description', 'category',
                  'icon', 'reference', 'destination_name', 'destination_account', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'bank', 'rut', 'account_number', 'avatar_color', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransferSerializer(serializers.Serializer):
    destination_account = serializers.CharField(max_length=20)
    destination_name = serializers.CharField(max_length=100)
    amount = serializers.IntegerField(min_value=1)
    description = serializers.CharField(max_length=200, required=False, default='Transferencia')
    category = serializers.CharField(max_length=50, required=False, default='transferencia')
    account_id = serializers.UUIDField()


class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    description = serializers.CharField(max_length=200, required=False, default='Depósito')
    account_id = serializers.UUIDField()


class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    description = serializers.CharField(max_length=200, required=False, default='Retiro')
    account_id = serializers.UUIDField()