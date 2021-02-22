from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Department ,Enterprise, Position, Job
from mptt.models import MPTTModel, TreeForeignKey




class DepartmentResource(resources.ModelResource): 
    class Meta:
        model = Department
        skip_unchanged = True
        report_skipped = True
        fields = ('id' ,'enterprise', 'department_user', 'dept_name',
         'parent', 'objects','start_date','end_date' )  # defines which model fields will be imported
        # id is required here to save attendance object
       


    enterprise = fields.Field(
        column_name='enterprise_id',  # this is the name of imported column
        attribute='enterprise owner',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Enterprise, 'pk'))  # specify which field of the fk this column refer to


    parent = fields.Field(
        column_name='parent_id',  # this is the name of imported column
        attribute='parent',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Department, 'pk'))  # specify which field of the fk this column refer to
        
    


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
        attribute='job',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Job, 'pk'))  # specify which field of the fk this column refer to


    department = fields.Field(
        column_name='department',  # this is the name of imported column
        attribute='department',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Department, 'pk'))  # specify which field of the fk this column refer to
            
        