from django import forms
from resume.models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields=['email','message']
