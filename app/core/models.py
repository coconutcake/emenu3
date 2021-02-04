from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from core import signals 

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """ Tworzy uzytkownika """
        if not email:
            raise ValueError('Uzytkownik musi mieć email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password):
        """ Tworzy superusera """
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def create_staff(self,email,password):
        user = self.create_user(email,password)
        user.is_staff = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'




# Auto tworzenie tokena usera

# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)