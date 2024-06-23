from random import randint

from django.db import models

from card.models import Card


class Transaction(models.Model):
    sender = models.ForeignKey(Card, on_delete=models.PROTECT, related_name='sender')
    receiver = models.ForeignKey(Card, on_delete=models.PROTECT, related_name='receiver')
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    transaction_number = models.CharField(max_length=12, unique=True, null=True)

    def __str__(self):
        return f'{self.transaction_number}-{self.amount}-{self.date}'

    def save(self, *args, **kwargs):
        if not self.transaction_number:
            self.transaction_number = randint(100000000000, 999999999999)
            super().save()
        super().save()