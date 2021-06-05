from django.shortcuts import render

# Create your views here.
def Welcome(request):
    return render(request,"Welcome.html")
def AdminLogin(request):
    return render(request,"AdminLogin.html")