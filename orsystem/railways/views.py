from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from .models import Admin,Train
from django.contrib import messages
from .forms import updateTrainsForm
from django.forms import formset_factory

# Create your views here.
def Welcome(request):
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

