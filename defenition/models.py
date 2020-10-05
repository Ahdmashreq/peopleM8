from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from datetime import date
from .manager import (LookupTypeManager,InsuranceRuleManager,TaxRuleManager)
from company.models import Enterprise

class LookupType(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE,related_name='enterprise_lookup_type', verbose_name=_('Enterprise Name'))
    lookup_type_name	=	models.CharField(max_length=100,verbose_name=_('Lookup Type'))
    lookup_type_description	=	models.CharField(max_length=255, null=True, blank=True,verbose_name=_('Description'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,blank=True, null=True ,verbose_name=_('Start Date'))
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by =    models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE,related_name="lookup_type_created_by")
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,on_delete=models.CASCADE,related_name="lookup_type_last_update_by")
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)
    objects = LookupTypeManager()
    def __str__(self):
        return self.lookup_type_name

class LookupDet(models.Model):
    lookup_type_fk	=	models.ForeignKey(LookupType, on_delete=models.CASCADE,related_name='lookup_type_fk',verbose_name=_('Lookup Type'))
    name	=	models.CharField(max_length=50,verbose_name=_('Name'))
    code	=	models.CharField(max_length=50,verbose_name=_('Code'))
    description	=	models.CharField(max_length=255, null=True, blank=True,verbose_name=_('Description'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date') )
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by =    models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE,related_name="lookup_det_created_by")
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.CASCADE,related_name="lookup_det_last_update_by")
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

class InsuranceRule(models.Model):
    enterprise_name = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name=_('Enterprise Name'))
    name = models.CharField(max_length=100,verbose_name=_('Insurance Rule Name'))
    basic_deduction_percentage = models.FloatField(verbose_name=_('Basic Deduction Percentage'))
    variable_deduction_percentage = models.FloatField(verbose_name=_('Variable Deduction Percentage'))
    maximum_insurable_basic_salary = models.FloatField(verbose_name=_('Maximum Insurable Basic Salary'))
    maximum_insurable_variable_salary = models.FloatField(verbose_name=_('Maximum Insurable Variable Salary'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date') )
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by =    models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE,related_name="InsuranceRule_created_by")
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,on_delete=models.CASCADE,related_name="InsuranceRule_last_update_by")
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)
    objects = InsuranceRuleManager()
    def __str__(self):
        return self.name

class TaxRule(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name=_('Enterprise Name'))
    name = models.CharField(max_length=255,verbose_name=_('Tax Rule Name'))
    personal_exemption = models.FloatField(verbose_name=_('Personal Exemption'))
    round_down_to_nearest_10 = models.BooleanField(default=True,verbose_name=_('Round To Nearest Zero'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date') )
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by =    models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,on_delete=models.CASCADE,related_name="TaxRule_created_by")
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,on_delete=models.CASCADE,related_name="TaxRule_last_update_by")
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)
    objects = TaxRuleManager()
    def __str__(self):
        return self.name

class TaxSection(models.Model):
    name = models.CharField(max_length=255,verbose_name=_('Name'))
    tax_rule_id = models.ForeignKey(TaxRule, related_name='sections', on_delete=models.PROTECT,verbose_name=_('Tax Rule Id'))
    salary_from = models.FloatField(verbose_name=_('Salary From'))
    salary_to = models.FloatField(default=1000000,verbose_name=_('Salary To'))
    tax_percentage = models.FloatField(verbose_name=_('Tax Percentage'))
    tax_discount_percentage = models.FloatField(verbose_name=_('Tax Discount Percentage'))
    section_execution_sequence = models.IntegerField(default=0,verbose_name=_('Section Execution Sequence'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date') )
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by =    models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,on_delete=models.CASCADE,related_name="TaxSection_created_by")
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,on_delete=models.CASCADE,related_name="TaxSection_last_update_by")
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class Tax_Sections(models.Model):
    name = models.CharField(max_length=255,verbose_name=_('Section Name'))
    tax_rule_id = models.ForeignKey(TaxRule, related_name='tax_sections', on_delete=models.PROTECT,verbose_name=_('Tax Rule Id'))
    salary_from = models.FloatField(verbose_name=_('Salary From'))
    salary_to = models.FloatField(default=1000000000,verbose_name=_('Salary To'))
    tax_percentage = models.FloatField(verbose_name=_('Tax Percentage'))
    tax_difference = models.FloatField(blank=True, null=True, verbose_name=_('Tax Difference'))
    section_execution_sequence = models.IntegerField(default=0,verbose_name=_('Section Execution Sequence'))
    start_date	=	models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date') )
    end_date	=	models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by  =   models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,on_delete=models.CASCADE,related_name="TaxSections_created_by")
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,on_delete=models.CASCADE,related_name="TaxSections_last_update_by")
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Tax_Sections)
def tax_difference_calc(sender, instance, *args, **kwargs):
    instance.tax_difference = instance.salary_to - instance.salary_from+1
