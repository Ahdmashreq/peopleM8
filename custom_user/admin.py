from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,UserCompany

# @admin.register(User)
# class User_Admin(admin.ModelAdmin):
#     fields = ('company',)

admin.site.register(User)
admin.site.register(UserCompany)
