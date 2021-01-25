from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserCompany, Visitor

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    models = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('employee_type','company', 'reg_tax_num', 'commercail_record',)}),

    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('employee_type','company', 'reg_tax_num', 'commercail_record',)}),
    )

@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    models = UserCompany
