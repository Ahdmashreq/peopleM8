from django import forms
from attendance.models import Attendance, Task

class FormAttendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['created_by','creation_date','last_update_by','last_update_date','employee']

    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type')
        super(FormAttendance, self).__init__(*args, **kwargs)
        if form_type=='check_out':
            self.fields['check_in'].widget.attrs['disabled'] = True

class FormTasks(forms.ModelForm):
    class Meta():
        model = Task
        fields = '__all__'
        exclude = ['created_by','creation_date','last_update_by','last_update_date','user','attendance','slug']
        widgets = {
                 'start_time' : forms.TextInput(attrs={'class': 'form-control tm', 'type':'text'}),
                 'end_time' : forms.TextInput(attrs={'class': 'form-control tm', 'type':'text'}),
                 'task' : forms.TextInput(attrs={'class': 'form-control'}),

        }


Tasks_inline_formset = forms.inlineformset_factory(Attendance, Task,form=FormTasks, extra=3, can_delete=True)
