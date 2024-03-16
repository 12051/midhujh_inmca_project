from datetime import timezone
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
    num = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=128)
    is_normal = models.BooleanField(default=False)
    is_law = models.BooleanField(default=False)
    is_prison = models.BooleanField(default=False)
    is_control = models.BooleanField(default=False)
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
    
from django.db.models.signals import pre_save
from django.dispatch import receiver
    
class CrimeReport(models.Model):
    #fir_number = models.CharField(max_length=10, null=True, unique=True)
    reporter_name = models.CharField(max_length=100,null=True,blank=True)
    reporter_location = models.CharField(max_length=100)
    spec_location = models.ForeignKey(SpecLoc, on_delete=models.SET_NULL, null=True, blank=True)
    off_type = models.CharField(max_length=100,null=True,blank=True)
    datetime = models.DateTimeField(null=True,blank=True)
    aadhaarno=models.CharField(max_length=12, default='')
    description = models.TextField(null=True,blank=True)
    victimDescription = models.TextField(null=True,blank=True)
    witnessInformation = models.TextField(null=True,blank=True)
    offenderDescription = models.TextField(null=True,blank=True)
    delay = models.TextField(null=True,blank=True)
    report_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    list_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    location_status = models.CharField(max_length=100, null=True, blank=True)
    STATUS_CHOICES = (
        ('Crime Reported', 'Crime Reported'),
        ('Preliminary Investigation completed', 'Preliminary Investigation completed'),
        ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'),
        ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'),        
        ('Arrest and Detention', 'Arrest and Detention'),
        ('Case Closure in progress', 'Case Closure in progress'),
        ('Case Closed', 'Case Closed'),
    )
    
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Crime Reported',null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if self.spec_location:
            self.location_status = self.spec_location.enforcement_loc  
        super().save(*args, **kwargs)

    def save_id(self):
        # Create an EvidenceCrimeReport instance and associate it with the current CrimeReport
        evidence_report = EvidenceCrimeReport(crime_idnum=self)
        evidence_report.save()
        
    def fir(self):
        self.status='Preliminary Investigation completed'
    def witness(self):
        self.status='Inquiry and Investigation in progress'
    def forensic(self):
        self.status='Inquiry and Investigation completed' 
    def arrest(self):
        self.status='Arrest and Detention'
    def charge(self):
        self.status='Case Closure in progress'
    def case(self):
        self.status='Case Closure in progress'
    def final(self):
        self.status='Case Closed'
    def __str__(self):
        return self.reporter_name
    
    
