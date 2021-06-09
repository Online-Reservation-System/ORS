from django.urls import path
from . import views


urlpatterns=[
    path('',views.Welcome,name="Welcome"),
    path('AdminLogin',views.AdminLogin,name="AdminLogin"),
    path('AdminOptions',views.AdminOptions,name="AdminOptions"),
    path('AddAdmin',views.AddAdmin,name="AddAdmin"),
    path('UpdateTrains',views.UpdateTrains,name="UpdateTrains"),
    

    
]