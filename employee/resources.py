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

    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'pk'))

    enterprise = fields.Field(
        column_name='enterprise',
        attribute='enterprise',
        widget=ForeignKeyWidget(Enterprise, 'pk'))  

    
    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']





class JobRollResource(resources.ModelResource): 
    class Meta:
        model = JobRoll

    emp_id = fields.Field(
        column_name='emp_id',
        attribute='emp_id',
        widget=ForeignKeyWidget(Employee, 'pk'))

    manager = fields.Field(
        column_name='manager',
        attribute='manager',
        widget=ForeignKeyWidget(Employee, 'pk'))  

    position = fields.Field(
        column_name='position',
        attribute='position',
        widget=ForeignKeyWidget(Position, 'pk'))  
    


    contract_type = fields.Field(
        column_name='contract_type',
        attribute='contract_type',
        widget=ForeignKeyWidget(LookupDet, 'pk'))  
    

    payroll = fields.Field(
        column_name='payroll',
        attribute='payroll',
        widget=ForeignKeyWidget(Payroll_Master, 'pk'))  
    
    
    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']
