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


class Student(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    class_detail = models.ForeignKey('ClassDetail', on_delete=models.CASCADE)
    point_scored = models.IntegerField(default=0)

class ClassDetail(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    grad_year = models.ForeignKey('GraduationYear', on_delete=models.CASCADE)

class Certificate(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    certificate_approval_status = models.ForeignKey('Status', on_delete=models.CASCADE)
    activity_point_details = models.ForeignKey('ActivityPoint', on_delete=models.CASCADE)

class ActivityPoint(models.Model):
    type = models.CharField(max_length=255)
    point_alloted = models.IntegerField()

class PendingRequest(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    student_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='pending_requests')
    faculty = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    grad_year = models.ForeignKey('GraduationYear', on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)

class Branch(models.Model):
    BRANCH_CHOICES = [
        ('csa', 'CSA'),
        ('csb', 'CSB'),
        ('csc', 'CSC'),
        ('csbs', 'CSBS'),
        ('eca', 'ECA'),
        ('ecb', 'ECB'),
        ('eee', 'EEE'),
        ('ebe', 'EBE'),
        ('mech', 'MECH'),
    ]
    branch = models.CharField(max_length=255, choices=BRANCH_CHOICES)

class GraduationYear(models.Model):
    grad_year_choice = [
        ('2024','2024'),
        ('2025','2025'),
        ('2026','2026'),
        ('2027','2027'),
        ('2028','2028'),
        ('2029','2029'),
        ('2030','2030'),
    ]
    grad_year = models.CharField(max_length=255, choices=grad_year_choice)

class Status(models.Model):
    STATUS_CHOICES = [
        ('approved','Approved'),
        ('pending','Pending'),
        ('rejected','Rejected'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
