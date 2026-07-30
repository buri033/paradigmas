import uuid
from django.db import models
from users.models import Profile


class SavingsBox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='savings_boxes')
    name = models.CharField(max_length=100)
    balance = models.BigIntegerField(default=0)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=11.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.balance:,} COP"

    class Meta:
        verbose_name = 'Cajita'
        verbose_name_plural = 'Cajitas'
        ordering = ['-created_at']


class SavingsBoxInterestLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    box = models.ForeignKey(SavingsBox, on_delete=models.CASCADE, related_name='interest_logs')
    period_start = models.DateField()
    period_end = models.DateField()
    interest_earned = models.BigIntegerField()
    balance_before = models.BigIntegerField()
    balance_after = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interest {self.box.name}: +${self.interest_earned:,}"

    class Meta:
        verbose_name = 'Registro de Interés'
        verbose_name_plural = 'Registros de Interés'
        ordering = ['-period_end']