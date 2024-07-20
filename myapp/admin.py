from django.contrib import admin
from .models import Profile,CustomUser,BlogPost,Category
# Register your models here.


admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(BlogPost)
admin.site.register(Category)