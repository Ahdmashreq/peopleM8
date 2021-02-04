from django.contrib import admin
from leave import models


@admin.register(models.LeaveMaster)
class Leave_Master_Admin(admin.ModelAdmin):
    fields = (
        'type',
        'leave_value',
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


@admin.register(models.Leave)
class Leave_Admin(admin.ModelAdmin):
    fields = (
        'user',
        'startdate',
        'enddate',
        'resume_date',
        'leavetype',
        'reason',
        'status',
        'attachment',
        'is_approved',
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


@admin.register(models.Employee_Leave_balance)
class Employee_Leave_balance_Admin(admin.ModelAdmin):
    fields = (
        'employee',
        'casual',
        'usual',
        'carried_forward',
        'absence',
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
