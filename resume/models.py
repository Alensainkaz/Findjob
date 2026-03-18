from django.db import models
from users.models import User
from django.conf import settings
SPECIALITY_CHOICES = [
    ('finansist','Finansist'),
    ('architecture','Architecture'),
    ('Sales manager','Sales Manager'),
    ('Sportsman','Sportsman'),
    ('Programmer','Programmer'),
]
class Resume(models.Model):
    name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100)
    father_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    experience=models.CharField(max_length=100)
    education=models.CharField(max_length=100)
    telephone=models.CharField(name='telephone')
    image=models.ImageField(upload_to='images/', blank=True, null=True)
    speciality=models.CharField(max_length=100,choices=SPECIALITY_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Message(models.Model):
    email=models.EmailField(max_length=100)
    message=models.TextField()
    sended_at=models.DateTimeField(auto_now_add=True)
    from_user=models.ForeignKey(User,on_delete=models.CASCADE)
