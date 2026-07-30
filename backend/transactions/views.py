from django.db import transaction as db_transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import Account
from .models import Transaction, Contact
from .serializers import (
    TransactionSerializer, ContactSerializer,
    TransferSerializer, DepositSerializer, WithdrawalSerializer,
)


class TransactionListView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class ContactListCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class ContactDeleteView(generics.DestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user.profile)


class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @db_transaction.atomic
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender_account = Account.objects.filter(
            id=serializer.validated_data['account_id'],
            user=request.user.profile
        ).first()

        if not sender_account:
            return Response({'detail': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        amount = serializer.validated_data['amount']
        if sender_account.balance < amount:
            return Response({'detail': 'Saldo insuficiente.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create expense on sender
        Transaction.objects.create(
            account=sender_account,
            user=request.user.profile,
            type='transfer',
            amount=amount,
            description=serializer.validated_data.get('description', 'Transferencia'),
            category=serializer.validated_data.get('category', 'transferencia'),
            icon='💸',
            destination_name=serializer.validated_data['destination_name'],
            destination_account=serializer.validated_data['destination_account'],
        )

        # Try to find destination account for income transaction
        dest_account = Account.objects.filter(
            account_number=serializer.validated_data['destination_account']
        ).first()
        if dest_account:
            Transaction.objects.create(
                account=dest_account,
                user=dest_account.user,
                type='income',
                amount=amount,
                description=f'Transferencia de {request.user.get_full_name() or request.user.email}',
                category='transferencia',
                icon='📥',
            )

        return Response({'detail': 'Transferencia exitosa.'}, status=status.HTTP_200_OK)


class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = Account.objects.filter(
            id=serializer.validated_data['account_id'],
            user=request.user.profile
        ).first()

        if not account:
            return Response({'detail': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        txn = Transaction.objects.create(
            account=account,
            user=request.user.profile,
            type='income',
            amount=serializer.validated_data['amount'],
            description=serializer.validated_data.get('description', 'Depósito'),
            category='deposito',
            icon='💵',
        )

        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)


class WithdrawalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WithdrawalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = Account.objects.filter(
            id=serializer.validated_data['account_id'],
            user=request.user.profile
        ).first()

        if not account:
            return Response({'detail': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        amount = serializer.validated_data['amount']
        if account.balance < amount:
            return Response({'detail': 'Saldo insuficiente.'}, status=status.HTTP_400_BAD_REQUEST)

        txn = Transaction.objects.create(
            account=account,
            user=request.user.profile,
            type='expense',
            amount=amount,
            description=serializer.validated_data.get('description', 'Retiro'),
            category='retiro',
            icon='🏧',
        )

        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)