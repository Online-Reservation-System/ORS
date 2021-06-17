from django.core.checks import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from .models import Admin, AppUser,Train,Ticket
from django.contrib import messages
from django.conf import settings
from .models import Transaction
from django.utils import timezone
import random,string,datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def welcome(request):
    request.session['trainid']=''
    request.session['no_of_seats']=''
    request.session['username']=''
    request.session['userid']=''
    request.session["dates"]=''
    return render(request,"welcome.html")
#--------------------------------------------------------------------------------------------------------------------
def adminlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        Admin_cred=Admin.objects.all()
        flag=0
        for user in Admin_cred:
            if username==user.username and password==user.password:
                flag=1
                Train_data = Train.objects.all().order_by("starttime")
                return render(request,"AdminOptions.html",{"name":user.name,"Train_data":Train_data})
                    
        if  flag==0:
            messages.add_message(request, messages.INFO, 'Invalid credentials!!')
    return render(request,"adminlogin.html")
#------------------------------------------------------------------------------------------------
def adminoptions(request):
    Train_data = Train.objects.all().order_by("starttime")
    return render(request,"adminoptions.html",{"Train_data":Train_data})
    
#------------------------------------------------------------------------------------------------
def addadmin(request):
    Train_data = Train.objects.all().order_by("starttime")
    if request.method=='POST':
        password=request.POST['password']
        conf=request.POST['confirmpassword']
        print(conf,password)
        if password==conf:
                new_admin=Admin()
                new_admin.name= request.POST['name']
                new_admin.username= request.POST['username']
                new_admin.password= request.POST['password']
                new_admin.save()
                messages.add_message(request, messages.INFO, 'ADDED ADMIN SUCCESSFULLY!!')
                
                return render(request, 'addadmin.html',{"Train_data":Train_data})  
        else:
            messages.add_message(request, messages.INFO, 'password missmatch!!')

    return render(request, 'addadmin.html',{"Train_data":Train_data}) 
#---------------------------------------------------------------------------------------------------
def updatetrains(request):
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
        cost = request.POST.get("cost")
        
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
                train.Ticketcost=cost
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
                train.Ticketcost=cost
                train.save()

        print("Submitteeddd!!!")
    return render(request,"UpdateTrains.html",{"Train_data":Train_data})
#-------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
def useroptions(request):
    return render(request,"useroptions.html")
#-----------------------------------------------------------------------------------    
def userregister(request):
    if request.method=='POST':
        email=request.POST["email"]
        try:
            email = AppUser.objects.get(email=email)
            if email!=None:
                 messages.add_message(request, messages.INFO, 'Email already exists!!')
        except:
            try:
                username=request.POST["username"]
                username = AppUser.objects.get(username=username)
                if username!=None:
                    messages.add_message(request, messages.INFO, 'Username taken!!')
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
                    messages.add_message(request, messages.INFO, 'password missmatch!!')
    return render(request,"userregister.html")
        
def userlogin(request):
    if request.method=="POST":
        username = request.POST["username"]
        passwd = request.POST["password"]
        try:
            user = AppUser.objects.get(username=username)
            if user!=None:
                if user.username==username and user.password==passwd:
                    request.session['username']=username
                    request.session['userid']=user.user_id
                    Traindata = Train.objects.filter(status="Running")
                    return render(request,"trainslist.html",{"Traindata":Traindata})


                else:
                    messages.add_message(request, messages.INFO, 'Invalid credentials!!')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.INFO,"Your account doesn't exist.")
    return render(request,"userlogin.html")
def trainslist(request):
        Traindata = Train.objects.filter(status="Running")
        return render(request,"trainslist.html",{"Traindata":Traindata})

#-----------------------------------------------------------------------------------
def BookTickets(request):
    Traindata = Train.objects.filter(status="Running")
    if request.method=="POST":
        id=request.POST["trainid"]
        no_of_seats=request.POST["seats"]
        request.session['trainid']=id
        dates=request.POST["dates"]
        request.session["dates"]=dates
        request.session['no_of_seats']=no_of_seats
        try:
            Train_data=Train.objects.get(trainid=id)
            return render(request,"Payment.html",{"Traindata":Train_data,"seats":no_of_seats})
        except Exception as e:
            print(e)
            messages.add_message(request,messages.INFO,"Train Doesn't Exist!")
    return render(request,"BookTickets.html",{"Traindata":Traindata})
        
#------------------------------------------------------------------------
def Payment(request):
    if request.method=="POST":
        Nameoncard=request.POST["nameoncard"]
        cvv=request.POST["cvv"]
        cardnum=request.POST["cardno"]
        train=Train.objects.get(trainid=request.session["trainid"])
        train.filled=train.filled+int(request.session['no_of_seats'])
        train.save()
        amount=train.Ticketcost*int(request.session['no_of_seats'])
        #----new Ticket Object------
        ticketrec=Ticket()
        randomstring_length = 5
        ticketid = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = randomstring_length)))
        while ticketid in Ticket.objects.values_list('ticket_id', flat=True):
            ticketid = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = randomstring_length)))
     
        ticketrec.ticket_id=ticketid
        ticketrec.trainid= request.session['trainid']
        ticketrec.passanger_id=str(request.session['userid'])+'174'
        ticketrec.passanger_name = request.session['username']
        ticketrec.status="BOOKED"
        ticketrec.seats=int(request.session['no_of_seats'])
        ticketrec.amount=amount
        
        train = Train.objects.get(trainid=request.session["trainid"])
        ticketrec.journeydate = request.session["dates"]
        ticketrec.save()

        #-------new Transaction Object-----
        trans=Transaction()
        trans.username=request.session['username']
        trans.nameoncard=Nameoncard
        trans.cvv=cvv
        trans.cardno=cardnum
        trans.amount=amount
        trans.time=  timezone.now()
        trans.save()
        messages.add_message(request, messages.INFO,"Booked succesfully!!!")
        Train_data=Train.objects.get(trainid=request.session['trainid'])
    return render(request,"Payment.html",{"Traindata":Train_data,"seats":request.session['no_of_seats']})




def showbookedtickets(request):
    Tickets = Ticket.objects.filter(passanger_name=request.session['username'])
    return render(request,"showbookedtickets.html",{"Tickets":Tickets})



def CancelTickets(request):
    
    if request.method=="POST":
        ticketid=request.POST["ticketid"]
        try:
            Tick= Ticket.objects.get(ticket_id=ticketid)
            trainids=Tick.trainid
            train = Train.objects.get(trainid=trainids)
            if Tick.status=="BOOKED":
                Tick.status="CANCELLED"
                Tick.save()
                train.filled=train.filled-Tick.seats
                train.save()

            messages.add_message(request, messages.INFO,"Cancelled ..Amount will be refunded soon!!!")
        except Exception as e:
            print(e)
            messages.add_message(request,messages.INFO,"Invalid Ticket ID")
    Tickets = Ticket.objects.filter(passanger_name=request.session['username'])
    return render(request,"CancelTickets.html",{"Tickets":Tickets})

