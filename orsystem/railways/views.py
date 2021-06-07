from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from .models import Admin,Train
from django.contrib import messages

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
    return render(request,"AdminOptions.html")
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