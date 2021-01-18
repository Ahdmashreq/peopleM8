from django.conf import settings
from django.db import models
from datetime import date
import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from home.slugify import unique_slug_generator
from cities_light.models import City, Country
from django.utils.translation import ugettext_lazy as _
from .manager import (DepartmentManager, JobManager, GradeManager, PositionManager, WorkingHoursPolicy,
                      YearlyHolidayManager, YearsManager)
from multiselectfield import MultiSelectField
from mptt.models import MPTTModel, TreeForeignKey


class Enterprise(models.Model):
    enterprise_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_user")
    name = models.CharField(max_length=255, verbose_name=_('Company Name'))
    reg_tax_num = models.CharField(
        max_length=150, verbose_name=_('Reg Tax Num'))
    commercail_record = models.CharField(
        max_length=150, verbose_name=_('Commercial Record'))
    address1 = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Address1'))
    phone = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name=_('Phone'))
    mobile = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Mobile'))
    fax = models.CharField(max_length=255, blank=True,
                           null=True, verbose_name=_('Fax'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Country'))
    slug = models.SlugField(blank=True, null=True)
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="company_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name="company_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)
    attribute1 = models.CharField(max_length=255)
    attribute2 = models.CharField(max_length=255)
    attribute3 = models.CharField(max_length=255)
    attribute4 = models.CharField(max_length=255)
    attribute5 = models.CharField(max_length=255)
    attribute6 = models.CharField(max_length=255)
    attribute7 = models.CharField(max_length=255)
    attribute8 = models.CharField(max_length=255)
    attribute9 = models.CharField(max_length=255)
    attribute10 = models.CharField(max_length=255)
    attribute11 = models.CharField(max_length=255)
    attribute12 = models.CharField(max_length=255)
    attribute13 = models.CharField(max_length=255)
    attribute14 = models.CharField(max_length=255)
    attribute15 = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(MPTTModel):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='department_enterprise',
                                   verbose_name=_('Enterprise Name'))
    department_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dept_name = models.CharField(max_length=150, verbose_name=_('Department'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            verbose_name=_('Reporting Department'))

    objects = DepartmentManager()
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start  Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="department_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="department_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)
    attribute1 = models.CharField(max_length=255)
    attribute2 = models.CharField(max_length=255)
    attribute3 = models.CharField(max_length=255)
    attribute4 = models.CharField(max_length=255)
    attribute5 = models.CharField(max_length=255)
    attribute6 = models.CharField(max_length=255)
    attribute7 = models.CharField(max_length=255)
    attribute8 = models.CharField(max_length=255)
    attribute9 = models.CharField(max_length=255)
    attribute10 = models.CharField(max_length=255)
    attribute11 = models.CharField(max_length=255)
    attribute12 = models.CharField(max_length=255)
    attribute13 = models.CharField(max_length=255)
    attribute14 = models.CharField(max_length=255)
    attribute15 = models.CharField(max_length=255)

    class MPTTMeta:
        order_insertion_by = ['dept_name']

    def __str__(self):
        return self.dept_name


class Job(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='job_enterprise',
                                   verbose_name=_('Enterprise Name'))
    job_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=100, verbose_name=_('Job Name'))
    job_description = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Job Description'))
    objects = JobManager()
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="job_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="job_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)
    attribute1 = models.CharField(max_length=255)
    attribute2 = models.CharField(max_length=255)
    attribute3 = models.CharField(max_length=255)
    attribute4 = models.CharField(max_length=255)
    attribute5 = models.CharField(max_length=255)
    attribute6 = models.CharField(max_length=255)
    attribute7 = models.CharField(max_length=255)
    attribute8 = models.CharField(max_length=255)
    attribute9 = models.CharField(max_length=255)
    attribute10 = models.CharField(max_length=255)
    attribute11 = models.CharField(max_length=255)
    attribute12 = models.CharField(max_length=255)
    attribute13 = models.CharField(max_length=255)
    attribute14 = models.CharField(max_length=255)
    attribute15 = models.CharField(max_length=255)

    def __str__(self):
        return self.job_name


class Grade(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='grade_enterprise',
                                   verbose_name=_('Enterprise Name'))
    grade_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade_name = models.CharField(max_length=100, verbose_name=_('Grade Name'))
    grade_description = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Grade Description'))
    objects = GradeManager()
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="grade_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="grade_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)
    attribute1 = models.CharField(max_length=255)
    attribute2 = models.CharField(max_length=255)
    attribute3 = models.CharField(max_length=255)
    attribute4 = models.CharField(max_length=255)
    attribute5 = models.CharField(max_length=255)
    attribute6 = models.CharField(max_length=255)
    attribute7 = models.CharField(max_length=255)
    attribute8 = models.CharField(max_length=255)
    attribute9 = models.CharField(max_length=255)
    attribute10 = models.CharField(max_length=255)
    attribute11 = models.CharField(max_length=255)
    attribute12 = models.CharField(max_length=255)
    attribute13 = models.CharField(max_length=255)
    attribute14 = models.CharField(max_length=255)
    attribute15 = models.CharField(max_length=255)

    def __str__(self):
        return self.grade_name


