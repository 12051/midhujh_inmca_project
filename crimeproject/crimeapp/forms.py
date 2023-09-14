from django import forms
from .models import CrimeReport, AnonyReport

class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = CrimeReport
        fields = '__all__'
    
class AnonyReportForm(forms.ModelForm):
    class Meta:
        model = AnonyReport
        fields = '__all__'
    # Add custom validation methods as needed
