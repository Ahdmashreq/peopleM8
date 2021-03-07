from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from custom_user.models import User
from company.models import Enterprise



class UserResource(resources.ModelResource): 
    class Meta:
        model = User

    company = fields.Field(
        column_name='company',
        attribute='company',
        widget=ForeignKeyWidget(Enterprise, 'pk'))