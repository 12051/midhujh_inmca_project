from django.contrib import admin
from .models import CustomUser,CrimeReport,AnonyReport

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CrimeReport)
admin.site.register(AnonyReport)