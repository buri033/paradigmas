from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [('user', 'Usuario'), ('admin', 'Administrador')]
    TIER_CHOICES = [('basic', 'Basic'), ('prime', 'Prime'), ('gold', 'Gold')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    account_tier = models.CharField(max_length=10, choices=TIER_CHOICES, default='prime')
    hide_balance = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'