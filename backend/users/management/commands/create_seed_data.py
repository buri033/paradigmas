from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile
from accounts.models import Account
from loans.models import Card, Loan
from notifications.models import Notification


class Command(BaseCommand):
    help = 'Create seed data for development'

    def handle(self, *args, **options):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin@duckbank.cl',
            defaults={
                'email': 'admin@duckbank.cl',
                'first_name': 'Admin',
                'last_name': 'DuckBank',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_user.profile.role = 'admin'
            admin_user.profile.account_tier = 'gold'
            admin_user.profile.save()
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Create demo user
        demo_user, created = User.objects.get_or_create(
            username='juan@duckbank.cl',
            defaults={
                'email': 'juan@duckbank.cl',
                'first_name': 'Juan',
                'last_name': 'Doe',
            }
        )
        if created:
            demo_user.set_password('juan123')
            demo_user.save()
            demo_user.profile.rut = '12345678-9'
            demo_user.profile.phone = '+56987654321'
            demo_user.profile.save()

            # Update default account balance
            account = demo_user.profile.accounts.first()
            if account:
                account.balance = 4850900
                account.save()

            # Create card
            Card.objects.create(
                user=demo_user.profile,
                card_name='Duck Visa Signature',
                card_type='credit',
                last_four='8821',
                cvv='842',
                credit_limit=2500000,
                used_amount=340000,
                expiry_date='12/28',
                card_network='Visa',
                color='#6366f1',
            )

            # Create loan
            Loan.objects.create(
                user=demo_user.profile,
                loan_name='Crédito de Consumo',
                total_amount=5000000,
                remaining=3220000,
                monthly_fee=185000,
                interest_rate=1.15,
                total_quotas=24,
                paid_quotas=12,
                next_due_date=date.today() + timedelta(days=15),
                status='active',
            )

            # Create notifications
            Notification.objects.create(
                user=demo_user.profile,
                title='¡Bienvenido a DuckBank!',
                message='Tu cuenta ha sido creada exitosamente. Comienza a explorar todas las funcionalidades.',
                type='success',
            )
            Notification.objects.create(
                user=demo_user.profile,
                title='Pago recibido',
                message='Has recibido $250,000 COP de María González.',
                type='success',
            )

            self.stdout.write(self.style.SUCCESS('Demo user created with cards, loans, and notifications'))
        else:
            self.stdout.write(self.style.WARNING('Demo user already exists'))

        self.stdout.write(self.style.SUCCESS('Seed data complete!'))