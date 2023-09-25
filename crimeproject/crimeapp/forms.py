from django import forms
from .models import CrimeReport, AnonyReport, DocReport

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

class DocReportForm(forms.ModelForm):
    class Meta:
        model = DocReport
        fields = '__all__'
        evidence = forms.FileField(
        label='Upload Evidence (Photograph, Video, or Audio)',
        required=False  # Set this to True if evidence is mandatory
    )