from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from employee.models import Employee
from datetime import datetime, date
from string import Template
from tablib import Dataset
from home.slugify import unique_slug_generator
from django.utils.translation import ugettext_lazy as _



class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


class Attendance_Interface(models.Model):
    employee = models.PositiveIntegerField()
    date = models.DateField()
    check_in = models.TimeField(blank=True, null=True, )
    check_out = models.TimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='attendance_interface_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='attendance_interface_last_updated_by')
    last_update_date = models.DateField(auto_now=True)


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, related_name='emp_attendance', on_delete=models.CASCADE, blank=True, null=True,)
    date = models.DateField(blank=True, null=True,)
    check_in = models.TimeField(blank=True, null=True, )
    check_out = models.TimeField(blank=True, null=True)
    work_hours = models.CharField(max_length=100, blank=True, null=True)
    normal_hrs = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    normal_overtime_hours = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    exceptional_hrs = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    exceptional_overtime = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    delay_hrs = models.TimeField(blank=True, null=True)
    absence_days = models.IntegerField(blank=True, null=True, default=0)
    day_of_week = models.CharField(max_length=12, blank=True, null=True,)
    slug = models.SlugField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='attendance_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='attendance_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.employee.emp_name

    @property
    def overtime(self):
        return self.check_out > datetime.datetime.strptime('05:00', '%H:%M').time()

    @property
    def worktime(self):
        return datetime.datetime.strptime(str(self.check_out), '%H:%M:%S') - datetime.datetime.strptime(str(self.check_in), '%H:%M:%S')

    @property
    def how_much_overtime(self):
        return datetime.datetime.strptime(str(self.check_out), '%H:%M:%S') - datetime.datetime.strptime('05:00:00',
                                                                                                        '%H:%M:%S')

class Employee_Attendance_History(models.Model):
    month_list = [
        (1, _('January')), (2, _('February')), (3, _('March')), (4, _('April')),
        (5, _('May')), (6, _('June')), (7, _('July')), (8, _('August')),
        (9, _('September')), (10, _('October')
                              ), (11, _('November')), (12, _('December')),
    ]
    employee = models.ForeignKey(Employee, related_name='employee_attendance_history_employee', on_delete=models.CASCADE)
    month = models.PositiveIntegerField(choices=month_list)
    year = models.PositiveIntegerField()
    attendance_days = models.PositiveIntegerField(default=0, blank=True, null=True)
    leave_days = models.PositiveIntegerField(default=0, blank=True, null=True)
    absence_days = models.PositiveIntegerField(default=0, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='employee_attendance_history_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='employee_attendance_history_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.employee.emp_name +" "+str(self.month)+" "+str(self.year)


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    attendance = models.ForeignKey(Attendance, related_name='attendance', on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='task_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='task_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.task


# @receiver(pre_save, sender=Attendance)
@receiver(pre_save, sender=Task)
def slug_task_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

@receiver(pre_save, sender=Attendance)
def working_time(sender, instance, *args, **kwargs):
    if instance.check_out:
        difference = datetime.combine(datetime.now(), instance.check_out) - datetime.combine(datetime.now(), instance.check_in)
        instance.work_hours = strfdelta(difference, "%H:%M:%S")
    else:
        instance.work_hours = 0
