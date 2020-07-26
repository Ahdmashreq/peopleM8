from django.db import models
from django.contrib.auth.models import AbstractUser
from company.models import Enterprise
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    emp_type_list = [("A", _("Admin")),
                       ("E", _("Employee")) ]
    # ###########################################################################################
    company = models.ForeignKey(Enterprise ,null=True, blank=True, on_delete=models.CASCADE, related_name='company_user',verbose_name=_('Name'))
    employee_type = models.CharField(max_length=3, choices=emp_type_list, verbose_name=_('Employee Type'))
    business_unit_name	=	models.CharField(max_length=150,null=True, blank=True,verbose_name=_('Business Unit Name'))
    reg_tax_num	=	models.CharField(max_length=150,null=True, blank=True,verbose_name=_('Reg Tax Num'))
    commercail_record	=	models.CharField(max_length=150,null=True, blank=True,verbose_name=_('Commercail Record '))
