from django.db import models

# Create your models here.
class  Database_users(models.Model):
    User_Name = models.CharField(max_length=30)
    User_Email = models.EmailField(max_length=50)
    User_password = models.CharField(max_length=100)
    User_otp = models.CharField(max_length=6, default=None)

# Model class for storing information of destinations
class Destination(models.Model):
    destination_name = models.CharField(max_length=20)
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
    destination_image = models.ImageField(upload_to='images')
    discription = models.TextField()
    