from django import forms
from crispy_forms.helper import FormHelper
from task_management.models import Project, Project_Task



class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

    class Meta():
        model = Project
        fields = '__all__'
        exclude = ['created_by','creation_date','last_update_by','last_update_date']


class ProjectTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

    class Meta():
        model = Project_Task
        fields = '__all__'
        exclude = ['created_by','creation_date','last_update_by','last_update_date']

Project_Tasks_ModelFormset = forms.modelformset_factory(Project_Task, form=ProjectTaskForm, extra=3, can_delete=False)
