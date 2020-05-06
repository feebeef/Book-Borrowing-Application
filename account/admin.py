from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm
from .models import Account

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'idnum', 'password', 'username')}
        ),
    )
    #this will allow to change these fields in admin module
    
admin.site.register(Account, MyUserAdmin)