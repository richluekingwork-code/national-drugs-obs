from django.contrib import admin
from .models import*
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username','role']
    
admin.site.register(CustomUser,UserModel)
admin.site.register(LDEA_User)
admin.site.register(MoJ_User)
admin.site.register(MoH_User)

admin.site.register(MoG_User)
admin.site.register(MoYS_User) 