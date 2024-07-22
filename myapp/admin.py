from django.contrib import admin
from .models import Profile,CustomUser,BlogPost,Category,Appointment
# Register your models here.


admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Appointment)