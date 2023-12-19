from django.db import models #noqa
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
# Create your models here.

class UserManager(BaseUserManager):
    """user manager"""
    def create_user(self,email,password=None,**extraFields):

        user = self.model(email=self.normalize_email(email),**extraFields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None,**extraFields):
        """create super user"""
        user = self.create_user(email=email,password=password,**extraFields)
        user.is_superuser=True
        user.is_staff = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser,PermissionsMixin):
    """user on our app (ovveriding default django user)"""
    email = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()
    USERNAME_FIELD ="email"


