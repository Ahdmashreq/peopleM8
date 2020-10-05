from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from employee.models import Employee
from datetime import datetime, date
from string import Template
from home.slugify import unique_slug_generator
from django.utils.translation import ugettext_lazy as _
from company.models import Working_Days_Policy
import datetime as mydatetime


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
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='attendance_interface_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='attendance_interface_last_updated_by')
    last_update_date = models.DateField(auto_now=True)


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, related_name='emp_attendance', on_delete=models.CASCADE, blank=True,
                                 null=True, )
    date = models.DateField(blank=True, null=True, )
    check_in = models.TimeField(blank=True, null=True, )
    check_out = models.TimeField(blank=True, null=True, )
    work_hours = models.CharField(max_length=100, blank=True, null=True)
    normal_hrs = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    normal_overtime_hours = models.DurationField(blank=True, null=True)
    exceptional_hrs = models.TimeField(blank=True, null=True)
    exceptional_overtime = models.TimeField(blank=True, null=True)
    delay_hrs = models.DurationField(blank=True, null=True)
    absence_days = models.IntegerField(blank=True, null=True, default=0)
    day_of_week = models.CharField(max_length=12, blank=True, null=True, )
    slug = models.SlugField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='attendance_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='attendance_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.employee.emp_name

    @property
    def overtime(self):
        print("$$$$$$$$$$$$", self.check_out)
        hrs_end_at = Working_Days_Policy.objects.filter(enterprise=self.employee.enterprise).values("hrs_end_at")[0][
            'hrs_end_at']

        return self.check_out > hrs_end_at

    @property
    def delay(self):
        print("&&&&&&&&&&")
        hrs_start_from = \
            Working_Days_Policy.objects.filter(enterprise=self.employee.enterprise).values("hrs_start_from")[0][
                'hrs_start_from']
        return self.check_in > hrs_start_from

    @property
    def worktime(self):
        return datetime.strptime(str(self.check_out), '%H:%M:%S') - datetime.strptime(
            str(self.check_in), '%H:%M:%S')

    @property
    def how_much_overtime(self):
        hrs_end_at = Working_Days_Policy.objects.filter(enterprise=self.employee.enterprise).values("hrs_end_at")[0][
            'hrs_end_at']
        print("&&&&&&&&&&", hrs_end_at)
        # first_delta = mydatetime.timedelta(hours=self.check_out.hour, minutes=self.check_out.minute,
        #                                    seconds=self.check_out.second)
        # second_delta = mydatetime.timedelta(hours=hrs_end_at.hour, minutes=hrs_end_at.minute,
        #                                    seconds=hrs_end_at.second)
        # difference = first_delta - second_delta

        difference = datetime.combine(datetime.now(), self.check_out) - datetime.combine(datetime.now(), hrs_end_at)
        return difference

    @property
    def how_much_delay(self):
        hrs_start_from = \
        Working_Days_Policy.objects.filter(enterprise=self.employee.enterprise).values("hrs_start_from")[0][
            'hrs_start_from']
        # first_delta = mydatetime.timedelta(hours=self.check_in.hour, minutes=self.check_in.minute,
        #                                    seconds=self.check_in.second)
        # second_delta = mydatetime.timedelta(hours=hrs_start_from.hour, minutes=hrs_start_from.minute,
        #                                     seconds=hrs_start_from.second)
        # difference = first_delta - second_delta
        difference = datetime.combine(datetime.now(), self.check_in) - datetime.combine(datetime.now(), hrs_start_from)
        return difference


class Employee_Attendance_History(models.Model):
    month_list = [
        (1, _('January')), (2, _('February')), (3, _('March')), (4, _('April')),
        (5, _('May')), (6, _('June')), (7, _('July')), (8, _('August')),
        (9, _('September')), (10, _('October')
                              ), (11, _('November')), (12, _('December')),
    ]
    employee = models.ForeignKey(Employee, related_name='employee_attendance_history_employee',
                                 on_delete=models.CASCADE)
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
                                       blank=True, null=True,
                                       related_name='employee_attendance_history_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.employee.emp_name + " " + str(self.month) + " " + str(self.year)


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
        difference = datetime.combine(datetime.now(), instance.check_out) - datetime.combine(datetime.now(),
                                                                                             instance.check_in)
        instance.work_hours = strfdelta(difference, "%H:%M:%S")
        if instance.overtime:
            print("%%%%%%%%overtime")
            overtime = instance.how_much_overtime
            instance.normal_overtime_hours = overtime
        else:
            instance.normal_overtime_hours = mydatetime.timedelta(hours=0, minutes=0, seconds=0)
        if instance.delay:
            print("%%%%%%%%delay")

            delay = instance.how_much_delay
            instance.delay_hrs = delay
            print("*********",delay)
        else:
            instance.delay_hrs = mydatetime.timedelta(hours=0, minutes=0, seconds=0)
    else:
        instance.work_hours = 0
