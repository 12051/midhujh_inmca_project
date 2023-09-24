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
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=128)
    is_normal = models.BooleanField(default=False)
    is_law = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    REQUIRED_FIELDS = []
    def __str__(self): 
        return self.name
    
class SpecLoc(models.Model):
    reporter_loc = models.CharField(max_length=100)
    enforcement_loc = models.CharField(max_length=100)
    def __str__(self):
        return self.reporter_loc
    
class CrimeReport(models.Model):
    #fir_number = models.CharField(max_length=10, null=True, unique=True)
    reporter_name = models.CharField(max_length=100)
    reporter_location = models.CharField(max_length=100)
    spec_location = models.ForeignKey(SpecLoc, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    aadhaarno=models.CharField(max_length=12, default='')
    location = models.CharField(max_length=200)
    description = models.TextField()
    offender_name = models.CharField(max_length=100, blank=True, null=True)
    offender_vehiclenumber = models.CharField(max_length=20, blank=True, null=True)
    witness_name = models.CharField(max_length=100, blank=True, null=True)
    list_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    STATUS_CHOICES = (
        ('Reported', 'Reported'),
        ('FIR Verified', 'FIR Verified'),
        ('Investigation in progress', 'Investigation in progress'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Reported')
    def __str__(self):
        return self.reporter_name
    
class AnonyReport(models.Model):
    reporter_location = models.CharField(max_length=100)
    spec_location = models.ForeignKey(SpecLoc, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    offender_name = models.CharField(max_length=100, blank=True, null=True)
    offender_vehiclenumber = models.CharField(max_length=20, blank=True, null=True)
    witness_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.reporter_location

class Aadhaar(models.Model):
    aadhaar_number = models.CharField(max_length=12, unique=True)
    def __str__(self):
        return self.aadhaar_number
