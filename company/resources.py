from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Department ,Enterprise , Job , Grade, Position
from mptt.models import MPTTModel, TreeForeignKey
from custom_user.models import User
from cities_light.models import City, Country

class EnterpriseResource(resources.ModelResource): 
    class Meta:
        model = Enterprise
        skip_unchanged = True
        report_skipped = True


    enterprise_user = fields.Field(
        column_name='enterprise_user',  # this is the name of imported column
        attribute='enterprise_user ',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(User, 'pk'))  # specify which field of the fk this column refer to


    country = fields.Field(
        column_name='country',  # this is the name of imported column
        attribute='country ',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Country, 'pk'))  # specify which field of the fk this column refer to


    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']

class DepartmentResource(resources.ModelResource): 
    class Meta:
        model = Department
        skip_unchanged = True
        report_skipped = True


    enterprise = fields.Field(
        column_name='enterprise',  # this is the name of imported column
        attribute='enterprise',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Enterprise, 'pk'))  # specify which field of the fk this column refer to


    parent = fields.Field(
        column_name='parent',  # this is the name of imported column
        attribute='parent',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Department, 'pk'))  # specify which field of the fk this column refer to
        

    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']

class JobResource(resources.ModelResource): 
    class Meta:
        model = Job
        skip_unchanged = True
        report_skipped = True


    enterprise = fields.Field(
        column_name='enterprise',  # this is the name of imported column
        attribute='enterprise',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Enterprise, 'pk'))  # specify which field of the fk this column refer to


    job_user = fields.Field(
        column_name='job_user',  # this is the name of imported column
        attribute='job_user',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(User, 'pk'))  # specify which field of the fk this column refer to
        
    

    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']


       
class GradeResource(resources.ModelResource): 
    class Meta:
        model = Grade
        skip_unchanged = True
        report_skipped = True


    enterprise = fields.Field(
        column_name='enterprise',  # this is the name of imported column
        attribute='enterprise ',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Enterprise, 'pk'))  # specify which field of the fk this column refer to


    grade_user = fields.Field(
        column_name='grade_user',  # this is the name of imported column
        attribute='grade_user',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(User, 'pk'))  # specify which field of the fk this column refer to
        

    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']



class PositionResource(resources.ModelResource): 
    class Meta:
        model = Position
        skip_unchanged = True
        report_skipped = True

    job = fields.Field(
        column_name='job',  # this is the name of imported column
        attribute=' job',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Job, 'pk'))  # specify which field of the fk this column refer to


    department = fields.Field(
        column_name='department',  # this is the name of imported column
        attribute='department',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Department, 'pk'))  # specify which field of the fk this column refer to
        

    grade = fields.Field(
        column_name='grade',  # this is the name of imported column
        attribute='grade',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Grade, 'pk'))  # specify which field of the fk this column refer to
            

    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']


      