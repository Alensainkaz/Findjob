from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 
class User(AbstractUser):
    ROLE_CHOICES = (
        ('employer','Работадатель'),
        ('admin','Администратор'),
        ('jobfinder','Искатель'),
    )
    role=models.CharField(choices=ROLE_CHOICES,default='jobfinder',max_length=20)

class EmailVerificationToken(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    token=models.UUIDField(default=uuid.uuid4, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)