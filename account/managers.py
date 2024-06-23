from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password):
        if not phone_number:
            raise ValueError("User must have phone number")

        if not password:
            raise ValueError("Should have password")

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.status = "SU"
        user.is_staff = True
        user.save()

    def create_admin(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.status = "AD"
        user.save()