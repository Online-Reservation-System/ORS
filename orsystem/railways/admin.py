from django.contrib import admin
from .models import Admin,Train,AppUser,Ticket

# Register your models here.
admin.site.register(Admin)
admin.site.register(Train)
admin.site.register(AppUser)
admin.site.register(Ticket)