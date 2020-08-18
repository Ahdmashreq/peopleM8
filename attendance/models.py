from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from employee.models import Employee
import datetime
from home.slugify import unique_slug_generator


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, related_name='emp_attendance', on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(blank=True, null=True, )
    check_out = models.TimeField(blank=True, null=True)
    work_time = models.CharField(max_length=100, blank=True, null=True)
    normal_hrs = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    normal_overtime = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    exceptional_hrs = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    exceptional_overtime = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    delay_hrs = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True, default=0)
    absence_days = models.IntegerField(blank=True, null=True, default=0)
    slug = models.SlugField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='attendance_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='attendance_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.employee.emp_name

    @property
    def is_late(self):
        return self.check_in > datetime.datetime.strptime('09:00', '%H:%M').time()

    @property
    def how_late(self):
        # return self.check_in - datetime.datetime.strptime('09:00', '%H:%M').time()
        return datetime.datetime.strptime(str(self.check_in), '%H:%M:%S') - datetime.datetime.strptime('09:00:00',
                                                                                                       '%H:%M:%S')

    @property
    def overtime(self):
        return self.check_out > datetime.datetime.strptime('05:00', '%H:%M').time()

    @property
    def how_much_overtime(self):
        # return self.check_in - datetime.datetime.strptime('09:00', '%H:%M').time()
        return datetime.datetime.strptime(str(self.check_out), '%H:%M:%S') - datetime.datetime.strptime('05:00:00',
                                                                                                        '%H:%M:%S')


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


@receiver(pre_save, sender=Attendance)
@receiver(pre_save, sender=Task)
def slug_task_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
