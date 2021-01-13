import os
from crispy_forms.helper import FormHelper
from django import forms
from attendance.models import Attendance, Task, Employee_Attendance_History


class FormAttendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['absence_days','delay_hrs', 'day_of_week', 'status', 'work_hours', 'normal_hrs', 'normal_overtime_hours',
                   'exceptional_hrs', 'exceptional_overtime', 'slug', 'created_by', 'creation_date', 'last_update_by',
                   'last_update_date', 'employee']

    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type')
        super(FormAttendance, self).__init__(*args, **kwargs)
        if form_type == 'check_out':
            self.fields['check_in'].widget.attrs['disabled'] = True
        self.fields['date'].widget.input_type = 'date'
        self.fields['check_in'].widget.input_type = 'time'
        self.fields['check_out'].widget.input_type = 'time'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
            self.helper = FormHelper()
            self.helper.form_show_labels = False


class FormTasks(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormTasks, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
            self.helper = FormHelper()
            self.helper.form_show_labels = False
    class Meta():
        model = Task
        fields = '__all__'
        exclude = ['created_by', 'creation_date', 'last_update_by', 'last_update_date', 'user', 'attendance', 'slug']
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'form-control tm', 'type': 'time', }),
            'end_time': forms.TimeInput(attrs={'class': 'form-control tm', 'type': 'time', }),
            # 'task': forms.TextInput(attrs={'class': 'form-control'}),

        }


Tasks_inline_formset = forms.inlineformset_factory(Attendance, Task, form=FormTasks, extra=3, can_delete=True)


class FormEmployeeAttendanceHistory(forms.ModelForm):
    class Meta():
        model = Employee_Attendance_History
        fields = ('month', 'year')
        exclude = ['created_by', 'creation_date',
                   'last_update_by', 'last_update_date',
                   'employee', 'attendance_days', 'leave_days',
                   'absence_days', 'slug']


class ConfirmImportForm(forms.Form):
    import_file_name = forms.CharField(widget=forms.HiddenInput())
    original_file_name = forms.CharField(widget=forms.HiddenInput())

    def clean_import_file_name(self):
        data = self.cleaned_data['import_file_name']
        data = os.path.basename(data)
        return data
