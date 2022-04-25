import hashlib
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError("Users should have a username")
        if password is None:
            raise TypeError("Users should have a password")

        user = self.model(email=email,
                          password=hashlib.md5(password).hexdigest())
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True)
    phone = PhoneNumberField(max_length=68, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=25)
    qr_img = models.ImageField(upload_to='static/media', blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
