import uuid
from django.db import models
from users.models import Profile


class Loan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('paid', 'Pagado'),
        ('defaulted', 'En mora'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='loans')
    loan_name = models.CharField(max_length=100)
    total_amount = models.BigIntegerField()
    remaining = models.BigIntegerField()
    monthly_fee = models.BigIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=1.15)
    total_quotas = models.IntegerField()
    paid_quotas = models.IntegerField(default=0)
    next_due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.loan_name} - ${self.remaining:,} COP pendiente"

    class Meta:
        verbose_name = 'Crédito'
        verbose_name_plural = 'Créditos'
        ordering = ['-created_at']


class Card(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activa'),
        ('locked', 'Bloqueada'),
        ('cancelled', 'Cancelada'),
    ]
    TYPE_CHOICES = [
        ('credit', 'Crédito'),
        ('debit', 'Débito'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cards')
    card_name = models.CharField(max_length=50)
    card_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='credit')
    last_four = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)
    credit_limit = models.BigIntegerField()
    used_amount = models.BigIntegerField(default=0)
    expiry_date = models.CharField(max_length=5)
    card_network = models.CharField(max_length=20, default='Visa')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    color = models.CharField(max_length=7, default='#6366f1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.card_name} •• {self.last_four}"

    class Meta:
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'
        ordering = ['created_at']