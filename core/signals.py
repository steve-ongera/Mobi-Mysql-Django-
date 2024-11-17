# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        # Automatically create an Account with an initial balance of 0
        Account.objects.create(user=instance, balance=0)

@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    try:
        # Save the associated Account if the User instance is saved
        instance.account.save()
    except Account.DoesNotExist:
        pass
