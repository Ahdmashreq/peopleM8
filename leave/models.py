from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save, post_init
from django.dispatch import receiver
from notifications.signals import notify

from employee.models import JobRoll, Employee
from datetime import date
from django.utils.translation import ugettext_lazy as _
from .manager import LeaveManager
from company.models import Enterprise
from datetime import date, datetime
from custom_user.models import User

class LeaveMaster(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='leave_master_bank_master',
                                   verbose_name=_('Enterprise Name'))
    type = models.CharField(max_length=200, verbose_name=_('Leave Type Name'))
    leave_value = models.FloatField(default=0, verbose_name=_('Leave Value'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='LeaveMaster_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='LeaveMaster_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.type


def path_and_rename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user, filename)


class Leave(models.Model):
    leave_type_list = [("A", _("Annual Leave")),
                       ("S", _("Sick Leave")),
                       ("C", _("Casual Leave")),
                       ("U", _("Usual Leave")),
                       ("UP", _("Unpaid Leave")),
                       ("M", _("Maternity/Paternity")),
                       ("O", _("Other")),
                       ("W", _("Working From Home")),
                       ("W", _("Excuse")), ]
    # ###########################################################################################
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)   
    approval = models.ForeignKey(Employee, related_name='approvall', on_delete=models.CASCADE, blank=True,
                                null=True)       
    startdate = models.DateField(verbose_name=_(
        'Start Date'), null=True, blank=False)
    enddate = models.DateField(verbose_name=_(
        'End Date'), null=True, blank=False)
    resume_date = models.DateField(verbose_name=_(
        'Resume Date'), null=True, blank=False)
    # leavetype = models.CharField(max_length=3, choices=leave_type_list, verbose_name=_('Leave Type Name'))
    leavetype = models.ForeignKey(
        LeaveMaster, on_delete=models.CASCADE, verbose_name=_('Leave Type Name'))
    reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255,
                              help_text='add additional information for leave', null=True, blank=True)
    attachment = models.ImageField(
        upload_to=path_and_rename, null=True, blank=True, verbose_name=_('Attachment'))
    status = models.CharField(max_length=20, default='pending')
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='Leave_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='Leave_last_updated_by')
    last_update_date = models.DateField(auto_now=True)
    objects = LeaveManager()

    def __str__(self):
        return ('{0} - {1}'.format(self.leavetype, self.user))
        # return self.user

    @property
    def pretty_leave(self):
        leave = self.leavetype
        user = self.user
        employee = user.employee_set.first().get_full_name
        return ('{0} - {1}'.format(employee, leave))

    @property
    def leave_days(self):
        days_count = ''
        startdate = self.startdate
        enddate = self.enddate
        if startdate > enddate:
            return
        dates = (enddate - startdate)
        return dates.days + 1

    @property
    def leave_approved(self):
        return self.is_approved == True

    @property
    def approve_leave(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'approved'
            self.save()

    @property
    def unapprove_leave(self):
        if self.is_approved:
            self.is_approved = False
            self.status = 'pending'
            self.save()

    @property
    def leaves_cancel(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'cancelled'
            self.save()

    @property
    def reject_leave(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'rejected'
            self.save()

    @property
    def is_rejected(self):
        return self.status == 'rejected'

class EmployeeAbsence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_absence_employee')
    date = models.DateTimeField(auto_now_add=True)
    num_of_days = models.IntegerField(null=False)
    value = models.IntegerField(null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='employee_absence_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name='employee_absence_last_updated_by')
    last_update_date = models.DateField(blank=True, null=True,auto_now_add=True )


class Employee_Leave_balance(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    casual = models.PositiveSmallIntegerField()  # رصيد الاجازات الاعتيادية
    usual = models.PositiveSmallIntegerField()  # رصيد الاجازات العارضة
    carried_forward = models.PositiveSmallIntegerField()  # رصيد الاجازات المرحلة
    absence = models.PositiveSmallIntegerField()  # عدد ايايم الغياب
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='Leave_balance_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name='Leave_balance_last_updated_by')
    last_update_date = models.DateField(auto_now=True, blank=True, null=True, )

    @property
    def total_balance(self):
        total_balance = self.casual + self.usual + self.carried_forward
        return total_balance

    def __str__(self):
        return self.employee.emp_name

    
@receiver(post_save, sender=Leave)
def leave_creation(sender, instance, created, update_fields, **kwargs):
    """
        This function is a receiver, it listens to any save hit on leave model, and send
        a notification to the manager that someone created a leave.
        or send a notification to the person who created the leave, if his leave is processed .
    """
    requestor_emp = instance.user.employee_user.all(
    )[0]  # assuming one employee per user
    # manager_emp = requestor_emp.job_roll_emp_id.filter(
    #     Q(end_date__gt=date.today()) | Q(end_date__isnull=True))[0].manager

    # requestor_emp = instance.ordered_by
    approval_emp = instance.approval
    required_job_roll = JobRoll.objects.get(emp_id = requestor_emp, end_date__isnull=True)
    if required_job_roll.manager:
        manager_emp = required_job_roll.manager.user
    else:
        hr_users = User.objects.filter(groups__name='HR')
        manager_emp = hr_users

    if created:  # check if this is a new leave instance
        data = {"title": "Leave request", "status": instance.status,
                "href": "leave:edit_leave"}
        notify.send(sender=instance.user,
                    recipient=manager_emp,
                    verb='requested', description="{employee} has requested {leave}".format(employee=requestor_emp,
                                                                                            leave=instance.leavetype.type),
                    action_object=instance, level='action', data=data)
    elif 'status' in update_fields:  # check if leave status is updated

        data = {"title": "Leave request", "status": instance.status}
        # send notification to the requestor employee that his request status is updated
        notify.send(sender=manager_emp,
                    recipient=instance.user,
                    verb=instance.status,
                    description="{employee} has {verb} your {leave}".format(employee=approval_emp, verb=instance.status,
                                                                            leave=instance.leavetype.type),
                    action_object=instance, level='info', data=data)

        #  update the old notification for the manager with the new status
        content_type = ContentType.objects.get_for_model(Leave)
        old_notification = manager_emp.notifications.filter(action_object_content_type=content_type,
                                                                 action_object_object_id=instance.id)
        if len(old_notification) > 0:
            old_notification[0].data['data']['status'] = instance.status
            old_notification[0].data['data']['href'] = ""
            old_notification[0].unread = False
            old_notification[0].save()
