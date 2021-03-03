from datetime import date

from django import forms
from django.forms import ValidationError
from django.core import validators
from django.db.models import Q

from crispy_forms.helper import FormHelper

from employee.models import Employee
from leave.models import Leave, LeaveMaster, Employee_Leave_balance


class FormLeave(forms.ModelForm):
    class Meta():
        model = Leave
        fields = ('startdate', 'enddate', 'resume_date', 'leavetype', 'reason', 'attachment')
        exclude = ['created_by', 'creation_date', 'last_update_by', 'last_update_date']
        widgets = {
            'startdate': forms.DateInput(attrs={'class': 'form-control',
                                                'data-provide': "datepicker",
                                                'wtx-context': "2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
            'enddate': forms.DateInput(attrs={'class': 'form-control',
                                              'data-provide': "datepicker",
                                              'wtx-context': "2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
            'resume_date': forms.DateInput(attrs={'class': 'form-control',
                                                  'data-provide': "datepicker",
                                                  'wtx-context': "2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
            'leavetype': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={
                'rows': 2, 'cols': 40,
                'style': 'height: 8em;',
                'class': 'form-control'}),

        }

    def __init__(self, form_type, *args, **kwargs):
        super(FormLeave, self).__init__(*args, **kwargs)
        if form_type == 'respond':
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = 'True'
        self.helper = FormHelper()
        self.helper.form_show_labels = True

    def clean(self):
        cleaned_data = super(FormLeave, self).clean()
        if cleaned_data['enddate'] < cleaned_data['startdate']:
            self.add_error('enddate', 'End date must be after start date')
        elif cleaned_data['resume_date'] < cleaned_data['enddate'] or cleaned_data['resume_date'] < cleaned_data[
            'startdate']:
            self.add_error('resume_date', 'Resume date must be equal or after the end date')
        return cleaned_data


class FormLeaveMaster(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormLeaveMaster, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

    class Meta():
        model = LeaveMaster
        exclude = ['enterprise', 'created_by', 'creation_date', 'last_update_by', 'last_update_date']


class Leave_Balance_Form(forms.ModelForm):
    def __init__(self, user_v, *args, **kwargs):
        super(Leave_Balance_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['employee'].queryset = Employee.objects.filter((Q(enterprise=user_v.company)), (
                    Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

    class Meta():
        model = Employee_Leave_balance
        exclude = ['absence', 'created_by', 'creation_date', 'last_update_by', 'last_update_date']