class DocReport(models.Model):
    #fir_number = models.CharField(max_length=10, null=True, unique=True)
    i_name = models.CharField(max_length=100)
    ano=models.CharField(max_length=12, default='')
    reporter_location = models.CharField(max_length=100,null=True,blank=True)
    descri = models.TextField(null=True,blank=True)
    victimDescri = models.TextField(null=True,blank=True)
    witnessInfo = models.TextField(null=True,blank=True)
    delay_report = models.TextField(null=True,blank=True)
    evidence_image = models.FileField(upload_to='evidence_images/',null=True,blank=True)
    list_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    report_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    THREAT_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    threat = models.CharField(
        blank=True,
        max_length=3,
        choices=THREAT_CHOICES,
        default='No',  # You can set the default value to 'No' if desired
        verbose_name='Any kind of Threat or Violence faced'
    )
    STATUS_CHOICES = (
        ('Crime Reported', 'Crime Reported'),
        ('Preliminary Investigation completed', 'Preliminary Investigation completed'),
        ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'),
        ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'),        
        ('Arrest and Detention', 'Arrest and Detention'),
        ('Case Closure in progress', 'Case Closure in progress'),
        ('Case Closed', 'Case Closed'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Crime Reported',null=True,blank=True)
    
    def save_id(self):
        # Create an EvidenceCrimeReport instance and associate it with the current CrimeReport
        evidence_report = EvidenceDocReport(crime_idnum=self)
        evidence_report.save()
        
    def fir(self):
        self.status='Preliminary Investigation completed'
    def witness(self):
        self.status='Inquiry and Investigation in progress'
    def forensic(self):
        self.status='Inquiry and Investigation completed' 
    def arrest(self):
        self.status='Arrest and Detention'
    def charge(self):
        self.status='Case Closure in progress'
    def case(self):
        self.status='Case Closure in progress'
    def final(self):
        self.status='Case Closed'
    
    def __str__(self):
        return self.i_name
    
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
    
class PublicReport(models.Model):
    #fir_number = models.CharField(max_length=10, null=True, unique=True)
    info_name = models.CharField(max_length=100)
    mail = models.EmailField(null=True,blank=True)
    reporter_location = models.CharField(max_length=100)
    spec_location = models.ForeignKey(SpecLoc, on_delete=models.SET_NULL, null=True, blank=True)
    offen_type = models.CharField(max_length=100,null=True,blank=True)
    datetime = models.DateTimeField(null=True,blank=True)
    aadhno=models.CharField(max_length=12, default='')
    description = models.TextField()
    victimDescription = models.TextField(null=True,blank=True)
    witnessInformation = models.TextField(null=True,blank=True)
    offenderDescription = models.TextField(null=True,blank=True)
    delay = models.TextField(null=True,blank=True)
    list_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    report_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    location_status = models.CharField(max_length=100, null=True, blank=True)
    STATUS_CHOICES = (
        ('Crime Reported', 'Crime Reported'),
        ('Preliminary Investigation completed', 'Preliminary Investigation completed'),
        ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'),
        ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'),        
        ('Arrest and Detention', 'Arrest and Detention'),
        ('Case Closure in progress', 'Case Closure in progress'),
        ('Case Closed', 'Case Closed'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Crime Reported')
    
    def save(self, *args, **kwargs):
        if self.spec_location:
            self.location_status = self.spec_location.enforcement_loc  
        super().save(*args, **kwargs)
    
    def save_id(self):
        # Create an EvidenceCrimeReport instance and associate it with the current CrimeReport
        evidence_report = EvidencePublicReport(crime_idnum=self)
        evidence_report.save()
        
    def fir(self):
        self.status='Preliminary Investigation completed'
    def witness(self):
        self.status='Inquiry and Investigation in progress'
    def forensic(self):
        self.status='Inquiry and Investigation completed' 
    def arrest(self):
        self.status='Arrest and Detention'
    def charge(self):
        self.status='Case Closure in progress'
    def case(self):
        self.status='Case Closure in progress'
    def final(self):
        self.status='Case Closed'
        
    def __str__(self):
        return self.info_name
    
class FIRFile(models.Model):
    crime_report = models.ForeignKey('CrimeReport', on_delete=models.CASCADE)
    file = models.FileField(upload_to='fir_files/')

    def __str__(self):
        return f"FIR File for Crime Report ID {self.crime_report.id}"

from django.db import models
from django.utils import timezone

class EvidenceCrimeReport(models.Model):
    crime_idnum = models.ForeignKey('CrimeReport', on_delete=models.CASCADE, null=True, blank=True)
    document_fir = models.FileField(upload_to='evidence_fir/', null=True, blank=True)
    document_witness = models.FileField(upload_to='evidence_witness/', null=True, blank=True)
    document_forensic = models.FileField(upload_to='evidence_forensic/', null=True, blank=True)
    document_arrest = models.FileField(upload_to='evidence_arrest/', null=True, blank=True)
    document_charge = models.FileField(upload_to='evidence_charge/', null=True, blank=True)
    document_case = models.FileField(upload_to='evidence_case/', null=True, blank=True)
    document_final = models.FileField(upload_to='evidence_final/', null=True, blank=True)
    
    date_fir = models.DateTimeField(null=True, blank=True)
    date_witness = models.DateTimeField(null=True, blank=True)
    date_forensic = models.DateTimeField(null=True, blank=True)
    date_arrest = models.DateTimeField(null=True, blank=True)
    date_charge = models.DateTimeField(null=True, blank=True)
    date_case = models.DateTimeField(null=True, blank=True)
    date_final = models.DateTimeField(null=True, blank=True)
    
class EvidenceDocReport(models.Model):
    crime_idnum = models.ForeignKey('DocReport', on_delete=models.CASCADE, null=True, blank=True)
    document_fir = models.FileField(upload_to='evidence_fir/', null=True, blank=True)
    document_witness = models.FileField(upload_to='evidence_witness/', null=True, blank=True)
    document_forensic = models.FileField(upload_to='evidence_forensic/', null=True, blank=True)
    document_arrest = models.FileField(upload_to='evidence_arrest/', null=True, blank=True)
    document_charge = models.FileField(upload_to='evidence_charge/', null=True, blank=True)
    document_case = models.FileField(upload_to='evidence_case/', null=True, blank=True)
    document_final = models.FileField(upload_to='evidence_final/', null=True, blank=True)
    
    date_fir = models.DateTimeField(null=True, blank=True)
    date_witness = models.DateTimeField(null=True, blank=True)
    date_forensic = models.DateTimeField(null=True, blank=True)
    date_arrest = models.DateTimeField(null=True, blank=True)
    date_charge = models.DateTimeField(null=True, blank=True)
    date_case = models.DateTimeField(null=True, blank=True)
    date_final = models.DateTimeField(null=True, blank=True)
    
class EvidencePublicReport(models.Model):
    crime_idnum = models.ForeignKey('PublicReport', on_delete=models.CASCADE, null=True, blank=True)
    document_fir = models.FileField(upload_to='evidence_fir/', null=True, blank=True)
    document_witness = models.FileField(upload_to='evidence_witness/', null=True, blank=True)
    document_forensic = models.FileField(upload_to='evidence_forensic/', null=True, blank=True)
    document_arrest = models.FileField(upload_to='evidence_arrest/', null=True, blank=True)
    document_charge = models.FileField(upload_to='evidence_charge/', null=True, blank=True)
    document_case = models.FileField(upload_to='evidence_case/', null=True, blank=True)
    document_final = models.FileField(upload_to='evidence_final/', null=True, blank=True)
    
    date_fir = models.DateTimeField(null=True, blank=True)
    date_witness = models.DateTimeField(null=True, blank=True)
    date_forensic = models.DateTimeField(null=True, blank=True)
    date_arrest = models.DateTimeField(null=True, blank=True)
    date_charge = models.DateTimeField(null=True, blank=True)
    date_case = models.DateTimeField(null=True, blank=True)
    date_final = models.DateTimeField(null=True, blank=True)
    

        
class InmatePlaces(models.Model):
    place_id = models.AutoField(primary_key=True)
    place_name = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.place_name

class Inmate(models.Model):
    inmate_name = models.TextField(max_length=100,null=True,blank=True)
    inmate_id = models.CharField(max_length=10,null=True,blank=True)
    inmate_loc = models.ForeignKey(InmatePlaces,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.inmate_name
    
class PrisonReport(models.Model):
    inmates = models.ManyToManyField(Inmate, blank=True)
    loc_prison = models.CharField(max_length=100, choices=[("kanjirappally", "Kanjirappally"), ("changanassery", "Changanassery")])
    nat_crime = models.CharField(max_length=100, choices=[("misconduct", "Inmate Misconduct"), ("breach", "Security Breaches"), ("harm", "Harm")])
    datetime = models.DateTimeField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    evidence_image = models.FileField(upload_to='evidence_images/',null=True,blank=True)
    def __str__(self):
        return self.datetime
    
class Jailor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Appointment(models.Model):
    ap_name = models.CharField(max_length=20,null=True,blank=True)
    time_slot = models.CharField(max_length=20,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    # Add more fields as needed

    def __str__(self):
        return f'Appointment for {self.ap_name} on {self.date} at {self.time_slot}'
    
class ContactMessage(models.Model):
    your_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.your_name
    
class Location(models.Model):
    station_name = models.CharField(max_length=15,null=True)
    latitude = models.CharField(max_length=15,null=True)
    longitude = models.CharField(max_length=15,null=True)

    def __str__(self):
        return self.your_name   
    
