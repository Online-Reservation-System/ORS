from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from .models import Admin
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
                    return render(request,"AdminOptions.html",{"name":user.name})
                else:
                    messages.add_message(request, messages.INFO, 'Invalid credentials')

    return render(request,"AdminLogin.html")
def AdminOptions(request):
    return render(request,"AdminOptions.html")