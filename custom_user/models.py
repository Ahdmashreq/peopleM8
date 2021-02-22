from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from MashreqPayroll.settings import base
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

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        return super(User, self).save(*args, **kwargs)

class UserCompany(models.Model):
    user = models.ForeignKey(base.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                             related_name='user_fk',
                             verbose_name=_('User'))
    company = models.ForeignKey(Enterprise, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='company', verbose_name=_('Company'))
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='user_company_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='user_company_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username + ' ' + self.company.name


AUTH_USER_MODEL = getattr(base, 'AUTH_USER_MODEL', User)


class Visitor(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, null=False, related_name='visitor', on_delete=models.CASCADE)
    session_key = models.CharField(null=False, max_length=40)
