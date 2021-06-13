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

class AppUser(models.Model):
    user_id  = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='UserID')
    name = models.CharField(max_length=30)
    username= models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50,unique=True)
    phone=models.BigIntegerField()
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10,primary_key=True)
    trainid = models.ForeignKey(Train, verbose_name="TrainID", on_delete=models.CASCADE)
    passanger_id = models.ForeignKey(AppUser,verbose_name="UserID",on_delete=models.CASCADE)
    passanger_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    
class Transaction(models.Model):
    made_by = models.ForeignKey(AppUser, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
