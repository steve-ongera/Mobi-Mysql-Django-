# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account, Fuliza

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


@receiver(post_save, sender=Account)
def update_fuliza_limit(sender, instance, **kwargs):
    """
    Signal to update or create Fuliza based on the account balance.
    """
    account = instance  # The account instance being saved
    balance = account.balance

    # Determine the Fuliza limit based on balance
    if balance < 500:
        limit = 0
    elif 500 <= balance < 5000:
        limit = 300
    elif 5000 <= balance < 20000:
        limit = 800
    elif 20000 <= balance < 50000:
        limit = 1000
    elif 50000 <= balance <= 100000:
        limit = 1200
    else:
        limit = 0  # Default to 0 if balance exceeds the upper range

    # Update or create the associated Fuliza record
    fuliza, created = Fuliza.objects.update_or_create(
        account=account,
        defaults={
            'limit': limit,  # Update the limit
            'used': 0  # Reset the used amount when limit changes
        }
    )
