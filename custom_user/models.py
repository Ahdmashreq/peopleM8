from django.db import models
from django.contrib.auth.models import AbstractUser

from MashreqPayroll import settings
from company.models import Enterprise
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    emp_type_list = [("A", _("Admin")),
                     ("E", _("Employee"))]
    # ###########################################################################################
    company = models.ForeignKey(Enterprise, null=True, blank=True, on_delete=models.CASCADE, related_name='company_user', verbose_name=_('Name'))
    employee_type = models.CharField(max_length=3, choices=emp_type_list, verbose_name=_('Employee Type'))
    business_unit_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Business Unit Name'))
    reg_tax_num = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Reg Tax Num'))
    commercail_record = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Commercail Record '))


class UserCompany(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='user_fk',
                             verbose_name=_('User'))
    company = models.ForeignKey(Enterprise, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='company', verbose_name=_('Company'))
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='user_company_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='user_company_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username+' ' +self.company.name
