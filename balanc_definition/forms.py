from django import forms
from crispy_forms.helper import FormHelper
from balanc_definition.models import Cost_Level, Cost_Detail, Cost_Center, Cost_Center_Link
from company.models import Department, Job, Grade, Position
from datetime import date
from django.db.models import Q

common_items_to_execlude = (
    'created_by', 'creation_date',
    'last_update_by',  'last_update_date','enterprise',
    'attribute1',    'attribute2',    'attribute3',
    'attribute4',    'attribute5',    'attribute6',
    'attribute7',    'attribute8',    'attribute9',
    'attribute10',    'attribute11',    'attribute12',
    'attribute13',    'attribute14',    'attribute15',
)

class CostLevelForm(forms.ModelForm):
    class Meta:
        model = Cost_Level
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(CostLevelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True


class CostDetailForm(forms.ModelForm):
    class Meta:
        model = Cost_Detail
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(CostDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['level_Department'].queryset = Department.objects.filter(parent_dept__isnull=False).filter(Q(end_date__gte=today)|Q(end_date__isnull=True))
        self.fields['level_Job'].queryset = Job.objects.filter((Q(end_date__gte=today)|Q(end_date__isnull=True)))
        self.fields['level_Grade'].queryset = Grade.objects.filter((Q(end_date__gte=today)|Q(end_date__isnull=True)))
        self.fields['level_Position'].queryset = Position.objects.filter((Q(end_date__gte=today)|Q(end_date__isnull=True)))

Cost_detail_inline_form = forms.inlineformset_factory(Cost_Level,
                                                      Cost_Detail,
                                                      form= CostDetailForm,
                                                      extra=5, can_delete=False)



class Cost_Center_Form(forms.ModelForm):
    class Meta:
        model = Cost_Center
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Cost_Center_Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True


class Cost_Center_Link_Form(forms.ModelForm):
    class Meta:
        model = Cost_Center_Link
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Cost_Center_Link_Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True

Cost_Center_inline_form = forms.inlineformset_factory(Cost_Center,
                                                      Cost_Center_Link,
                                                      form= Cost_Center_Link_Form,
                                                      extra=3, can_delete=False)
