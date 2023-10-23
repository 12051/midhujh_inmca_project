from django import forms
from .models import CrimeReport, AnonyReport, DocReport, PublicReport, EvidenceCrimeReport, PrisonReport

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
        
class PublicForm(forms.ModelForm):
    class Meta:
        model = PublicReport
        fields = '__all__'
        exclude = ['status']
        
class PrisonReportForm(forms.ModelForm):
    class Meta:
        model = PrisonReport
        fields = '__all__'
        
class EvidenceCrimeForm(forms.ModelForm):
    class Meta:
        model = EvidenceCrimeReport
        fields = ('document_fir', 'document_witness', 'document_forensic', 'document_arrest', 'document_charge', 'document_case', 'document_final')