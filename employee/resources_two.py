from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Employee , JobRoll
from company.models import Position

from company.models import Enterprise
from custom_user.models import User
from manage_payroll.models import (Bank_Master, Payroll_Master)
from defenition.models import LookupType, LookupDet



class EmployeeResource(resources.ModelResource): 
    class Meta:
        model = Employee
        exclude = ('id','is_active','last_update_date', 'last_update_by' ,'creation_date', 'created_by')

    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username'))

    enterprise = fields.Field(
        column_name='enterprise',
        attribute='enterprise',
        widget=ForeignKeyWidget(Enterprise, 'name'))  

    