from django.conf import settings
from django.db import models
from employee.models import Employee
from service.models import  Bussiness_Travel
from leave.models import Leave
from datetime import date
from django.utils.translation import ugettext_lazy as _


class Notification(models.Model):
    from_emp= models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notification_from', verbose_name=_('Employee'))
    to_emp= models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notification_to', verbose_name=_('Employee'),null=True, blank=True) #in the case of manager, it has no 'to' field
    message= models.CharField(verbose_name=_('message content'), max_length=255, null=True, blank=True)
    leave= models.ForeignKey(Leave, related_name='notification_leave',on_delete=models.CASCADE, null=True, blank=True)
    bussiness_travel= models.ForeignKey(Bussiness_Travel, related_name='notification_bussiness_travel',on_delete=models.CASCADE, null=True, blank=True)
    timestamp= models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='delivered')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='Notification_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='Notification_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.message
