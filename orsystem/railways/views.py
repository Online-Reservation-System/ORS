from django.core.checks import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from .models import Admin, AppUser,Train
from django.contrib import messages

# Create your views here.

def welcome(request):
    return render(request,"welcome.html")
#---------------------------------------------------------------------------------------
def adminlogin(request):
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
                    return render(request,"welcome.html")
                else:
                    messages.add_message(request, messages.INFO, 'Invalid credentials')
        except:
            messages.add_message(request, messages.INFO,"Your account doesn't exist.")
    return render(request,"userlogin.html")
    

