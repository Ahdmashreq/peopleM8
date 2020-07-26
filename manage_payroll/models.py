from django.conf import settings
from django.db import models
from datetime import date
from currencies.models import Currency
from company.models import (Enterprise, Department,Job, Position)
from defenition.models import LookupType, LookupDet
from cities_light.models import City, Country
from defenition.models import InsuranceRule, TaxRule
from django.utils.translation import ugettext_lazy as _


period_typ_list = [('m',_('Monthly')),('w',_('Weekly')),('y',_('Yearly'))]
account_type_list = [('c',_('Company account')),('e',_('Employee account'))]

class Bank_Master(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name= 'enterprise_bank_master', verbose_name=_('Enterprise Name'))
    bank_name = models.CharField(max_length=150,verbose_name=_('Bank Name'))
    branch_name = models.CharField(max_length=150,verbose_name=_('Branch Name'))
    country	=	models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True,verbose_name=_('Country'))
    address = models.CharField(max_length=150, blank=True, null=True,verbose_name=_('Address'))
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE,verbose_name=_('Currency'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE, related_name='bank_created_by')
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE)
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        bank_name = self.bank_name+" "+self.branch_name+" - "+self.currency.code
        return bank_name

class Payment_Type(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name= 'enterprise_payment_type',verbose_name=_('Enterprise Name'))
    type_name = models.CharField(max_length=25,verbose_name=_('Payment Type Name'))
    category = models.ForeignKey(LookupDet, on_delete=models.CASCADE,verbose_name=_('Category'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE, related_name='payment_type_created_by')
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE)
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.type_name

class Payment_Method(models.Model):
    payment_type = models.ForeignKey(Payment_Type, on_delete=models.CASCADE,verbose_name=_('Payment Type'))
    method_name = models.CharField(max_length=25,verbose_name=_('Payment Method Name'))
    bank_name = models.ForeignKey(Bank_Master, on_delete=models.CASCADE,verbose_name=_('Bank Name'))
    account_number = models.CharField(max_length=50,verbose_name=_('Account Number'))
    swift_code = models.CharField(max_length=50, blank=True, null=True,verbose_name=_('Swift Code'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE, related_name='payment_method_created_by')
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE)
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.method_name+", "+self.payment_type.type_name

class Payroll_Period(models.Model):
    period_name	=	models.CharField(max_length=20,verbose_name=_('Period Name'))
    period_code	=	models.CharField(max_length=10,verbose_name=_('Period Code'))
    period_desc	=	models.CharField(max_length=100,verbose_name=_('Description'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by	=	models.IntegerField(default=0)
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.IntegerField(default=0)
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return  self.period_name

class Payroll_Master(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE,related_name='payroll_enterprise', verbose_name=_('Enterprise Name'))
    first_pay_period	=	models.DateField(auto_now=False, auto_now_add=False,verbose_name=_('First Pay Period'))
    payroll_name	=	models.CharField(max_length=255,verbose_name=_('Payroll Name'))
    payment_method = models.ForeignKey(Payment_Type, on_delete=models.CASCADE,verbose_name=_('Payment Method'))
    period_type	=	models.ForeignKey(LookupDet, on_delete=models.CASCADE,verbose_name=_('Period Type'))
    social_insurance = models.ForeignKey(InsuranceRule, on_delete=models.CASCADE, verbose_name=_('Social Insurance'))  # Deductions
    tax_rule = models.ForeignKey(TaxRule, on_delete=models.CASCADE, verbose_name=_('Tax Rule'))  # Deductions

    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by	=	models.IntegerField(default=0)
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.IntegerField(default=0)
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return  self.payroll_name

class Assignment_Batch(models.Model):
    payroll_id	=	models.ForeignKey(Payroll_Master, on_delete=models.CASCADE, null=True, blank=True, related_name='assign_batch_payroll',verbose_name=_('Payroll'))
    assignment_name	=	models.CharField(max_length=50,verbose_name=_('Assignment Name'))
    assignment_code	=	models.CharField(max_length=50,verbose_name=_('Assignment Code'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE, related_name='assignment_batch_created_by')
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE)
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.assignment_name

class Assignment_Batch_Include(models.Model):
    include_batch_id	=	models.ForeignKey(Assignment_Batch, on_delete=models.CASCADE, null=True, blank=True, related_name='assign_include_batch',verbose_name=_('Exclude Batch Id'))
    dept_id	=	models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='assign_include_dept',verbose_name=_('Department'))
    position_id	=	models.ForeignKey(Position , on_delete=models.CASCADE, null=True, blank=True, related_name='assign_include_position',verbose_name=_('Position'))
    job_id	=	models.ForeignKey(Job , on_delete=models.CASCADE, null=True, blank=True, related_name='assign_include_job',verbose_name=_('Job'))
    emp_id	=	models.ForeignKey('employee.Employee' , on_delete=models.CASCADE, null=True, blank=True, related_name='assign_include_emp',verbose_name=_('Employee'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE, related_name='assignment_include_created_by')
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE)
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

class Assignment_Batch_Exclude(models.Model):
    exclude_batch_id	=	models.ForeignKey(Assignment_Batch, on_delete=models.CASCADE, null=True, blank=True, related_name='assign_exclude_batch',verbose_name=_('Deduction'))
    dept_id	=	models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='assign_exclude_dept',verbose_name=_('Department'))
    position_id	=	models.ForeignKey(Position , on_delete=models.CASCADE, null=True, blank=True, related_name='assign_exclude_postion',verbose_name=_('Position'))
    job_id	=	models.ForeignKey(Job , on_delete=models.CASCADE, null=True, blank=True, related_name='assign_exclude_job',verbose_name=_('Job'))
    emp_id	=	models.ForeignKey('employee.Employee' , on_delete=models.CASCADE, null=True, blank=True, related_name='assign_exclude_emp',verbose_name=_('Employee'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE, related_name='assignment_exclude_created_by')
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE)
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)
