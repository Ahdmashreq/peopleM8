from django import forms
from crispy_forms.helper import FormHelper
from django.forms import ValidationError
from django.core import validators
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
    class Meta():
        model = LeaveMaster
        exclude = ['created_by', 'creation_date', 'last_update_by', 'last_update_date']


class Leave_Balance_Form(forms.ModelForm):
    class Meta():
        model = Employee_Leave_balance
        exclude = ['created_by', 'creation_date', 'last_update_by', 'last_update_date']

    def __init__(self, *args, **kwargs):
        super(Leave_Balance_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['employee'].widget.attrs['class']   = 'form-control parsley-validated'
        self.fields['casual'].widget.attrs['class']   = 'form-control parsley-validated'
        self.fields['usual'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['carried_forward'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['absence'].widget.attrs['class']   = 'form-control parsley-validated'
