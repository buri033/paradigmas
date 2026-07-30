from django.utils import timezone
from django.db.models import Q
from django.db import transaction as db_transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from accounts.models import Account
from notifications.models import Notification
from transactions.models import Transaction
from .models import MoneyRequest
from .serializers import MoneyRequestSerializer, CreateMoneyRequestSerializer


class MoneyRequestListView(generics.ListAPIView):
    serializer_class = MoneyRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        return MoneyRequest.objects.filter(
            Q(requester=profile) | Q(target=profile)
        )


class CreateMoneyRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateMoneyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_email = serializer.validated_data['target_email']
        try:
            target_user = User.objects.get(email=target_email)
            target_profile = target_user.profile
        except (User.DoesNotExist, Exception):
            return Response({'detail': 'Usuario destino no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if target_profile == request.user.profile:
            return Response({'detail': 'No puedes solicitarte dinero a ti mismo.'}, status=status.HTTP_400_BAD_REQUEST)

        money_request = MoneyRequest.objects.create(
            requester=request.user.profile,
            target=target_profile,
            amount=serializer.validated_data['amount'],
            description=serializer.validated_data['description'],
        )

        # Notify target
        Notification.objects.create(
            user=target_profile,
            title='Nueva solicitud de dinero',
            message=f'{request.user.get_full_name() or request.user.email} te ha solicitado ${serializer.validated_data["amount"]:,} COP.',
            type='info',
        )

        return Response(MoneyRequestSerializer(money_request).data, status=status.HTTP_201_CREATED)


class AcceptMoneyRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        money_request = MoneyRequest.objects.filter(
            id=pk, target=request.user.profile, status='pending'
        ).first()
        if not money_request:
            return Response({'detail': 'Solicitud no encontrada o ya procesada.'}, status=status.HTTP_404_NOT_FOUND)

        # Get accounts
        target_account = Account.objects.filter(user=money_request.target).first()
        requester_account = Account.objects.filter(user=money_request.requester).first()

        if not target_account or not requester_account:
            return Response({'detail': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        if target_account.balance < money_request.amount:
            return Response({'detail': 'Saldo insuficiente.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create transactions atomically
        with db_transaction.atomic():
            Transaction.objects.create(
                account=target_account, user=money_request.target, type='expense',
                amount=money_request.amount,
                description=f'Solicitud de dinero aceptada: {money_request.description}',
                category='solicitud', icon='💸',
                destination_name=money_request.requester.user.get_full_name() or money_request.requester.user.email,
            )
            Transaction.objects.create(
                account=requester_account, user=money_request.requester, type='income',
                amount=money_request.amount,
                description=f'Dinero recibido por solicitud: {money_request.description}',
                category='solicitud', icon='📥',
            )

            money_request.status = 'accepted'
            money_request.responded_at = timezone.now()
            money_request.save()

        # Notify requester
        Notification.objects.create(
            user=money_request.requester,
            title='Solicitud aceptada',
            message=f'{request.user.get_full_name() or request.user.email} aceptó tu solicitud de ${money_request.amount:,} COP.',
            type='success',
        )

        return Response(MoneyRequestSerializer(money_request).data)


class RejectMoneyRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        money_request = MoneyRequest.objects.filter(
            id=pk, target=request.user.profile, status='pending'
        ).first()
        if not money_request:
            return Response({'detail': 'Solicitud no encontrada o ya procesada.'}, status=status.HTTP_404_NOT_FOUND)

        money_request.status = 'rejected'
        money_request.responded_at = timezone.now()
        money_request.save()

        # Notify requester
        Notification.objects.create(
            user=money_request.requester,
            title='Solicitud rechazada',
            message=f'{request.user.get_full_name() or request.user.email} rechazó tu solicitud de ${money_request.amount:,} COP.',
            type='warning',
        )

        return Response(MoneyRequestSerializer(money_request).data)