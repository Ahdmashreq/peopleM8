from django.contrib import admin
from import_export.forms import ImportForm, ConfirmImportForm

from attendance.models import Attendance, Task, Attendance_Interface
from import_export.admin import ImportExportModelAdmin, ImportMixin
from django import forms
from employee.models import Employee
from attendance.resources import AttendanceResource


# @admin.register(Attendance)
# class AttendanceAdmin(admin.ModelAdmin):
#     fields = (
#         'employee',
#         'check_in',
#         'check_out',
#         'work_hours',
#     )
#     readonly_fields = ('date',)
#
#     def save_model(self, request, instance, form, change):
#         user = request.user
#         instance = form.save(commit=False)
#         if not change or not instance.created_by:
#             instance.created_by = user
#         instance.last_update_by = user
#         instance.save()
#         form.save()
#         return instance
admin.site.register(Attendance_Interface)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'attendance',
        'task',
        'start_time',
        'end_time',
        'slug',
    )

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save()
        return instance


@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin):
    resource_class = AttendanceResource
    fields = (
         'employee',
         'date',
         'check_in',
         'check_out',
         'work_hours',
         'slug',
    )
    list_display = ('employee', 'date', 'check_in',  'check_out', 'work_hours',)
