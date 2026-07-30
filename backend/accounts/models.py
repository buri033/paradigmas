import uuid
import random
from django.db import models
from users.models import Profile


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('vista', 'Cuenta Vista'),
        ('ahorro', 'Cuenta de Ahorro'),
        ('corriente', 'Cuenta Corriente'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='accounts')
    account_type = models.CharField(max_length=15, choices=ACCOUNT_TYPE_CHOICES, default='vista')
    account_number = models.CharField(max_length=20, unique=True)
    alias = models.CharField(max_length=50, null=True, blank=True)
    balance = models.BigIntegerField(default=0)
    currency = models.CharField(max_length=3, default='CLP')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.alias or self.account_type} - {self.account_number}"

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        super().save(*args, **kwargs)