from django import forms
from crispy_forms.helper import FormHelper
from defenition.models import LookupType, LookupDet, InsuranceRule, TaxRule, TaxSection, Tax_Sections
from datetime import date
from django.db.models import Q

common_items_to_execlude = (
                            'enterprise','created_by', 'creation_date',
                            'last_update_by',  'last_update_date',
                            'attribute1',    'attribute2',    'attribute3',
                            'attribute4',    'attribute5',    'attribute6',
                            'attribute7',    'attribute8',    'attribute9',
                            'attribute10',    'attribute11',    'attribute12',
                            'attribute13',    'attribute14',    'attribute15',
)

class LookupTypeForm(forms.ModelForm):
    class Meta:
        model = LookupType
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(LookupTypeForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'


class LookupDetForm(forms.ModelForm):
    class Meta:
        model = LookupDet
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(LookupDetForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

LookupDetinlineFormSet = forms.inlineformset_factory(LookupType,
                                                     LookupDet,
                                                     form=LookupDetForm,
                                                     extra=5,
                                                     can_delete=False)

class InsuranceRuleForm(forms.ModelForm):
    class Meta:
        model = InsuranceRule
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(InsuranceRuleForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

class TaxRuleForm(forms.ModelForm):
    class Meta:
        model = TaxRule
        fields = '__all__'
        widgets = {
            'round_down_to_nearest_10': forms.CheckboxInput(attrs={
                                                     'style': 'padding: 25px; margin:25px;'
            }),
        }
        exclude = common_items_to_execlude , 'start_date'

    def __init__(self, *args, **kwargs):
        super(TaxRuleForm, self).__init__(*args, **kwargs)
        # self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

class TaxSectionForm(forms.ModelForm):
    class Meta:
        model = Tax_Sections
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(TaxSectionForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = ''
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

TaxSectionFormSet = forms.inlineformset_factory(TaxRule, Tax_Sections, form= TaxSectionForm, extra=2, can_delete=False)
