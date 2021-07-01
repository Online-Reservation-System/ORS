
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
    Ticketcost =models.IntegerField()

class AppUser(models.Model):
    user_id  = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='UserID')
    name = models.CharField(max_length=30)
    username= models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50,unique=True)
    phone=models.BigIntegerField()
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10,primary_key=True)
    trainid = models.CharField(max_length=10)
    passanger_id = models.CharField(max_length=10)
    passanger_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    journeydate = models.CharField(max_length=50)
    seats=models.BigIntegerField()
    amount=models.BigIntegerField()
class Transaction(models.Model):
    id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    username = models.CharField(max_length=50)
    nameoncard = models.CharField(max_length=100)
    cvv = models.IntegerField()
    cardno=models.CharField(max_length=100)
    amount=models.BigIntegerField()
    time=models.DateTimeField()

