from django.contrib import admin
from .models import CustomUser,CrimeReport,AnonyReport,SpecLoc,Aadhaar

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CrimeReport)
admin.site.register(AnonyReport)
admin.site.register(SpecLoc)
admin.site.register(Aadhaar)