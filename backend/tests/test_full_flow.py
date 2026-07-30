"""
DuckBank — Test Suite: Flujo Completo entre Dos Usuarios
=========================================================

Crea dos usuarios (Ana y Bob) y prueba todas las funcionalidades
del banco: registro, login, depósitos, retiros, transferencias,
cajitas de ahorro, créditos, tarjetas, notificaciones y
solicitudes de dinero P2P.

Ejecutar:
    cd backend
    pytest tests/ -v
"""

import pytest
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Account
from transactions.models import Transaction, Contact
from savings.models import SavingsBox
from loans.models import Loan, Card
from notifications.models import Notification
from money_requests.models import MoneyRequest


# ──────────────────────────────────────────────────────────────
# 1. REGISTRO Y LOGIN
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestAuth:
    """Registro y login de usuarios."""

    def test_register_user(self, client_a, user_a):
        """El usuario A fue creado correctamente y tiene profile."""
        assert user_a.username == 'ana@duckbank.cl'
        assert user_a.profile is not None
        assert user_a.profile.role == 'user'

    def test_register_second_user(self, client_b, user_b):
        """El usuario B fue creado correctamente y tiene profile."""
        assert user_b.username == 'bob@duckbank.cl'
        assert user_b.profile is not None

    def test_login_returns_tokens(self, client_a):
        """El JWT token permite acceder a endpoints protegidos."""
        resp = client_a.get('/api/profile/')
        assert resp.status_code == 200
        assert resp.data['rut'] == '11111111-1'

    def test_duplicate_email_registration(self, db):
        """No se puede registrar un usuario con email duplicado."""
        from rest_framework.test import APIClient
        client = APIClient()
        # First registration
        resp = client.post('/api/auth/register/', {
            'email': 'nuevo@duckbank.cl',
            'password': 'nuevo12345',
            'full_name': 'Nuevo Usuario',
        }, format='json')
        assert resp.status_code == 201
        # Duplicate
        resp2 = client.post('/api/auth/register/', {
            'email': 'nuevo@duckbank.cl',
            'password': 'nuevo12345',
            'full_name': 'Otro Nombre',
        }, format='json')
        assert resp2.status_code == 400


# ──────────────────────────────────────────────────────────────
# 2. PERFIL Y OCULTAR SALDO
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestProfile:
    """Perfil y mostrar/ocultar saldo."""

    def test_get_profile(self, client_a, user_a):
        """GET /api/profile/ devuelve los datos del usuario autenticado."""
        resp = client_a.get('/api/profile/')
        assert resp.status_code == 200
        assert resp.data['rut'] == '11111111-1'
        assert resp.data['phone'] == '+573001111111'

    def test_update_profile(self, client_a):
        """PATCH /api/profile/ actualiza campos del perfil."""
        resp = client_a.patch('/api/profile/', {
            'phone': '+573009999999',
        }, format='json')
        assert resp.status_code == 200
        assert resp.data['phone'] == '+573009999999'

    def test_toggle_balance_hides_balance(self, client_a):
        """POST /api/profile/toggle-balance/ alterna hide_balance."""
        resp = client_a.post('/api/profile/toggle-balance/')
        assert resp.status_code == 200
        assert resp.data['hide_balance'] is True

        # Now check account shows '***'
        resp2 = client_a.get('/api/accounts/')
        assert resp2.status_code == 200
        assert resp2.data['results'][0]['display_balance'] == '***'

    def test_toggle_balance_shows_balance(self, client_a):
        """Toggling twice restores balance visibility."""
        client_a.post('/api/profile/toggle-balance/')  # hide
        resp = client_a.post('/api/profile/toggle-balance/')  # show
        assert resp.status_code == 200
        assert resp.data['hide_balance'] is False


