from django import forms
from .models import Resume,Category

class ResumeForm(forms.ModelForm):
    class Meta:
        model=Resume
        fields=['name','surname','father_name','education','experience','image','telephone','email','speciality']
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']

