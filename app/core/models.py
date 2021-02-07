from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime
from core.additionals.emailnotify import EmailNotification
from menu.models import Menu,Dish


# funkcje pomocnicze
def get_current_time():
    return datetime.datetime.now()
def get_yesterday_date():
    yesterday = get_current_time()-datetime.timedelta(days=1)
    return yesterday.date()
def get_created_yesterdays(model):
    return model.objects.filter(created__date=get_yesterday_date())
def get_updated_yesterdays(model):
    return model.objects.filter(updated__date=get_yesterday_date())

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

