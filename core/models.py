from django.contrib.auth.models import User
from django.db import models

class Safaricom(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Account of {self.user.username} with balance {self.balance}"

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.receiver:
            return f"Transaction from {self.sender.username} to {self.receiver.username} of Ksh {self.amount}"
        else:
            return f"Transaction from {self.sender.username} to Self (Withdrawal) of Ksh {self.amount}"


class Fuliza(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Fuliza overdraft limit
    used = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)   # Amount of Fuliza already used

    def available_fuliza(self):
        """Calculate the available Fuliza overdraft."""
        return self.limit - self.used

    def __str__(self):
        return f"Fuliza for {self.account.user.username} - Used: {self.used}, Limit: {self.limit}"
    
class MShwari(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    locked_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"MShwari account for {self.account.user.username}"

    def get_locked_balance(self):
        return self.locked_balance

    def get_available_balance(self):
        return self.available_balance