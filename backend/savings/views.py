from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import Account
from transactions.models import Transaction
from .models import SavingsBox, SavingsBoxInterestLog
from .serializers import (
    SavingsBoxSerializer, SavingsBoxInterestLogSerializer,
    DepositToBoxSerializer, WithdrawFromBoxSerializer,
)


class SavingsBoxListView(generics.ListCreateAPIView):
    serializer_class = SavingsBoxSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsBox.objects.filter(user=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class SavingsBoxDetailView(generics.RetrieveAPIView):
    serializer_class = SavingsBoxSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsBox.objects.filter(user=self.request.user.profile)


class DepositToBoxView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        box = SavingsBox.objects.filter(id=pk, user=request.user.profile).first()
        if not box:
            return Response({'detail': 'Cajita no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepositToBoxSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = Account.objects.filter(
            id=serializer.validated_data['account_id'],
            user=request.user.profile
        ).first()
        if not account:
            return Response({'detail': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        amount = serializer.validated_data['amount']
        if account.balance < amount:
            return Response({'detail': 'Saldo insuficiente en la cuenta.'}, status=status.HTTP_400_BAD_REQUEST)

        # Withdraw from account
        Transaction.objects.create(
            account=account, user=request.user.profile, type='expense',
            amount=amount, description=f'Depósito a cajita: {box.name}',
            category='ahorro', icon='🐷'
        )
        # Add to box
        box.balance += amount
        box.save()

        return Response(SavingsBoxSerializer(box).data)


class WithdrawFromBoxView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        box = SavingsBox.objects.filter(id=pk, user=request.user.profile).first()
        if not box:
            return Response({'detail': 'Cajita no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WithdrawFromBoxSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = Account.objects.filter(
            id=serializer.validated_data['account_id'],
            user=request.user.profile
        ).first()
        if not account:
            return Response({'detail': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        amount = serializer.validated_data['amount']
        if box.balance < amount:
            return Response({'detail': 'Saldo insuficiente en la cajita.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deposit to account
        Transaction.objects.create(
            account=account, user=request.user.profile, type='income',
            amount=amount, description=f'Retiro de cajita: {box.name}',
            category='ahorro', icon='🏦'
        )
        # Subtract from box
        box.balance -= amount
        box.save()

        return Response(SavingsBoxSerializer(box).data)


class SavingsBoxInterestLogView(generics.ListAPIView):
    serializer_class = SavingsBoxInterestLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        box = SavingsBox.objects.filter(id=self.kwargs['pk'], user=self.request.user.profile).first()
        if not box:
            return SavingsBoxInterestLog.objects.none()
        return SavingsBoxInterestLog.objects.filter(box=box)