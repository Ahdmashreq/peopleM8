from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserCompany, Visitor
from .resources import *
from import_export.forms import ImportForm, ConfirmImportForm
from import_export.admin import ImportExportModelAdmin, ImportMixin


@admin.register(User)
class CustomUserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('employee_type','company', 'reg_tax_num', 'commercail_record',)}),

    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('employee_type','company', 'reg_tax_num', 'commercail_record',)}),
    )

@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    models = UserCompany
