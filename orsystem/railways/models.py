from django.db import models

# Create your models here.
class Admin(models.Model):
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=10)
    password=models.CharField(max_length=10)
class Train(models.Model):
    trainid = models.CharField(max_length=10,primary_key=True)
    trainname = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    totalseats = models.IntegerField()
    filled = models.IntegerField()
    status = models.CharField(max_length=20)