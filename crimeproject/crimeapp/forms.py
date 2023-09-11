from django import forms
from .models import CrimeReport

class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = CrimeReport
        fields = '__all__'
    
    # Add custom validation methods as needed
