from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields
from django.contrib.auth.models import Group
from .forms import GroupForm, GroupViewForm

class GroupResource(resources.ModelResource):
    # this class describes how the model will be imported
    class Meta:
        model = Group
