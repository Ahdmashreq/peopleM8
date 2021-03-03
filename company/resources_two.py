from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Department ,Enterprise , Job , Grade, Position
from mptt.models import MPTTModel, TreeForeignKey
from custom_user.models import User
from cities_light.models import City, Country


class DepartmentResource(resources.ModelResource): 
    class Meta:
        model = Department
        skip_unchanged = True
        report_skipped = True
        fields = ('enterprise', 'department_user' , 'dept_name' , 'parent' , 'start_date' , 'end_date')



    enterprise = fields.Field(
        column_name='enterprise',  # this is the name of imported column
        attribute='enterprise',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Enterprise, 'name'))  # specify which field of the fk this column refer to

    department_user = fields.Field(
        column_name='department_user',  # this is the name of imported column
        attribute='department_user',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(User, 'username'))  # specify which field of the fk this column refer to
        

    parent = fields.Field(
        column_name='parent',  # this is the name of imported column
        attribute='parent',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Department, 'dept_name'))  # specify which field of the fk this column refer to
        

class JobResource(resources.ModelResource): 
    class Meta:
        model = Job
        skip_unchanged = True
        report_skipped = True
        fields = ('enterprise', 'job_user' , 'job_name' , 'job_description' , 'start_date' , 'end_date')


    enterprise = fields.Field(
        column_name='enterprise',  # this is the name of imported column
        attribute='enterprise',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Enterprise, 'name'))  # specify which field of the fk this column refer to


    job_user = fields.Field(
        column_name='job_user',  # this is the name of imported column
        attribute='job_user',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(User, 'username'))  # specify which field of the fk this column refer to
        
class GradeResource(resources.ModelResource): 
    class Meta:
        model = Grade
        skip_unchanged = True
        report_skipped = True
        fields = ('enterprise', 'grade_user' , 'grade_name' , 'grade_description' , 'start_date' , 'end_date')

    enterprise = fields.Field(
        column_name='enterprise',  # this is the name of imported column
        attribute='enterprise',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Enterprise, 'name'))  # specify which field of the fk this column refer to


    grade_user = fields.Field(
        column_name='grade_user',  # this is the name of imported column
        attribute='grade_user',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(User, 'username'))  # specify which field of the fk this column refer to
        
class PositionResource(resources.ModelResource): 
    class Meta:
        model = Position
        skip_unchanged = True
        report_skipped = True
        fields = ('job', 'department' , 'grade' , 'position_name' , 'position_description' ,'start_date', 'end_date')


    job = fields.Field(
        column_name='job',  # this is the name of imported column
        attribute='job',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Job, 'job_name'))  # specify which field of the fk this column refer to
        

    department = fields.Field(
        column_name='department',  # this is the name of imported column
        attribute='department',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Department, 'dept_name'))  # specify which field of the fk this column refer to
        

    grade = fields.Field(
        column_name='grade',  # this is the name of imported column
        attribute='grade',  # this is the name of the model attribute it represents
        widget=ForeignKeyWidget(Grade, 'grade_name'))  # specify which field of the fk this column refer to