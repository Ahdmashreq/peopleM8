from django.conf import settings
from django.db import models
from employee.models import JobRoll
from datetime import date
from django.utils.translation import ugettext_lazy as _
from .manager import LeaveManager


class LeaveMaster(models.Model):
    type = models.CharField(max_length=100, verbose_name=_('Leave Type Name'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='LeaveMaster_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='LeaveMaster_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.type)

def path_and_rename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user, filename)

class Leave(models.Model):
    leave_type_list = [("A", _("Annual Leave")),
                       ("S", _("Sick Leave")),
                       ("C", _("Casual Leave")),
                       ("U", _("Unpaid Leave")),
                       ("M", _("Maternity/Paternity")),
                       ("O", _("Other")) ]
    # ###########################################################################################
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)
    startdate = models.DateField(verbose_name=_('Start Date'), null=True, blank=False)
    enddate = models.DateField(verbose_name=_('End Date'), null=True, blank=False)
    resume_date = models.DateField(verbose_name=_('Resume Date'), null=True, blank=False)
    leavetype = models.CharField(max_length=3, choices=leave_type_list, verbose_name=_('Leave Type Name'))
    reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255,
                              help_text='add additional information for leave', null=True, blank=True)
    attachment = models.ImageField(upload_to=path_and_rename, null=True, blank=True, verbose_name=_('Attachment'))
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
