from datetime import timedelta
from decimal import Decimal
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import Account
from transactions.models import Transaction
from .models import Loan, Card
from .serializers import (
    LoanSerializer, CardSerializer, PayLoanQuotaSerializer,
    PayCardSerializer, SimulateLoanSerializer,
)


class LoanListView(generics.ListAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user.profile)


class PayLoanQuotaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        loan = Loan.objects.filter(id=pk, user=request.user.profile).first()
        if not loan:
            return Response({'detail': 'Crédito no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PayLoanQuotaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = Account.objects.filter(
            id=serializer.validated_data['account_id'],
            user=request.user.profile
        ).first()
        if not account:
            return Response({'detail': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        if account.balance < loan.monthly_fee:
            return Response({'detail': 'Saldo insuficiente.'}, status=status.HTTP_400_BAD_REQUEST)

        if loan.status != 'active':
            return Response({'detail': 'El crédito no está activo.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create transaction
        Transaction.objects.create(
            account=account, user=request.user.profile, type='expense',
            amount=loan.monthly_fee,
            description=f'Pago cuota #{loan.paid_quotas + 1} - {loan.loan_name}',
            category='credito', icon='💳'
        )

        # Update loan
        loan.paid_quotas += 1
        loan.remaining = max(0, loan.remaining - loan.monthly_fee)
        loan.next_due_date = loan.next_due_date + timedelta(days=30)
        if loan.paid_quotas >= loan.total_quotas:
            loan.status = 'paid'
        loan.save()

        return Response(LoanSerializer(loan).data)


class SimulateLoanView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SimulateLoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = float(serializer.validated_data['amount'])
        term = serializer.validated_data['term']
        rate = float(serializer.validated_data['interest_rate']) / 100

        # French amortization formula
        monthly_fee = amount * (rate * (1 + rate) ** term) / ((1 + rate) ** term - 1)
        total_cost = monthly_fee * term
        total_interest = total_cost - amount

        return Response({
            'amount': int(amount),
            'term': term,
            'interest_rate': float(serializer.validated_data['interest_rate']),
            'monthly_fee': int(round(monthly_fee)),
            'total_cost': int(round(total_cost)),
            'total_interest': int(round(total_interest)),
        })


class CardListView(generics.ListAPIView):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user.profile)


class ToggleCardLockView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        card = Card.objects.filter(id=pk, user=request.user.profile).first()
        if not card:
            return Response({'detail': 'Tarjeta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        if card.status == 'active':
            card.status = 'locked'
        elif card.status == 'locked':
            card.status = 'active'
        else:
            return Response({'detail': 'No se puede cambiar el estado de esta tarjeta.'}, status=status.HTTP_400_BAD_REQUEST)

        card.save()
        return Response(CardSerializer(card).data)


class PayCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        card = Card.objects.filter(id=pk, user=request.user.profile).first()
        if not card:
            return Response({'detail': 'Tarjeta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PayCardSerializer(data=request.data)
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

        if amount > card.used_amount:
            return Response(
                {'detail': f'El monto excede la deuda de ${card.used_amount:,} CLP.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create transaction
        Transaction.objects.create(
            account=account, user=request.user.profile, type='expense',
            amount=amount,
            description=f'Pago tarjeta {card.card_name} •• {card.last_four}',
            category='tarjeta', icon='💳'
        )

        # Update card
        card.used_amount = max(0, card.used_amount - amount)
        card.save()

        return Response(CardSerializer(card).data)