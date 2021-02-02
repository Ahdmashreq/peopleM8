from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Department, Enterprise
from mptt.models import MPTTModel, TreeForeignKey
from custom_user.models import User
from django.contrib.auth import authenticate


class DepartmentForeignKeyWidget(ForeignKeyWidget):

    def __init__(self, user,  model, field='pk', *args, **kwargs):
        self.user = user
        self.model = model
        self.field = field
        super().__init__(model, *args, **kwargs)

    def get_queryset(self, value, row):
        user = User.objects.get(id=1)
        return self.model.objects.all(user)


class DepartmentResource(resources.ModelResource):
    user = None
    def __init__(self,user,  *args, **kwargs):
        self.user = user
        print (user)
        self.request = kwargs.pop('request', None)
        super(DepartmentResource, self).__init__(*args, **kwargs)

    class Meta:
        model = Department
        fields = ('id', 'enterprise', 'department_user', 'dept_name',
                  'parent', 'objects', 'start_date', 'end_date')  # defines which model fields will be imported
        # id is required here to save attendance object

    #def get_user(self):
      #  user = self.user
      #  return user



    enterprise = fields.Field(
        column_name='enterprise_id',  # this is the name of imported column
        # this is the name of the model attribute it represents
        attribute='enterprise',
        widget=ForeignKeyWidget(Enterprise, 'pk'))  # specify which field of the fk this column refer to
    
    parent = fields.Field(
        column_name='parent_id',  # this is the name of imported column
        attribute='parent',  # this is the name of the model attribute it represents
        widget=DepartmentForeignKeyWidget(Department, 'pk'))  # specify which field of the fk this column refer to

    def after_import_instance(self, instance, new, **kwargs):
        if new or not instance.created_by:
            instance.created_by = kwargs['user']
        instance.last_update_by = kwargs['user']


   

    def get_queryset(self):
        user = User.objects.get(id=1)
        return self._meta.model.objects.all(user)
    
