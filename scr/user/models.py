from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.cache import cache
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, full_name, email, phone=None, password=None):
        if not username:
            raise ValueError('User must have a username')
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            username=username,
            full_name=full_name,
            email=self.normalize_email(email),
            phone=phone,  # Allow phone to be None
        )
        print(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, email, password):
        print(password)
        user = self.create_user(username, full_name, email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    tg_id = models.CharField(max_length=255, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']

    def __str__(self):
        return f"{self.full_name} - {self.username}"


def getKey(key):
    return cache.get(key)


def setKey(key, value, timeout):
    cache.set(key, value, timeout)
