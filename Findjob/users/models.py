from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employer','Работадатель'),
        ('admin','Администратор'),
        ('jobfinder','Искатель'),
    )
    role=models.CharField(choices=ROLE_CHOICES,default='jobfinder',max_length=20)

# Create your models here.
