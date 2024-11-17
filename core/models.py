from django.contrib.auth.models import User
from django.db import models

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
