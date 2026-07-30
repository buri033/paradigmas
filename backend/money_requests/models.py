import uuid
from django.db import models
from users.models import Profile


class MoneyRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptada'),
        ('rejected', 'Rechazada'),
        ('expired', 'Expirada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requests_made')
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requests_received')
    amount = models.BigIntegerField()
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.requester} → {self.target}: ${self.amount:,} CLP ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Solicitud de Dinero'
        verbose_name_plural = 'Solicitudes de Dinero'
        ordering = ['-created_at']