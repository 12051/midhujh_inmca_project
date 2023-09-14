from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser): 
    username = None 
    USERNAME_FIELD  = 'email' 
    # username=models.CharField(unique=True,max_length=20,default='')
    name = models.CharField(max_length=100, default='') 
    aadhaarno=models.CharField(max_length=12, default='') 
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=128) 
    is_witness = models.BooleanField(default=False) 
    is_victim = models.BooleanField(default=False) 
    REQUIRED_FIELDS = []
    def __str__(self): 
        return self.name
    
class CrimeReport(models.Model):
    #fir_number = models.CharField(max_length=10, null=True, unique=True)
    reporter_name = models.CharField(max_length=100)
    reporter_location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    offender_name = models.CharField(max_length=100, blank=True, null=True)
    offender_vehiclenumber = models.CharField(max_length=20, blank=True, null=True)
    witness_name = models.CharField(max_length=100, blank=True, null=True)
    list_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.reporter_name
    
class AnonyReport(models.Model):
    reporter_location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    offender_name = models.CharField(max_length=100, blank=True, null=True)
    offender_vehiclenumber = models.CharField(max_length=20, blank=True, null=True)
    witness_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.reporter_location