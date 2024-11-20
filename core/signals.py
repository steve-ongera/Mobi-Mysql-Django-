# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
from decimal import Decimal

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



@receiver(post_save, sender=MShwari)
def update_mpesa_balance(sender, instance, created, **kwargs):
    if not created:  # Trigger only when the account is updated (not created)
        # Amount to deduct from Mpesa account is the deposited amount
        deposit_amount = instance.available_balance  # The amount added to MShwari account

        try:
            # Get the Mpesa account associated with the user
            mpesa_account = Account.objects.get(user=instance.account.user)
            
            # Check if the Mpesa balance is sufficient to deduct the deposit
            if mpesa_account.balance >= deposit_amount:
                # Deduct the amount from Mpesa account balance
                mpesa_account.balance -= deposit_amount
                mpesa_account.save()  # Save the updated balance

        except Account.DoesNotExist:
            # If no Mpesa account exists for the user, log or handle the error
            print(f"Error: No Mpesa account found for {instance.account.user.username}")


# @receiver(post_save, sender=MShwari)
# def update_mpesa_balance_on_withdrawal(sender, instance, **kwargs):
#     # Check if the available balance was updated (indicating a withdrawal occurred)
#     if 'available_balance' in kwargs.get('update_fields', []):
#         # Check if the balance has decreased (withdrawal)
#         if instance.available_balance < instance.__original_available_balance:
#             withdrawn_amount = instance.__original_available_balance - instance.available_balance
#             # Get the corresponding Mpesa account linked to the MShwari account
#             try:
#                 mpesa_account = Account.objects.get(user=instance.account.user)
#                 mpesa_account.balance += withdrawn_amount
#                 mpesa_account.save()
#             except Account.DoesNotExist:
#                 pass  # Handle missing Mpesa account if necessary