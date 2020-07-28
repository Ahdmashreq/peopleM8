from django.contrib import admin
from attendance.models import Attendance, Task


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    fields = (
        'employee',
        'check_in',
        'check_out',
        'work_time',
        'slug',
    )
    readonly_fields = ('date',)

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save()
        return instance


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
