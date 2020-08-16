from django.conf import settings
from django.db import models
from datetime import date
from django.db.models.signals import pre_save
from home.slugify import unique_slug_generator
from cities_light.models import City, Country
from django.utils.translation import ugettext_lazy as _
from .manager import CompanyManager, DepartmentManager, JobManager, GradeManager, PositionManager, PolicyManager, \
    YearlyHolidayManager


class Enterprise(models.Model):
    enterprise_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_('Company Name'))
    reg_tax_num = models.CharField(max_length=150, verbose_name=_('Reg Tax Num'))
    commercail_record = models.CharField(max_length=150, verbose_name=_('Commercial Record'))
    address1 = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Address1'))
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Phone'))
    mobile = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Mobile'))
    fax = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Fax'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Country'))
    slug = models.SlugField(blank=True, null=True)
    objects = CompanyManager()
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="company_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
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


def slug_enterprise_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_enterprise_generator, sender=Enterprise)


class Department(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='department_enterprise',
                                   verbose_name=_('Enterprise Name'))
    department_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dept_name = models.CharField(max_length=150, verbose_name=_('Department'))
    parent_dept = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name=_('Parent Department'))
    # dept_type   =   models.ForeignKey("defenition.LookupDet", on_delete=models.CASCADE, null=True, blank=True,verbose_name=_('Department Type'))
    objects = DepartmentManager()
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start  Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

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

    def __str__(self):
        return self.dept_name


class Job(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='job_enterprise',
                                   verbose_name=_('Enterprise Name'))
    job_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=100, verbose_name=_('Job Name'))
    job_description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Job Description'))
    objects = JobManager()
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

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
    grade_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade_name = models.CharField(max_length=100, verbose_name=_('Grade Name'))
    grade_description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Grade Description'))
    objects = GradeManager()
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

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
    position_name = models.CharField(max_length=100, verbose_name=_('Position Name'))
    position_description = models.CharField(max_length=255, null=True, blank=True,
                                            verbose_name=_('Position Description'))
    objects = PositionManager()
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

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
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='policy_enterprise',
                                   verbose_name=_('Enterprise Name'))
    policy_description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Policy Description'))
    attachment = models.ImageField(upload_to=path_and_rename, null=True, blank=True, verbose_name=_('Attachment'))
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

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


class WorkingHoursPolicy(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_working_hrs_policy',
                                   verbose_name=_('Enterprise Name'))
    objects = PolicyManager()
    number_of_daily_working_hrs = models.DecimalField(decimal_places=1, max_digits=2)
    normal_over_time_hourly_rate = models.DecimalField(decimal_places=1, max_digits=2)
    exceptional_over_time_hourly_rate = models.DecimalField(decimal_places=1, max_digits=2)
    delay_hours_rate = models.DecimalField(decimal_places=1, max_digits=2)
    absence_days_rate = models.DecimalField(decimal_places=1, max_digits=2)
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="working_hr_policy_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="working_hr_policy_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "Working Hours Policy"


class YearlyHoliday(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_yearly_holidays',
                                   verbose_name=_('Enterprise Name'))
    objects = YearlyHolidayManager()
    name = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name=_('End Date'))
    number_of_days_off = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="holiday_policy_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="holiday_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name + " Holiday"


# class year(models.Model):
#     YearlyHoliday = models.ForeignKey(YearlyHoliday, on_delete=models.CASCADE, verbose_name=_('Holidays'))
#     year = models.IntegerField()
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
#                                    related_name="year_created_by")
#     creation_date = models.DateField(auto_now=False, auto_now_add=True)
#     last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
#                                        related_name="year_update_by")
#     last_update_date = models.DateField(auto_now=True, auto_now_add=False)
#
#     def __str__(self):
#         return self.year
