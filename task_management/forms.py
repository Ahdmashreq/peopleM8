from django import forms
from crispy_forms.helper import FormHelper
from task_management.models import Project, Project_Task



class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields['start_date'].widget.input_type = 'date'
            self.fields['end_date'].widget.input_type = 'date'
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

    class Meta():
        model = Project
        fields = '__all__'
        exclude = ['created_by','creation_date','last_update_by','last_update_date', 'company']


class ProjectTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['task_start_date'].widget.input_type = 'date'
        self.fields['task_end_date'].widget.input_type = 'date'
        self.fields['parent_task'].queryset = Project_Task.objects.none()
        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['parent_task'].queryset = Project_Task.objects.filter(project=project_id)
            except Exception as e:
                print('Error occurred in project task form -> ', e)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

    class Meta():
        model = Project_Task
        fields = '__all__'
        widgets = {
                   'description': forms.Textarea(attrs={
                       'rows': 8, 'cols': 80,
                       'style': 'height: 8em;',
                       'class': 'form-control',
                   }),
                'comments': forms.Textarea(attrs={
                    'rows': 8, 'cols': 80,
                    'style': 'height: 8em;',
                    'class': 'form-control',
                }),
        }
        exclude = ['created_by','creation_date','last_update_by','last_update_date']

Project_Tasks_ModelFormset = forms.modelformset_factory(Project_Task, form=ProjectTaskForm, extra=10, can_delete=False)
