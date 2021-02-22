from django import forms
from crispy_forms.helper import FormHelper
from django.db.models import Q
from company.models import Department, Job, Grade, Position
from manage_payroll.models import Payroll_Master
from employee.models import Employee, JobRoll, Payment, Employee_Element, EmployeeStructureLink, Employee_File
from defenition.models import LookupType, LookupDet
from element_definition.models import Element_Master, Element_Link, SalaryStructure
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import date
from django.forms import BaseInlineFormSet

common_items_to_execlude = (
    'enterprise',
    'created_by', 'creation_date',
    'last_update_by', 'last_update_date',
    'attribute1', 'attribute2', 'attribute3',
    'attribute4', 'attribute5', 'attribute6',
    'attribute7', 'attribute8', 'attribute9',
    'attribute10', 'attribute11', 'attribute12',
    'attribute13', 'attribute14', 'attribute15',
)


###############################################################################

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'insured': forms.CheckboxInput(attrs={
                'style': 'padding: 25px; margin:25px;'
            }),
            'has_medical': forms.CheckboxInput(attrs={
                'style': 'padding: 25px; margin:25px;'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'style': 'padding: 25px; margin:25px;'
            }),
        }
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.input_type = 'date'
        self.fields['hiredate'].widget.input_type = 'date'
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.fields['insurance_date'].widget.input_type = 'date'
        self.fields['medical_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True


class JobRollForm(forms.ModelForm):
    class Meta:
        model = JobRoll
        fields = '__all__'
        exclude = common_items_to_execlude
       
    def __init__(self, user_v, *args, **kwargs):
        super(JobRollForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['contract_type'].queryset = LookupDet.objects.filter(
            lookup_type_fk__lookup_type_name='EMPLOYEE_TYPE',lookup_type_fk__enterprise=user_v.company)
        self.fields['position'].queryset = Position.objects.filter((Q(department__enterprise=user_v.company)), (
                Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        self.fields['payroll'].queryset = Payroll_Master.objects.filter((Q(enterprise=user_v.company)), (
                Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        self.fields['manager'].queryset = Employee.objects.filter(enterprise=user_v.company)
        #self.fields['manager'].widget.attrs['onchange'] = 'one_Function(this)'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True


# class PaymentTotalCheckFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         total_percentage = sum(f.cleaned_data['percentage'] for f in self.forms)
#         if total_percentage != 100:
#             raise forms.ValidationError("Total percentage must be 100")

Employee_Payment_formset = forms.inlineformset_factory(Employee, Payment, form=PaymentForm, can_delete=False)


class EmployeeElementForm(forms.ModelForm):
    class Meta:
        model = Employee_Element
        fields = "__all__"
        exclude = ('emp_id',) + common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(EmployeeElementForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True


Employee_Element_Inline = forms.inlineformset_factory(Employee, Employee_Element, form=EmployeeElementForm,
                                                      can_delete=False, extra=8)


class EmployeeStructureLinkForm(forms.ModelForm):
    class Meta:
        model = EmployeeStructureLink
        fields = "__all__"
        exclude = common_items_to_execlude + ('employee',)

    def __init__(self, *args, **kwargs):
        super(EmployeeStructureLinkForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.fields['salary_structure'].queryset = SalaryStructure.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gt=date.today()))

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True

class EmployeeFileForm(forms.ModelForm):
    class Meta:
        model = Employee_File
        fields = "__all__"
        exclude = common_items_to_execlude + ('emp_id',)
    
    # def __init__(self , *args, *kwargs):
    #     self.fields['']