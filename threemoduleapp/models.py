from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class CustomUser(AbstractUser):

    user_type = models.CharField(default=1,max_length=255,null=True)
    status = models.IntegerField(default=0,null=True)


class Teacher(models.Model):

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    course = models.CharField(max_length=255,null=True)
    age = models.IntegerField(null=True)
    mobile = models.CharField(max_length=255,null=True)
    Image = models.ImageField(upload_to="images/",null=True,blank=True)

class Student(models.Model):
    
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    course = models.CharField(max_length=255,null=True)
    age = models.IntegerField(null=True)
    mobile = models.CharField(max_length=255,null=True)
    Image = models.ImageField(upload_to="images/",null=True,blank=True)