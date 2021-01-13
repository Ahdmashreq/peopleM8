from django.contrib import admin
from task_management import models


# ################ inlines #################
class ProjectTasksInline(admin.TabularInline):
    model = models.Project_Task
    fields = (
        'project',
        'task_name',
        'parent_task',
        'description',
        'scope',
        'assigned_to',
        'status',
        'percentage',
        'task_start_date',
        'task_end_date',
    )

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        if change:
            instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance


# #################### model admin ##########################
@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = (
              'name',
              'description',
              'percentage',
              'start_date',
              'end_date'
    )
    inlines=[
        ProjectTasksInline,
    ]

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        if change:
            instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(models.Project_Task)
class ProjectTaskAdmin(admin.ModelAdmin):
    fields = (
        'project',
        'task_name',
        'parent_task',
        'description',
        'scope',
        'assigned_to',
        'status',
        'percentage',
        'task_start_date',
        'task_end_date',
        'duration_days',
        'total_hours',
    )
    readonly_fields = ('duration_days','total_hours')

    list_display = ('project','task_name', 'assigned_to', 'status','percentage')

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        if change:
            instance.last_update_by = user
        instance.save()
        form.save_m2m()
        return instance
