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
class AppUser(models.Model):
    user_id  = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='UserID')
    name = models.CharField(max_length=30)
    username= models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone=models.BigIntegerField()
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10,primary_key=True)
    trainid = models.ForeignKey(Train, verbose_name="TrainID", on_delete=models.CASCADE)
    passanger_id = models.ForeignKey(AppUser,verbose_name="UserID",on_delete=models.CASCADE)
    passanger_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)