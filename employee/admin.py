from django.contrib import admin
from employee.models import Employee, Medical, JobRoll,Payment, Employee_Element

class JobRollInlineAdmin(admin.TabularInline):
    fields = (
        'emp_id',
        'manager',
        'position',
        'contract_type',
        'payroll',
        'start_date',
        'end_date',
    )
    model = JobRoll
    fk_name = 'emp_id'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields =(
        'user',
        'enterprise',
        'emp_number',
        'emp_name',
        'date_of_birth',
        'hiredate',
        'email',
        'picture',
        'is_active',
        'place_of_birth',
        'gender',
        'social_status',
        'military_status',
        'religion',
        'identification_type',
        'id_number',
        'nationality',
        'field_of_study',
        'education_degree',
        'insured',
        'insurance_number',
        'insurance_date',
        'has_medical',
        'medical_number',
        'medical_date',
        'start_date',
        'end_date',
    )
    inlines =[
        JobRollInlineAdmin
    ]
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.created_by = request.user
            instance.last_update_by = request.user
            instance.save()
        formset.save_m2m()
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save()
        return instance

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = (
          'emp_id',
          'payment_method',
          'account_number',
          'percentage',
          'bank_name',
          'swift_code',
          'start_date',
          'end_date',
    )
    list_display = ('emp_id','payment_method', 'percentage',)

@admin.register(Employee_Element)
class EmployeeElementAdmin(admin.ModelAdmin):
    fields = (
        'emp_id',
        'element_id',
        'element_value' ,
        'start_date',
        'end_date'
    )
    list_display = ('emp_id','element_id', 'element_value',)