class Position(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, related_name='position_job_fk',
                            verbose_name=_('Job'))
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='position_dept_fk', verbose_name=_('Department'))
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True, related_name='position_grade_fk',
                              verbose_name=_('Grade'))
    position_name = models.CharField(
        max_length=100, verbose_name=_('Position Name'))
    position_description = models.CharField(max_length=255, null=True, blank=True,
                                            verbose_name=_('Position Description'))
    objects = PositionManager()
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="position_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="position_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)
    attribute1 = models.CharField(max_length=255)
    attribute2 = models.CharField(max_length=255)
    attribute3 = models.CharField(max_length=255)
    attribute4 = models.CharField(max_length=255)
    attribute5 = models.CharField(max_length=255)
    attribute6 = models.CharField(max_length=255)
    attribute7 = models.CharField(max_length=255)
    attribute8 = models.CharField(max_length=255)
    attribute9 = models.CharField(max_length=255)
    attribute10 = models.CharField(max_length=255)
    attribute11 = models.CharField(max_length=255)
    attribute12 = models.CharField(max_length=255)
    attribute13 = models.CharField(max_length=255)
    attribute14 = models.CharField(max_length=255)
    attribute15 = models.CharField(max_length=255)

    def __str__(self):
        return self.position_name


def path_and_rename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user, filename)


class Enterprise_Policies(models.Model):
    # Company attachemnts
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='policy_enterprise',
                                   verbose_name=_('Enterprise Name'))
    policy_description = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Policy Description'))
    attachment = models.ImageField(
        upload_to=path_and_rename, null=True, blank=True, verbose_name=_('Attachment'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="policy_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="policy_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)
    attribute1 = models.CharField(max_length=255)
    attribute2 = models.CharField(max_length=255)
    attribute3 = models.CharField(max_length=255)
    attribute4 = models.CharField(max_length=255)
    attribute5 = models.CharField(max_length=255)
    attribute6 = models.CharField(max_length=255)
    attribute7 = models.CharField(max_length=255)
    attribute8 = models.CharField(max_length=255)
    attribute9 = models.CharField(max_length=255)
    attribute10 = models.CharField(max_length=255)
    attribute11 = models.CharField(max_length=255)
    attribute12 = models.CharField(max_length=255)
    attribute13 = models.CharField(max_length=255)
    attribute14 = models.CharField(max_length=255)
    attribute15 = models.CharField(max_length=255)

    def __str__(self):
        return self.position_name


class Working_Days_Policy(models.Model):
    class Meta:
        unique_together = ['enterprise', 'week_end_days']
    week_days = (
        (5, "Saturday"),
        (6, "Sunday"),
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
    )
    #######################################################################################################
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_working_hrs_policy',
                                   verbose_name=_('Enterprise Name'))
    objects = WorkingHoursPolicy()
    number_of_daily_working_hrs = models.DecimalField(
        decimal_places=2, max_digits=3, default=8)
    week_end_days = MultiSelectField(
        max_length=100, choices=week_days, null=True, blank=True)
    normal_over_time_hourly_rate = models.DecimalField(
        decimal_places=2, max_digits=3)
    exceptional_over_time_hourly_rate = models.DecimalField(
        decimal_places=2, max_digits=3)
    hrs_start_from = models.TimeField(
        blank=True, null=True, verbose_name=_('Working Hours From'))
    hrs_end_at = models.TimeField(
        blank=True, null=True, verbose_name=_('Working Hours To'))
    delay_allowed = models.TimeField(
        blank=True, null=True, verbose_name=_('Delay allowed'))
    delay_starts_from = models.TimeField(
        blank=True, null=True, verbose_name=_('Delay calculation starts from'))
    absence_starts_from = models.TimeField(
        blank=True, null=True, verbose_name=_('Absence calculation starts from'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="working_hr_policy_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name="working_hr_policy_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.enterprise.name + "Working Hours Policy"


class Working_Hours_Deductions_Policy(models.Model):
    class Meta:
        unique_together = ['working_days_policy', 'day_number']

    working_days_policy = models.ForeignKey(
        Working_Days_Policy, blank=True, null=True, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    delay_rate = models.DecimalField(
        decimal_places=2, max_digits=3, default=0.0)
    notify = models.BooleanField(default=False, )
    susbend = models.BooleanField(default=False, )
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="working_hr_deductions_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name="working_hr_deductions_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "Day Number " + str(self.day_number)


class Year(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_year',
                                   verbose_name=_('Enterprise Name'))
    objects = YearsManager()
    year = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="year_created_by")
    creation_date = models.DateField(auto_now=False, auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name="year_update_by")
    last_update_date = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.year)


class YearlyHoliday(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_yearly_holidays',
                                   verbose_name=_('Enterprise Name'))
    year = models.ForeignKey(
        Year, on_delete=models.CASCADE, verbose_name=_('Year'), blank=True, null=True)
    objects = YearlyHolidayManager()
    name = models.CharField(max_length=255)
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name=_('End Date'))
    number_of_days_off = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="holiday_policy_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="holiday_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name + " Holiday"


@receiver(pre_save, sender=YearlyHoliday)
def working_time(sender, instance, *args, **kwargs):
    instance.number_of_days_off = (
        instance.end_date - instance.start_date).days + 1