# ──────────────────────────────────────────────────────────────
# 3. CUENTAS
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestAccounts:
    """Cuentas digitales."""

    def test_user_has_default_account(self, user_a):
        """Al crear un usuario, se le crea automáticamente una Cuenta Vista."""
        accounts = Account.objects.filter(user=user_a.profile)
        assert accounts.count() == 1
        acc = accounts.first()
        assert acc.account_type == 'vista'
        assert acc.alias == 'Cuenta Vista'
        assert acc.balance == 4850900

    def test_list_accounts(self, client_a):
        """GET /api/accounts/ lista las cuentas del usuario."""
        resp = client_a.get('/api/accounts/')
        assert resp.status_code == 200
        assert len(resp.data['results']) >= 1
        acc = resp.data['results'][0]
        assert acc['account_type'] == 'vista'
        assert acc['balance'] == 4850900

    def test_account_detail(self, client_a, account_a):
        """GET /api/accounts/{id}/ devuelve detalle de la cuenta."""
        resp = client_a.get(f'/api/accounts/{account_a.id}/')
        assert resp.status_code == 200
        assert resp.data['currency'] == 'COP'

    def test_cannot_access_other_users_account(self, client_b, account_a):
        """Un usuario no puede ver la cuenta de otro usuario."""
        resp = client_b.get(f'/api/accounts/{account_a.id}/')
        assert resp.status_code == 404


