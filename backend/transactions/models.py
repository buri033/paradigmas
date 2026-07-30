import uuid
from django.db import models
from users.models import Profile
from accounts.models import Account


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Ingreso'),
        ('expense', 'Gasto'),
        ('transfer', 'Transferencia'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.BigIntegerField()
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50, null=True, blank=True)
    icon = models.CharField(max_length=10, default='💰')
    reference = models.CharField(max_length=50, null=True, blank=True)
    destination_name = models.CharField(max_length=100, null=True, blank=True)
    destination_account = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - ${self.amount:,} COP - {self.description}"

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-created_at']


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    bank = models.CharField(max_length=50)
    rut = models.CharField(max_length=12, null=True, blank=True)
    account_number = models.CharField(max_length=20)
    avatar_color = models.CharField(max_length=7, default='#6366f1')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.bank}"

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['created_at']