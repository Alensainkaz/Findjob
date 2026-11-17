from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'surname', 'father_name', 'city', 'education', 'experience', 'image', 'email', 'speciality']
        widgets = {
            'speciality': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Only a confirmed address is taken; unconfirmed claims never block the real owner
        taken = Resume.objects.filter(email__iexact=email, email_verified=True)
        if self.instance.pk:
            taken = taken.exclude(pk=self.instance.pk)
        if taken.exists():
            raise forms.ValidationError(_('A resume with this email already exists.'))
        return email
