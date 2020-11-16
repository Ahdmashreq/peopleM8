from django import forms
from crispy_forms.helper import FormHelper
from company.models import (Enterprise, Department, Grade, Job,
                            Position, Working_Days_Policy, Working_Hours_Deductions_Policy, YearlyHoliday, Year)
from defenition.models import LookupDet
from cities_light.models import City, Country
from datetime import date
from django.db.models import Q

common_items_to_execlude = (
    'enterprise_user',
    'created_by', 'creation_date',
    'last_update_by', 'last_update_date',
    'attribute1', 'attribute2', 'attribute3',
    'attribute4', 'attribute5', 'attribute6',
    'attribute7', 'attribute8', 'attribute9',
    'attribute10', 'attribute11', 'attribute12',
    'attribute13', 'attribute14', 'attribute15',
)


#######################################Company Information#################################################################
class EnterpriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(EnterpriseForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.fields['email'].widget.input_type = 'email'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True


########################################Department forms ###################################################################
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('dept_name', 'parent', 'start_date', 'end_date',)
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False


DepartmentInline = forms.modelformset_factory(Department, form=DepartmentForm, extra=3, can_delete=False)


########################################Job forms ###################################################################
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('job_name', 'job_description', 'start_date', 'end_date',)
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False


JobInline = forms.modelformset_factory(Job, form=JobForm, extra=5, can_delete=False)


########################################Grade forms ###################################################################
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('grade_name', 'grade_description', 'start_date', 'end_date',)
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'


GradeInline = forms.modelformset_factory(Grade, form=GradeForm, extra=5, can_delete=False)


########################################Position forms ###################################################################
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('job', 'department', 'grade', 'position_name', 'position_description', 'start_date', 'end_date',)
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False


PositionInline = forms.modelformset_factory(Position, form=PositionForm, extra=5, can_delete=True)


class WorkingDaysForm(forms.ModelForm):
    class Meta:
        model = Working_Days_Policy
        fields = '__all__'
        exclude = common_items_to_execlude+('enterprise',)

    def __init__(self, *args, **kwargs):
        super(WorkingDaysForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.fields['hrs_start_from'].widget.input_type = 'time'
        self.fields['hrs_end_at'].widget.input_type = 'time'
        self.fields['delay_allowed'].widget.input_type = 'time'
        self.fields['delay_starts_from'].widget.input_type = 'time'
        self.fields['absence_starts_from'].widget.input_type = 'time'
        for field in self.fields:
            if self.fields[field].widget.input_type != 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class WorkingHoursDeductionForm(forms.ModelForm):
    class Meta:
        model = Working_Hours_Deductions_Policy
        fields = ('__all__')
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(WorkingHoursDeductionForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

Working_Hours_Deduction_Form_Inline = forms.modelformset_factory(Working_Hours_Deductions_Policy, form=WorkingHoursDeductionForm, extra=1, can_delete=False)


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = '__all__'
        exclude = common_items_to_execlude+('enterprise',)

    def __init__(self, *args, **kwargs):
        super(YearForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class YearlyHolidayForm(forms.ModelForm):
    class Meta:
        model = YearlyHoliday
        fields = (
            'year',
            'name',
            'start_date',
            'end_date',
            # 'number_of_days_off',
        )
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(YearlyHolidayForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.fields['year'].widget= forms.HiddenInput()
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

YearlyHolidayInline = forms.modelformset_factory(YearlyHoliday, form=YearlyHolidayForm, extra=1, can_delete=False)
# YearlyHolidayInline = forms.inlineformset_factory(Year, YearlyHoliday, form=YearlyHolidayForm, extra=5, can_delete=False)
