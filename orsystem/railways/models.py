from django.db import models

# Create your models here.
class Admin(models.Model):
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
class Train(models.Model):
    trainid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='TRAINID')
    startstation = models.CharField(max_length=50)
    endstation = models.CharField(max_length=50)
    starttime = models.DateTimeField(auto_now=False)
    endtime = models.DateTimeField(auto_now=False)
    