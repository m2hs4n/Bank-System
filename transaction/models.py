from django.db import models

from card.models import Card


class Transaction(models.Model):
    sender = models.ForeignKey(Card, on_delete=models.PROTECT, related_name='sender')
    receiver = models.ForeignKey(Card, on_delete=models.PROTECT, related_name='receiver')
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    transaction_number = models.PositiveBigIntegerField(unique=True)

    def __str__(self):
        return f'{self.transaction_number}-{self.amount}-{self.date}'