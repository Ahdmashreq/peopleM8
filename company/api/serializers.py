from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from company.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    # children = serializers.PrimaryKeyRelatedField(read_only=True,source='sub_category')
    parent = serializers.PrimaryKeyRelatedField(queryset=Department.objects.filter(end_date__isnull=True))

    class Meta:
        model = Department
        fields = ['id', 'dept_name', 'enterprise', 'department_user', 'parent', 'start_date', 'end_date']
        read_only_fields = ('id',)
