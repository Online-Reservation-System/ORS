from django.urls import path
from django.urls import URLPattern
from . import views

urlpatterns=[
            path("",views.welcome,name="welcome"),
            path("adminlogin",views.adminlogin,name="adminlogin") ,
            path("adminoptions",views.adminoptions,name="adminoptions"),
            path("addadmin",views.addadmin,name="addadmin") ,
            path("updatetrains",views.updatetrains,name="updatetrains"),
            path("userlogin",views.userlogin,name="userlogin"),
            path("useroptions",views.useroptions,name="useroptions"),
            path("userregister",views.userregister,name="userregister")
            ]
