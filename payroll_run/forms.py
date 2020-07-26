from django import forms
from datetime import date
from crispy_forms.helper import FormHelper
from payroll_run.models import Salary_elements
from defenition.models import LookupDet
from employee.models import Employee, Employee_Element

common_items_to_execlude = (
    'created_by', 'creation_date',
    'last_update_by',  'last_update_date',
    'start_date', 'end_date',
    'attribute1',    'attribute2',    'attribute3',
    'attribute4',    'attribute5',    'attribute6',
    'attribute7',    'attribute8',    'attribute9',
    'attribute10',    'attribute11',    'attribute12',
    'attribute13',    'attribute14',    'attribute15',
)

class SalaryElementForm(forms.ModelForm):
    class Meta:
        model = Salary_elements
        fields = '__all__'
        exclude = common_items_to_execlude
        widgets = {
            'tax_amount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'insurance_amount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'gross_salary': forms.TextInput(attrs={'readonly': 'readonly'}),
            'net_salary': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(SalaryElementForm, self).__init__(*args, **kwargs)
        # self.fields['start_date'].widget.input_type = 'date'
        # self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        # self.fields['salary_month'].queryset = LookupDet.objects.filter(lookup_type_fk__lookup_type_name='SALARY_MONTH')


Salary_Element_Inline = forms.modelformset_factory(
    Salary_elements, form=SalaryElementForm)

################################################################################
