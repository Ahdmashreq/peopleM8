from django.conf import settings
from django.db import models
from datetime import date, datetime
from company.models import Enterprise


status_list = (
               ('planned','Planned'),
               ('in-progress','In Progress'),
               ('complete','Complete'),
               ('testing','Under Test'),
               ('closed','Closed'),
)
periority_list = (
               ('normal','Normal'),
               ('medium','Medium'),
               ('high','High'),
)
class Project(models.Model):
    company = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    percentage = models.PositiveSmallIntegerField(default=0)
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Project_Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parent_task = models.ForeignKey('Project_Task', on_delete=models.CASCADE, blank=True, null=True)
    task_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    scope = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True, choices=status_list)
    assigned_to = models.CharField(max_length=200, blank=True, null=True)
    percentage = models.PositiveSmallIntegerField(default=0)
    task_start_date = models.DateField(default=date.today)
    task_end_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_task_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    last_update_date = models.DateField(auto_now=True)

    @property
    def duration_days(self):
        num_of_days = self.task_end_date.day - self.task_start_date.day + 1
        return num_of_days

    @property
    def total_hours(self):
        total_hours = self.duration_days*8
        return total_hours

    def __str__(self):
        return self.task_name
