from django.contrib import admin
from company import models

####################################### Admin Forms #############################################
@admin.register(models.Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    fields = (
        'enterprise_user',
        'name',
        'slug',
        'reg_tax_num',
        'commercail_record',
        'address1',
        'phone',
        'mobile',
        'fax',
        'email',
        'country',
        'start_date',
        'end_date',
    )
    list_display = ('pk', 'name')
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save()
        return instance

@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields =(
         'department_user',
        'dept_name',
        'parent_dept',
        'start_date',
        'end_date',
    )
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance

@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    fields = (
        'job_user',
        'job_name',
        'job_description',
        'start_date',
        'end_date',
    )
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance

@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    fields = (
              'grade_user',
        'grade_name',
        'grade_description',
        'start_date',
        'end_date',
    )
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance

@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    fields = (
             'job',
             'department',
             'grade',
             'position_name',
             'position_description',
             'start_date',
             'end_date',
    )
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance
