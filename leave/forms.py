from django import forms
from crispy_forms.helper import FormHelper
from django.forms import ValidationError
from django.core import validators
from leave.models import Leave, LeaveMaster


class FormLeave(forms.ModelForm):
    class Meta():
        model = Leave
        fields = ('startdate', 'enddate', 'resume_date', 'leavetype',  'reason', 'attachment')
        exclude = ['created_by', 'creation_date', 'last_update_by', 'last_update_date']
        widgets = {
                 'startdate' : forms.DateInput(attrs={'class': 'form-control',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'enddate' : forms.DateInput(attrs={'class': 'form-control',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'resume_date' : forms.DateInput(attrs={'class': 'form-control',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'leavetype' : forms.Select(attrs={'class': 'form-control'}),
                 'reason' : forms.Textarea(attrs={
                                                   'rows': 2,'cols': 40,
                                                   'style': 'height: 8em;',
                                                   'class': 'form-control'}),

        }
    def __init__(self, *args, **kwargs):
        super(FormLeave, self).__init__(*args, **kwargs)
        # self.fields['startdate'].widget.input_type = 'date'
        # self.fields['enddate'].widget.input_type = 'date'
        self.helper = FormHelper()
        self.helper.form_show_labels = True


class FormLeaveMaster(forms.ModelForm):
    class Meta():
        model = LeaveMaster
        exclude = ['created_by', 'creation_date', 'last_update_by', 'last_update_date']
