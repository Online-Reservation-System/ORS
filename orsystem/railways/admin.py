from django.contrib import admin
from .models import Admin,Train,Ticket,AppUser

# Register your models here.
admin.site.register(Admin)
admin.site.register(Train)
admin.site.register(Ticket)
admin.site.register(AppUser)