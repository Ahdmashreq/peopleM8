from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Employee


class EmployeeResource(resources.ModelResource): 
    class Meta:
        model = Employee
        skip_unchanged = True
        report_skipped = True
        