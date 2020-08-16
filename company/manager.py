from django.db import models
from datetime import date
from django.db.models import Q


class CompanyManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(CompanyManager, self).filter(enterprise_user=user).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))


class DepartmentManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(DepartmentManager, self).filter(enterprise=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))

    def get_department(self, user, dept_id, *args, **kwargs):
        return super(DepartmentManager, self).filter(department_user__company=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True)).get(id=dept_id)


class JobManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(JobManager, self).filter(enterprise=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))

    def get_job(self, user, job_id, *args, **kwargs):
        return super(JobManager, self).filter(job_user__company=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True)).get(id=job_id)


class GradeManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(GradeManager, self).filter(enterprise=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))

    def get_job(self, user, grade_id, *args, **kwargs):
        return super(GradeManager, self).filter(grade_user__company=user.company).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True)).get(id=grade_id)


class PositionManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(PositionManager, self).filter(department__enterprise=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))

    def get_position(self, user, position_id, *args, **kwargs):
        return super(PositionManager, self).filter(department__enterprise=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True)).get(id=position_id)


class PolicyManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(PolicyManager, self).filter(enterprise=user.company).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))

    def get_policy(self, user, policy_id, *args, **kwargs):
        return super(PolicyManager, self).filter(enterprise=user.company).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True)).get(id=policy_id)


class YearlyHolidayManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(YearlyHolidayManager, self).filter(enterprise=user.company).filter(
            Q(start_date__year=date.today().year))

    def get_holiday(self, user, yearly_holiday_id, *args, **kwargs):
        return super(YearlyHolidayManager, self).filter(enterprise=user.company).filter(
            Q(start_date__year=date.today().year)).get(id=yearly_holiday_id)
