from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models


class AdminUserManager(BaseUserManager):
    def create_user(self, email, password):
        user = get_user_model().objects.create(email=email)
        user.set_password(password)
        return user.save()

    def create_superuser(self, email, password):
        return self.create_user(email, password)


class Admin(AbstractBaseUser):
    email = models.EmailField(primary_key=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = AdminUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