# ──────────────────────────────────────────────────────────────
# 4. DEPÓSITOS Y RETIROS
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestDepositsAndWithdrawals:
    """Depósitos y retiros."""

    def test_deposit(self, client_a, account_a):
        """POST /api/deposits/ agrega dinero a la cuenta."""
        initial_balance = account_a.balance
        resp = client_a.post('/api/deposits/', {
            'amount': 500000,
            'account_id': str(account_a.id),
            'description': 'Depósito de prueba',
        }, format='json')
        assert resp.status_code == 201
        account_a.refresh_from_db()
        assert account_a.balance == initial_balance + 500000

    def test_withdrawal(self, client_a, account_a):
        """POST /api/withdrawals/ retira dinero de la cuenta."""
        initial_balance = account_a.balance
        resp = client_a.post('/api/withdrawals/', {
            'amount': 200000,
            'account_id': str(account_a.id),
            'description': 'Retiro de prueba',
        }, format='json')
        assert resp.status_code == 201
        account_a.refresh_from_db()
        assert account_a.balance == initial_balance - 200000

    def test_withdrawal_insufficient_funds(self, client_a, account_a):
        """No se puede retirar más del saldo disponible."""
        resp = client_a.post('/api/withdrawals/', {
            'amount': 999999999,
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 400
        assert 'insuficiente' in str(resp.data).lower() or 'Saldo insuficiente' in str(resp.data)


# ──────────────────────────────────────────────────────────────
# 5. TRANSFERENCIAS
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestTransfers:
    """Transferencias entre usuarios."""

    def test_transfer_between_users(self, client_a, client_b, user_a, user_b, account_a, account_b):
        """POST /api/transfers/ transfiere dinero de A a B."""
        initial_a = account_a.balance
        initial_b = account_b.balance
        transfer_amount = 100000

        resp = client_a.post('/api/transfers/', {
            'account_id': str(account_a.id),
            'destination_account': account_b.account_number,
            'destination_name': 'Bob Gómez',
            'amount': transfer_amount,
            'description': 'Transferencia de prueba',
        }, format='json')
        assert resp.status_code == 200

        # Verify sender balance decreased
        account_a.refresh_from_db()
        assert account_a.balance == initial_a - transfer_amount

        # Verify receiver balance increased (signal handles it)
        account_b.refresh_from_db()
        assert account_b.balance == initial_b + transfer_amount

    def test_transfer_insufficient_funds(self, client_a, account_a, account_b):
        """No se puede transferir más de lo que se tiene."""
        resp = client_a.post('/api/transfers/', {
            'account_id': str(account_a.id),
            'destination_account': account_b.account_number,
            'destination_name': 'Bob Gómez',
            'amount': 999999999,
        }, format='json')
        assert resp.status_code == 400
        assert 'insuficiente' in str(resp.data).lower() or 'Saldo insuficiente' in str(resp.data)

    def test_transfer_creates_transactions(self, client_a, account_a, account_b, user_a):
        """Una transferencia crea dos transacciones: gasto para A, ingreso para B."""
        client_a.post('/api/transfers/', {
            'account_id': str(account_a.id),
            'destination_account': account_b.account_number,
            'destination_name': 'Bob Gómez',
            'amount': 50000,
        }, format='json')

        # Sender transaction
        sender_tx = Transaction.objects.filter(
            user=user_a.profile, type='transfer', amount=50000
        )
        assert sender_tx.exists()

        # Receiver transaction
        receiver_tx = Transaction.objects.filter(
            account=account_b, type='income', amount=50000
        )
        assert receiver_tx.exists()


# ──────────────────────────────────────────────────────────────
# 6. CAJITAS DE AHORRO
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestSavingsBoxes:
    """Cajitas de ahorro con interés compuesto."""

    def test_create_savings_box(self, client_a, user_a):
        """POST /api/savings-boxes/ crea una nueva cajita."""
        resp = client_a.post('/api/savings-boxes/', {
            'name': 'Vacaciones',
        }, format='json')
        assert resp.status_code == 201
        assert resp.data['name'] == 'Vacaciones'
        assert resp.data['balance'] == 0
        assert float(resp.data['interest_rate']) == 11.0

    def test_list_savings_boxes(self, client_a, user_a):
        """GET /api/savings-boxes/ lista las cajitas del usuario."""
        SavingsBox.objects.create(user=user_a.profile, name='Cajita 1')
        SavingsBox.objects.create(user=user_a.profile, name='Cajita 2')

        resp = client_a.get('/api/savings-boxes/')
        assert resp.status_code == 200
        assert len(resp.data['results']) == 2

    def test_deposit_to_savings_box(self, client_a, user_a, account_a):
        """POST /api/savings-boxes/{id}/deposit/ deposita dinero en la cajita."""
        box = SavingsBox.objects.create(user=user_a.profile, name='Viaje')

        resp = client_a.post(f'/api/savings-boxes/{box.id}/deposit/', {
            'amount': 200000,
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 200
        assert resp.data['balance'] == 200000

        # Account balance should decrease
        account_a.refresh_from_db()
        assert account_a.balance == 4850900 - 200000

    def test_withdraw_from_savings_box(self, client_a, user_a, account_a):
        """POST /api/savings-boxes/{id}/withdraw/ retira dinero de la cajita."""
        box = SavingsBox.objects.create(user=user_a.profile, name='Viaje', balance=300000)

        resp = client_a.post(f'/api/savings-boxes/{box.id}/withdraw/', {
            'amount': 50000,
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 200
        assert resp.data['balance'] == 250000

        # Account balance should increase
        account_a.refresh_from_db()
        assert account_a.balance == 4850900 + 50000

    def test_withdraw_exceeds_savings_balance(self, client_a, user_a, account_a):
        """No se puede retirar más de lo que tiene la cajita."""
        box = SavingsBox.objects.create(user=user_a.profile, name='Chica', balance=10000)

        resp = client_a.post(f'/api/savings-boxes/{box.id}/withdraw/', {
            'amount': 999999,
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 400
        assert 'insuficiente' in str(resp.data).lower()

    def test_projected_annual_earnings(self, client_a, user_a):
        """La cajita calcula la ganancia proyectada anual con interés compuesto."""
        box = SavingsBox.objects.create(user=user_a.profile, name='Ahorro', balance=1000000)

        resp = client_a.get(f'/api/savings-boxes/{box.id}/')
        assert resp.status_code == 200
        # 11% annual compound: 1,000,000 * ((1 + 0.11/365)^365 - 1) ≈ 115,000+
        projected = resp.data['projected_annual_earnings']
        assert projected > 100000  # At minimum ~11% of 1M

    def test_cannot_deposit_more_than_account_balance(self, client_a, user_a, account_a):
        """No se puede depositar más del saldo de la cuenta a la cajita."""
        box = SavingsBox.objects.create(user=user_a.profile, name='Grande')

        resp = client_a.post(f'/api/savings-boxes/{box.id}/deposit/', {
            'amount': 999999999,
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 400


# ──────────────────────────────────────────────────────────────
# 7. SIMULADOR DE CRÉDITO
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestLoanSimulator:
    """Simulador de crédito (amortización francesa)."""

    def test_simulate_loan(self, db):
        """POST /api/loans/simulate/ calcula la cuota mensual (sin auth)."""
        from rest_framework.test import APIClient
        client = APIClient()  # No auth needed for simulate

        resp = client.post('/api/loans/simulate/', {
            'amount': 5000000,
            'term': 24,
            'interest_rate': 1.15,
        }, format='json')
        assert resp.status_code == 200
        assert resp.data['monthly_fee'] > 0
        assert resp.data['total_cost'] > resp.data['amount']
        assert resp.data['total_interest'] == resp.data['total_cost'] - resp.data['amount']

        # Verify French amortization formula manually
        # M = P * r * (1+r)^n / ((1+r)^n - 1)
        import math
        P = 5000000
        r = 0.0115
        n = 24
        expected_fee = P * r * (1 + r) ** n / ((1 + r) ** n - 1)
        assert abs(resp.data['monthly_fee'] - round(expected_fee)) < 2

    def test_simulate_loan_default_rate(self, db):
        """El simulador usa tasa 1.15% por defecto si no se especifica."""
        from rest_framework.test import APIClient
        client = APIClient()

        resp = client.post('/api/loans/simulate/', {
            'amount': 1000000,
            'term': 12,
        }, format='json')
        assert resp.status_code == 200
        assert float(resp.data['interest_rate']) == 1.15


# ──────────────────────────────────────────────────────────────
# 8. CRÉDITOS Y TARJETAS
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestLoansAndCards:
    """Créditos y tarjetas."""

    def test_list_loans(self, client_a, user_a):
        """GET /api/loans/ lista los créditos del usuario."""
        Loan.objects.create(
            user=user_a.profile,
            loan_name='Crédito de Consumo',
            total_amount=5000000,
            remaining=3220000,
            monthly_fee=185000,
            interest_rate=1.15,
            total_quotas=24,
            paid_quotas=12,
            next_due_date='2025-12-15',
            status='active',
        )
        resp = client_a.get('/api/loans/')
        assert resp.status_code == 200
        results = resp.data.get('results', resp.data)
        assert len(results) >= 1
        assert results[0]['loan_name'] == 'Crédito de Consumo'

    def test_pay_loan_quota(self, client_a, user_a, account_a):
        """POST /api/loans/{id}/pay-quota/ paga una cuota del crédito."""
        loan = Loan.objects.create(
            user=user_a.profile,
            loan_name='Crédito Test',
            total_amount=2000000,
            remaining=1000000,
            monthly_fee=100000,
            interest_rate=1.15,
            total_quotas=10,
            paid_quotas=5,
            next_due_date='2025-12-15',
            status='active',
        )
        initial_balance = account_a.balance

        resp = client_a.post(f'/api/loans/{loan.id}/pay-quota/', {
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 200
        assert resp.data['paid_quotas'] == 6
        assert resp.data['remaining'] == 900000

        # Balance decreased
        account_a.refresh_from_db()
        assert account_a.balance == initial_balance - 100000

    def test_pay_loan_insufficient_funds(self, client_a, user_a, account_a):
        """No se puede pagar una cuota si no hay saldo suficiente."""
        loan = Loan.objects.create(
            user=user_a.profile,
            loan_name='Crédito Caro',
            total_amount=999999999,
            remaining=999999999,
            monthly_fee=999999999,
            interest_rate=1.15,
            total_quotas=10,
            paid_quotas=0,
            next_due_date='2025-12-15',
            status='active',
        )
        resp = client_a.post(f'/api/loans/{loan.id}/pay-quota/', {
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 400

    def test_list_cards(self, client_a, user_a):
        """GET /api/cards/ lista las tarjetas del usuario."""
        Card.objects.create(
            user=user_a.profile,
            card_name='Duck Visa',
            card_type='credit',
            last_four='1234',
            cvv='567',
            credit_limit=2000000,
            used_amount=300000,
            expiry_date='12/28',
        )
        resp = client_a.get('/api/cards/')
        assert resp.status_code == 200
        results = resp.data.get('results', resp.data)
        assert len(results) >= 1
        assert results[0]['last_four'] == '1234'

    def test_toggle_card_lock(self, client_a, user_a):
        """POST /api/cards/{id}/toggle-lock/ alterna entre bloqueada y activa."""
        card = Card.objects.create(
            user=user_a.profile,
            card_name='Duck Visa',
            card_type='credit',
            last_four='5678',
            cvv='123',
            credit_limit=2000000,
            used_amount=0,
            expiry_date='06/27',
        )
        # Lock
        resp = client_a.post(f'/api/cards/{card.id}/toggle-lock/')
        assert resp.status_code == 200
        assert resp.data['status'] == 'locked'

        # Unlock
        resp2 = client_a.post(f'/api/cards/{card.id}/toggle-lock/')
        assert resp2.status_code == 200
        assert resp2.data['status'] == 'active'

    def test_pay_card(self, client_a, user_a, account_a):
        """POST /api/cards/{id}/pay/ paga deuda de la tarjeta."""
        card = Card.objects.create(
            user=user_a.profile,
            card_name='Duck Visa',
            card_type='credit',
            last_four='9999',
            cvv='456',
            credit_limit=2000000,
            used_amount=300000,
            expiry_date='03/27',
        )
        initial_balance = account_a.balance

        resp = client_a.post(f'/api/cards/{card.id}/pay/', {
            'amount': 100000,
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 200
        assert resp.data['used_amount'] == 200000

        # Balance decreased
        account_a.refresh_from_db()
        assert account_a.balance == initial_balance - 100000

    def test_pay_card_exceeds_debt(self, client_a, user_a, account_a):
        """No se puede pagar más de la deuda de la tarjeta."""
        card = Card.objects.create(
            user=user_a.profile,
            card_name='Duck Visa',
            card_type='credit',
            last_four='8888',
            cvv='789',
            credit_limit=2000000,
            used_amount=50000,
            expiry_date='01/26',
        )
        resp = client_a.post(f'/api/cards/{card.id}/pay/', {
            'amount': 999999,
            'account_id': str(account_a.id),
        }, format='json')
        assert resp.status_code == 400
        assert 'excede' in str(resp.data).lower()


# ──────────────────────────────────────────────────────────────
# 9. NOTIFICACIONES
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestNotifications:
    """Notificaciones."""

    def test_list_notifications(self, client_a, user_a):
        """GET /api/notifications/ lista las notificaciones del usuario."""
        Notification.objects.create(user=user_a.profile, title='Test', message='Mensaje', type='info')
        Notification.objects.create(user=user_a.profile, title='Test 2', message='Otro', type='success')

        resp = client_a.get('/api/notifications/')
        assert resp.status_code == 200
        assert len(resp.data['results']) == 2

    def test_filter_unread_notifications(self, client_a, user_a):
        """GET /api/notifications/?unread=true filtra solo no leídas."""
        Notification.objects.create(user=user_a.profile, title='Leída', message='X', type='info', is_read=True)
        Notification.objects.create(user=user_a.profile, title='No leída', message='Y', type='info', is_read=False)

        resp = client_a.get('/api/notifications/?unread=true')
        assert resp.status_code == 200
        assert len(resp.data['results']) == 1
        assert resp.data['results'][0]['is_read'] is False

    def test_mark_notification_read(self, client_a, user_a):
        """POST /api/notifications/{id}/read/ marca una notificación como leída."""
        notif = Notification.objects.create(user=user_a.profile, title='Nueva', message='X', type='info')

        resp = client_a.post(f'/api/notifications/{notif.id}/read/')
        assert resp.status_code == 200
        assert resp.data['is_read'] is True

    def test_mark_all_notifications_read(self, client_a, user_a):
        """POST /api/notifications/read-all/ marca todas como leídas."""
        Notification.objects.create(user=user_a.profile, title='1', message='X', type='info')
        Notification.objects.create(user=user_a.profile, title='2', message='Y', type='success')

        resp = client_a.post('/api/notifications/read-all/')
        assert resp.status_code == 200
        assert Notification.objects.filter(user=user_a.profile, is_read=False).count() == 0


# ──────────────────────────────────────────────────────────────
# 10. SOLICITUDES DE DINERO P2P
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestMoneyRequests:
    """Solicitudes de dinero entre usuarios."""

    def test_create_money_request(self, client_a, user_a, user_b):
        """POST /api/money-requests/create/ crea una solicitud de A a B."""
        resp = client_a.post('/api/money-requests/create/', {
            'target_email': 'bob@duckbank.cl',
            'amount': 50000,
            'description': 'Pago de cena',
        }, format='json')
        assert resp.status_code == 201
        assert resp.data['status'] == 'pending'
        assert resp.data['amount'] == 50000

        # Notification sent to target
        assert Notification.objects.filter(user=user_b.profile, title__icontains='solicit').exists()

    def test_accept_money_request(self, client_a, client_b, user_a, user_b, account_a, account_b):
        """POST /api/money-requests/{id}/accept/ transfiere dinero de B a A."""
        # A requests money from B
        req = MoneyRequest.objects.create(
            requester=user_a.profile,
            target=user_b.profile,
            amount=50000,
            description='Pago compartido',
            status='pending',
        )

        initial_a = account_a.balance
        initial_b = account_b.balance

        resp = client_b.post(f'/api/money-requests/{req.id}/accept/')
        assert resp.status_code == 200
        assert resp.data['status'] == 'accepted'

        # Verify transfer happened
        account_a.refresh_from_db()
        account_b.refresh_from_db()
        assert account_a.balance == initial_a + 50000
        assert account_b.balance == initial_b - 50000

        # Notification sent to requester
        assert Notification.objects.filter(
            user=user_a.profile,
            title__icontains='acept'
        ).exists()

    def test_reject_money_request(self, client_a, client_b, user_a, user_b):
        """POST /api/money-requests/{id}/reject/ rechaza la solicitud sin mover dinero."""
        req = MoneyRequest.objects.create(
            requester=user_a.profile,
            target=user_b.profile,
            amount=30000,
            description='Otra solicitud',
            status='pending',
        )

        resp = client_b.post(f'/api/money-requests/{req.id}/reject/')
        assert resp.status_code == 200
        assert resp.data['status'] == 'rejected'

        # Notification sent to requester about rejection
        assert Notification.objects.filter(
            user=user_a.profile,
            title__icontains='rechaz'
        ).exists()

    def test_cannot_request_money_to_self(self, client_a, user_a):
        """No se puede solicitar dinero a uno mismo."""
        resp = client_a.post('/api/money-requests/create/', {
            'target_email': 'ana@duckbank.cl',
            'amount': 10000,
            'description': 'A mí mismo',
        }, format='json')
        assert resp.status_code == 400

    def test_list_money_requests(self, client_a, client_b, user_a, user_b):
        """GET /api/money-requests/ muestra solicitudes de y para el usuario."""
        MoneyRequest.objects.create(
            requester=user_a.profile,
            target=user_b.profile,
            amount=25000,
            description='Prueba listado',
            status='pending',
        )

        # Both users can see the request
        resp_a = client_a.get('/api/money-requests/')
        resp_b = client_b.get('/api/money-requests/')
        assert len(resp_a.data) >= 1
        assert len(resp_b.data) >= 1


# ──────────────────────────────────────────────────────────────
# 11. CONTACTOS
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestContacts:
    """Agenda de contactos."""

    def test_create_contact(self, client_a, user_a):
        """POST /api/contacts/ crea un contacto."""
        resp = client_a.post('/api/contacts/', {
            'name': 'María González',
            'bank': 'Banco Test',
            'rut': '33333333-3',
            'account_number': '123456789012',
        }, format='json')
        assert resp.status_code == 201
        assert resp.data['name'] == 'María González'

    def test_list_contacts(self, client_a, user_a):
        """GET /api/contacts/ lista los contactos del usuario."""
        Contact.objects.create(
            user=user_a.profile,
            name='Carlos López',
            bank='Banco X',
            account_number='987654321098',
        )
        resp = client_a.get('/api/contacts/')
        assert resp.status_code == 200
        assert len(resp.data['results']) >= 1

    def test_delete_contact(self, client_a, user_a):
        """DELETE /api/contacts/{id}/ elimina un contacto."""
        contact = Contact.objects.create(
            user=user_a.profile,
            name='Temporal',
            bank='Banco Y',
            account_number='111111111111',
        )
        resp = client_a.delete(f'/api/contacts/{contact.id}/')
        assert resp.status_code == 204
        assert not Contact.objects.filter(id=contact.id).exists()


# ──────────────────────────────────────────────────────────────
# 12. LOGOUT Y SEGURIDAD
# ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestAuthSecurity:
    """Seguridad: logout y acceso no autorizado."""

    def test_logout_blacklists_token(self, user_a):
        """POST /api/auth/logout/ invalida el refresh token."""
        refresh = RefreshToken.for_user(user_a)

        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        resp = client.post('/api/auth/logout/', {
            'refresh': str(refresh),
        }, format='json')
        assert resp.status_code == 200

    def test_unauthenticated_access_denied(self, db):
        """Sin token JWT, los endpoints protegidos retornan 401."""
        from rest_framework.test import APIClient
        client = APIClient()

        resp = client.get('/api/profile/')
        assert resp.status_code == 401

        resp = client.get('/api/accounts/')
        assert resp.status_code == 401

        resp = client.get('/api/transactions/')
        assert resp.status_code == 401