from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class AdminUserManager(BaseUserManager):
    """The UserManager for our Admin class."""

    def create_user(self, email, password):
        """Create a user and return it."""
        user = get_user_model().objects.create(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Create a superuser and return it.

        Since all admins are superusers, a superuser is just a normal user
        """
        return self.create_user(email, password)


class Admin(AbstractBaseUser):
    """Our custom user model for the administrators."""

    email = models.EmailField(primary_key=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = AdminUserManager()

    class Meta:
        verbose_name = _("Admin")
        verbose_name_plural = _("Admins")

    def has_perm(self, perm, obj=None):
        """Django requires this function."""
        return True

    def has_module_perms(self, app_label):
        """Django requires this function."""
        return True
