from urllib.request import AbstractBasicAuthHandler
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class AppUserManager(BaseUserManager):
    def create_user(self, email, password = None):
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password = None):
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='')
    USERNAME_FIELD = 'email' 
    #Django's authentication system requires a unique username to identify a user. 
    # However, in this case, the email field is used as the unique identifier for the user instead of the 
    # username field. This is specified by setting USERNAME_FIELD = 'email' in the AppUser model.
    REQUIRED_FIELDS = ['username','role']
    objects = AppUserManager()
    def __str__(self):
	    return self.username
