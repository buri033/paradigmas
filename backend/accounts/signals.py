from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from .models import Account


@receiver(post_save, sender=Profile)
def create_default_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(
            user=instance,
            account_type='vista',
            alias='Cuenta Vista',
            balance=4850900,
        )