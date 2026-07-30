import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from savings.models import SavingsBox, SavingsBoxInterestLog


class Command(BaseCommand):
    help = 'Calculate daily compound interest for all active savings boxes'

    def handle(self, *args, **options):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        boxes = SavingsBox.objects.filter(is_active=True)
        count = 0

        for box in boxes:
            rate = float(box.interest_rate) / 100
            daily_factor = Decimal(str(1 + rate / 365))
            balance_before = box.balance
            interest = int(balance_before * (daily_factor - 1))

            if interest > 0:
                balance_after = balance_before + interest
                box.balance = balance_after
                box.save()

                SavingsBoxInterestLog.objects.create(
                    box=box,
                    period_start=yesterday,
                    period_end=today,
                    interest_earned=interest,
                    balance_before=balance_before,
                    balance_after=balance_after,
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Interest calculated for {count} boxes'))