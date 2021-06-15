from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from .models import Admin,Train,AppUser,Transaction,Ticket
from django.contrib import messages
from django.conf import settings
import random
import string  
from django.utils import timezone
import pandas as pd

# Create your views here.
def Welcome(request):
    request.session['userid']=''
    request.session['username']=''
    request.session['trainid']=''
    request.session['no_of_seats']=0
    request.session['amount'] = 0
    return render(request,"Welcome.html")
def AdminLogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        Admin_cred=Admin.objects.all()
        for user in Admin_cred:
            if username==user.username:
                if password==user.password:
                    Train_data = Train.objects.all().order_by("starttime")
                    return render(request,"AdminOptions.html",{"name":user.name,"Train_data":Train_data})
                else:
                    messages.add_message(request, messages.INFO, 'Invalid credentials')

    return render(request,"AdminLogin.html")
def AdminOptions(request):
    Train_data = Train.objects.all().order_by("starttime")
    return render(request,"AdminOptions.html",{"Train_data":Train_data})

def UpdateTrains(request):
    Train_data = Train.objects.all().order_by("starttime")
    if request.method=='POST':
        id=request.POST["trainid"]
        name=request.POST["trainname"]
        status=request.POST["status"]
        source=request.POST["source"]
        dest=request.POST["destination"]
        start=request.POST["starttime"]
        end=request.POST["endtime"]
        totalseats=request.POST.get("totalseats")
        filled=request.POST.get("filled")
        
        if totalseats!=None and filled!=None:
            try:
                train=Train.objects.get(trainid=id)
                train.trainid=id
                train.trainname=name
                train.status=status
                train.source=source
                train.destination=dest
                train.starttime=start
                train.endtime=end
                train.totalseats=totalseats
                train.filled=filled
                train.save()
            except:
                train=Train()
                train.trainid=id
                train.trainname=name
                train.status=status
                train.source=source
                train.destination=dest
                train.starttime=start
                train.endtime=end
                train.totalseats=totalseats
                train.filled=filled
                train.save()

        
    return render(request,"UpdateTrains.html",{"Train_data":Train_data})

def AddAdmin(request):
    if request.method=='POST':
        passwd = request.POST['password']
        confpwd = request.POST['confirmpassword']
        if passwd == confpwd:
                new_admin=Admin()
                new_admin.name= request.POST.get('name')
                new_admin.username= request.POST.get('username')
                new_admin.password= request.POST.get('password')
                new_admin.save()
                messages.add_message(request, messages.INFO, 'ADDED ADMIN SUCCESSFULLY!!')
                
                return render(request, 'AddAdmin.html')  
        else:
            messages.add_message(request, messages.INFO, 'Password missmatch!!')

    return render(request,"AddAdmin.html")

def UserLogin(request):
    if request.method=="POST":
        username = request.POST["username"]
        passwd = request.POST["password"]
        try:
            user = AppUser.objects.get(username=username)
            if user!=None:
                if user.username==username and user.password==passwd:
                    Traindata = Train.objects.filter(status="Running")
                    request.session["userid"]=user.user_id
                    request.session['username']=user.username
                    return render(request,"Trainlist.html",{"Traindata":Traindata})
                else:
                    messages.add_message(request, messages.INFO, 'Invalid credentials')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.INFO,"Your account doesn't exist.")

        return render(request,"UserLogin.html")

    else:
        return render(request,"UserLogin.html")


def UserRegister(request):
    if request.method=='POST':
        try:
            email=request.POST['email']
            user = AppUser.objects.get(email=email)
            if user!=None:
                messages.add_message(request,messages.INFO,"Email already exists!")
        except:
            try:
                username = request.POST["username"]
                user = AppUser.objects.get(username=username)
                if user!=None:
                    messages.add_message(request,messages.INFO,"Username Already Taken!")
            except:
                password=request.POST["password"]
                confpassword=request.POST["confirmpassword"]
                if password==confpassword:
                    user=AppUser()
                    user.name=request.POST["name"]
                    user.username=request.POST["username"]
                    user.password=password
                    user.email=request.POST["email"]
                    user.phone=request.POST["phonenumber"]
                    user.save()
                    messages.add_message(request, messages.INFO, 'User Registered!! Login now')
                else:
                    messages.add_message(request, messages.INFO, 'Password missmatch!!')

    return render(request,"UserRegistration.html")


def Trainlist(request):
        Traindata = Train.objects.filter(status="Running")
        return render(request,"Trainlist.html",{"Traindata":Traindata})
def BookTickets(request):
    Traindata = Train.objects.filter(status="Running")
    if request.method=="POST":
        id=request.POST.get("trainid")
        no_of_seats=request.POST.get("seats")
        request.session['trainid']=id
        request.session['seats']=no_of_seats
        try:
            print(request.session['trainid'])
            Train_data=Train.objects.get(trainid=request.session["trainid"])
            request.session['amount']=int(Train_data.Ticketcost) * int(no_of_seats)
            return render(request,"Payment.html",{"Traindata":Train_data,"seats":no_of_seats})
        except Exception as e:
            print(e)
            messages.add_message(request,messages.INFO,"Train Doesn't Exist!")


    return render(request,"BookTickets.html",{"Traindata":Traindata})
def Payment(request):
    #transaction object
    if request.method=="POST":

        randomstring_length = 5
        ticketid = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = randomstring_length)))

        while ticketid in Ticket.objects.values_list('ticket_id', flat=True):
            ticketid = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = randomstring_length)))


        newticket = Ticket()
        newticket.ticket_id = ticketid
        newticket.trainid = request.session["trainid"]
        train = Train.objects.get(trainid=request.session["trainid"])
        newticket.journeydate = train.starttime.strftime('%Y-%m-%d')
        newticket.passanger_id = request.session['userid']
        newticket.passanger_name = request.session['username']
        newticket.status = "Booked"
        newticket.save()


        trans = Transaction()
        trans.made_by= request.session['username']
        trans.made_on = timezone.now().strftime('%Y-%m-%d')
        trans.amount = request.session['amount']
        trans.order_id= str(request.session['userid'])+str(ticketid)
        trans.save()
        return render(request,"Payment.html",{"success":"Booked successfully!"})
    return render(request,"Payment.html") 
    
    



