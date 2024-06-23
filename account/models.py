from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    USER_TYPE = [
        ('SU', 'Superuser user'),
        ('AD', 'Admin user'),
        ('CU', 'Customer user')
    ]

    ACCOUNT_STATUS = [
        ('SU', 'Suspend'),
        ('AC', 'Active'),
        ('DE', 'Delete'),
        ('CL', 'Close'),
        ('BA', 'Banned')
    ]

    phone_number = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    status = models.CharField(max_length=3, choices=ACCOUNT_STATUS, default='AC')
    account_type = models.CharField(max_length=3, choices=USER_TYPE, default="CU")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number}-{self.status}-{self.account_type}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        if self.account_type == "SU" and self.is_staff:
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.account_type == "AD":
            return True
        else:
            return False

    @property
    def is_customer(self):
        if self.account_type == "CU":
            return True
        else:
            return False


class Profile(models.Model):
    STATUS = [
        ('SU', 'Suspend'),
        ('AC', 'Accepted'),
        ('BA', 'Banned'),
    ]

    GENDER = [
        ('0', 'Male'),
        ('1', 'Female'),
        ('2', 'Other'),
    ]

    user_rel = models.OneToOneField(User, on_delete=models.CASCADE)

    status = models.CharField(max_length=3, choices=STATUS, default='SU')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=10, unique=True)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=124)
    gender = models.CharField(max_length=1, choices=GENDER)
    face_image = models.ImageField(upload_to='account/face_image/')
    birth_date = models.DateField()
    address = models.TextField()

    updated_at = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'
