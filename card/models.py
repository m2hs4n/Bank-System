import datetime
from random import randint

from django.db import models

# from account.models import Profile


class Card(models.Model):
    profile_rel = models.OneToOneField("account.Profile", on_delete=models.PROTECT)

    card_number = models.CharField(max_length=16, unique=True)
    cvv2 = models.CharField(max_length=4)
    expiration_date = models.DateField()
    stock = models.PositiveBigIntegerField(default=0)

    def create(self):
        self.card_number = str(randint(1000_0000_0000_0000, 9999_9999_9999_9999))
        self.cvv2 = randint(1000, 9999)
        self.expiration_date = datetime.date.today() + datetime.timedelta(days=800)
        super().save()
