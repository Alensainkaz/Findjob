from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model=Resume
        fields=['name','surname','father_name','education','experience','image','telephone','email','speciality']
        widgets={
            'speciality':forms.Select(attrs={'class':'form-control'})
        }