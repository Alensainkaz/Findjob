from django.db import models
from users.models import User
from django.conf import settings
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug= models.SlugField(max_length=100)

    def __str__(self):
        return self.name

class Resume(models.Model):
    name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100)
    father_name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    email=models.EmailField(max_length=100)
    experience=models.CharField(max_length=100)
    education=models.CharField(max_length=100)
    telephone=models.IntegerField()
    image=models.ImageField(upload_to='images/', blank=True, null=True)
    speciality=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Message(models.Model):
    email=models.EmailField(max_length=100)
    message=models.TextField()
    sended_at=models.DateTimeField(auto_now_add=True)
    from_user=models.ForeignKey(User,on_delete=models.CASCADE)

# Create your models here.
