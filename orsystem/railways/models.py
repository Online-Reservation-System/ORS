from django.db import models

# Create your models here.
class Admin(models.Model):
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

class Train(models.Model):
    trainid = models.CharField(max_length=5,primary_key=True)
    trainname = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    totalseats = models.IntegerField()
    filled = models.IntegerField()
    status = models.CharField(max_length=20)
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10,primary_key=True)
    trainid = models.ForeignKey(Train, verbose_name="TrainID", on_delete=models.CASCADE)
    passanger_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    