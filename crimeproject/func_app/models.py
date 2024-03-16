from django.db import models
# from django.contrib. .db import models

# Create your models here.

class Advocate(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    office_place = models.CharField(max_length=100,blank=True,null=True)
    level = models.CharField(max_length=100,blank=True,null=True)
    phone_number = models.CharField(max_length=10,blank=True,null=True)  # Assuming Indian phone numbers
    email = models.EmailField(blank=True,null=True)
    specialization = models.CharField(max_length=100,blank=True,null=True)
    years_of_experience = models.PositiveIntegerField(blank=True,null=True)
    photo = models.ImageField(upload_to='advocate_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class PropertyDacoitReport(models.Model):
    reporter_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    date_time_incidence = models.DateTimeField()
    num_perpetrators = models.IntegerField()
    presence_weapon = models.CharField(max_length=100, blank=True, null=True)
    description_incidence = models.TextField()
    stolen_item = models.CharField(max_length=255, blank=True, null=True)
    injury = models.CharField(max_length=100, blank=True, null=True)
    witnesses = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.reporter_name
