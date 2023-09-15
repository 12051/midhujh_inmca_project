from django import forms
from .models import CrimeReport, AnonyReport

class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = CrimeReport
        fields = '__all__'
        exclude = ['status']
    
class AnonyReportForm(forms.ModelForm):
    class Meta:
        model = AnonyReport
        fields = '__all__'
        exclude = ['status']
    # Add custom validation methods as needed
