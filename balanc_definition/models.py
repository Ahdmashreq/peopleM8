from django.conf import settings
from django.db import models
from datetime import date
from company.models import Department, Job, Grade, Position
from django.utils.translation import ugettext_lazy as _


level_name_choises=[('D',_('Department')),('J',_('Jobs')),('G',_('Grade')),('P',_('Position'))]

class Cost_Level(models.Model):
    level_name =        models.CharField(max_length=50, choices=level_name_choises,verbose_name=_('Level Name'))
    start_date	=	    models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	    models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by =        models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE,related_name="cost_level_created_by")
    creation_date	=	models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE,related_name="cost_level_last_update_by")
    last_update_date=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.level_name


class Cost_Detail(models.Model):
    level_Department	=	models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True,verbose_name=_('Department'))
    level_Job	=	        models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True,verbose_name=_('Job'))
    level_Grade	=       	models.ForeignKey(Grade, on_delete=models.CASCADE, blank=True, null=True,verbose_name=_('Grade'))
    level_Position	=	    models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True,verbose_name=_('Position'))
    name	=	            models.ForeignKey(Cost_Level, blank=False,on_delete=models.CASCADE,verbose_name=_('Name'))
    debit_account =         models.CharField(blank=True, null=True,max_length=50,verbose_name=_('Debit Account'))
    credit_account =        models.CharField(blank=True, null=True,max_length=50,verbose_name=_('Credit Account'))
    start_date	=	        models.DateField(auto_now=False, auto_now_add=False, default=date.today,verbose_name=_('Start Date'))
    end_date	=	        models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,verbose_name=_('End Date'))
    created_by =            models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE,related_name="cost_detail_created_by")
    creation_date	=	    models.DateField(auto_now=True, auto_now_add=False)
    last_update_by	=	    models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,on_delete=models.CASCADE,related_name="cost_detail_last_update_by")
    last_update_date	=	models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        if self.level_Department is not None:
            return self.level_Department.dept_name
        elif self.level_Job is not  None:
            return self.level_Job.job_name
        elif self.level_Grade is not  None:
            return self.level_Grade.grade_name
        elif self.level_Position is not  None:
            return self.level_Position.position_name
        raise AssertionError("Neither 'level_Department' ,'level_Job', 'level_Grade' nor 'level_Position' is set")
