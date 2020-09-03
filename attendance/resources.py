from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields
from employee.models import Employee
from attendance.models import Attendance, Attendance_Interface


class AttendanceResource(resources.ModelResource):
    # this class describes how the model will be imported
    class Meta:
        model = Attendance_Interface
        fields = ('id', 'employee', 'date', 'check_in', 'check_out')  # defines which model fields will be imported
        # id is required here to save attendance object

    # employee = fields.Field(
    #     column_name='employee_id',  # this is the name of imported column
    #     attribute='employee',  # this is the name of the model attribute it represents
    #     widget=ForeignKeyWidget(Employee, 'pk'))  # specify which field of the fk this column refer to

    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']
