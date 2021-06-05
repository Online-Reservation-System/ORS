from django.urls import path
from . import views


urlpatterns=[
    path('',views.Welcome,name="Welcome"),
    path('AdminLogin',views.AdminLogin,name="AdminLogin"),
    
]