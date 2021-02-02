from django.contrib import admin
from company import models
from import_export.admin import ImportExportModelAdmin, ImportMixin
from .resources import DepartmentResource
from . models import Department




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
    fields = (
        'enterprise',
        'department_user',
        'dept_name',
        'parent',
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


@admin.register(models.Working_Days_Policy)
class Working_Days_PolicyAdmin(admin.ModelAdmin):
    fields = (
        'number_of_daily_working_hrs',
        'normal_over_time_hourly_rate',
        'exceptional_over_time_hourly_rate',
        'delay_hours_rate',
        'absence_days_rate',

    )

    def save_model(self, request, instance, form, change):
        user = request.user
        enterprise = request.user.company
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
            instance.enterprise = enterprise
        instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance

@admin.register(models.Working_Hours_Deductions_Policy)
class Working_Hours_Deductions_PolicyAdmin(admin.ModelAdmin):
    fields = (
            'working_days_policy',
            'day_number',
            'delay_rate',
            'notify',
            'susbend',
            'start_date',
            'end_date',
    )

    def save_model(self, request, instance, form, change):
        user = request.user
        enterprise = request.user.company
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
            instance.enterprise = enterprise
        instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance

@admin.register(models.YearlyHoliday)
class YearlyHolidaysAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'start_date',
        'end_date',
        'number_of_days_off',
    )

    def save_model(self, request, instance, form, change):
        user = request.user
        enterprise = request.user.company
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
            instance.enterprise = enterprise
        instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(models.Year)
class YearAdmin(admin.ModelAdmin):
    fields = (
        'year',
    )

    def save_model(self, request, instance, form, change):
        user = request.user
        enterprise = request.user.company
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
            instance.enterprise = enterprise
        instance.last_update_by = user
        instance.save()
        return instance



#class DepartmentResourceAdmin(ImportExportModelAdmin):
 #   resource_class = DepartmentResource
  #  def get_resource_kwargs(self, request, *args, **kwargs):
        #""" Passing request to resource obj to control exported fields dynamically """
   #     return {'request': request}
