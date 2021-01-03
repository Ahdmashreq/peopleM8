from django import forms
from django.db.models import Q
from django.core.exceptions import NON_FIELD_ERRORS
from crispy_forms.helper import FormHelper
from datetime import date
from element_definition.models import (Element_Master,
                                       Element_Batch, Element_Batch_Master, Element_Link, Custom_Python_Rule, Element,
                                       SalaryStructure, StructureElementLink)
from company.models import Department, Job, Grade, Position
from manage_payroll.models import Payroll_Master
from defenition.models import LookupType, LookupDet
from django.utils.translation import ugettext_lazy as _

common_items_to_execlude = ('id',
                            'enterprise',
                            'created_by', 'creation_date',
                            'last_update_by', 'last_update_date',
                            'attribute1', 'attribute2', 'attribute3',
                            'attribute4', 'attribute5', 'attribute6',
                            'attribute7', 'attribute8', 'attribute9',
                            'attribute10', 'attribute11', 'attribute12',
                            'attribute13', 'attribute14', 'attribute15',
                            )


class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(ElementForm, self).__init__(*args, **kwargs)
        # self.fields['start_date'].widget.input_type = 'date'
        # self.fields['end_date'].widget.input_type = 'date'
        self.fields['element_type'].widget.attrs['onchange'] = 'myFunction(this)'
        self.fields['amount_type'].widget.attrs['onchange'] = 'check_amount_type(this)'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(SalaryStructureForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class StructureElementLinkForm(forms.ModelForm):
    class Meta:
        model = StructureElementLink
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(StructureElementLinkForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


ElementInlineFormset = forms.inlineformset_factory(SalaryStructure, StructureElementLink,
                                                   form=StructureElementLinkForm, can_delete=True)


class ElementMasterForm(forms.ModelForm):
    class Meta:
        model = Element_Master
        fields = '__all__'
        labels = {
            'element_name': _('Pay Name'),
            'db_name': _('db Name'),
            'element_type': _('Type'),
            'classification': _('classification'),
            'effective_date': _('Effective Date'),
            'retro_flag': _('Retro Flag'),
            'tax_flag': _('Tax Flag'),
            'fixed_amount': _('Fixed Amount'),
            'element_formula': _('Formula'),
            'start_date': _('Start Date'),
            'end_date': _('End Date'),
        }
        widgets = {
            'element_formula': forms.Textarea(attrs={
                'rows': 8, 'cols': 80,
                'style': 'height: 8em;',
                'class': 'form-control',
            }),
            'retro_flag': forms.CheckboxInput(attrs={
                'style': 'padding: 25px; margin:25px;'
            }),
            'tax_flag': forms.CheckboxInput(attrs={
                'style': 'padding: 25px; margin:25px;'
            }),
        }
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(ElementMasterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['element_name'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['db_name'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['element_type'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['classification'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['effective_date'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['fixed_amount'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['start_date'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['end_date'].widget.attrs['class'] = 'form-control parsley-validated'
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.fields['element_type'].queryset = LookupDet.objects.filter(
            lookup_type_fk__lookup_type_name='ELEMENT_TYPE')
        self.fields['classification'].queryset = LookupDet.objects.filter(
            lookup_type_fk__lookup_type_name='ELEMENT_CLASSIFICATION')
        self.fields['db_name'].disabled = True


class ElementBatchForm(forms.ModelForm):
    class Meta:
        model = Element_Batch
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(ElementBatchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'


class ElementBatchMasterForm(forms.ModelForm):
    class Meta:
        model = Element_Batch_Master
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(ElementBatchMasterForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False


ElementMasterInlineFormset = forms.inlineformset_factory(Element_Batch, Element_Batch_Master,
                                                         form=ElementBatchMasterForm, can_delete=True)


class ElementLinkForm(forms.ModelForm):
    class Meta:
        model = Element_Link
        fields = '__all__'
        widgets = {
            'standard_flag': forms.CheckboxInput(attrs={
                'style': 'padding: 25px; margin:25px;'
            }),
            'link_to_all_payroll_flag': forms.CheckboxInput(attrs={
                'style': 'padding: 25px; margin:25px;'
            }),
        }
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(ElementLinkForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if not self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True


class CustomPythonRuleForm(forms.ModelForm):
    class Meta:
        model = Custom_Python_Rule
        exclude = ('help_text',)
        rule_definition = forms.CharField(
            widget=forms.Textarea(),
            help_text='Write here your message!'
        )
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "توجد قاعدة أخري مسجلة بنفس الاسم!",
            }
        }

    def __init__(self, *args, **kwargs):
        super(CustomPythonRuleForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
