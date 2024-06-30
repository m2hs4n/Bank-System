import uuid

from django.db import models

from account.models import Profile


class Token(models.Model):
    STATUS = [
        ('SU', 'Suspend'),
        ('RE', 'Received'),
    ]

    profile_rel = models.ForeignKey(Profile, on_delete=models.PROTECT)
    token = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=3, choices=STATUS, default='SU')
    stock = models.PositiveIntegerField(default=0)
    password = models.CharField(max_length=255, null=True, blank=True)
    date_received = models.DateField(null=True, blank=True)
    date_allow_receipt = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.token}-{self.stock}'

    def crate(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4())
            self.save()
        self.save()
