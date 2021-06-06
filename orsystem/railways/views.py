from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User

# Create your views here.
def Welcome(request):
    return render(request,"Welcome.html")
def AdminLogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,"Welcome.html")
        else:
            return render(request,"AdminLogin.html")
            
    else:
        return render(request,"AdminLogin.html")