from django import forms
from crispy_forms.helper import FormHelper
from datetime import date
from django.db.models import Q
from defenition.models import LookupType, LookupDet
from manage_payroll.models import (Assignment_Batch, Assignment_Batch_Exclude,
                                   Assignment_Batch_Include, Payment_Type, Payment_Method,
                                   Bank_Master, Payroll_Master, Payroll_Period)

common_items_to_execlude = (
                            'enterprise',
    'created_by', 'creation_date',
    'last_update_by',  'last_update_date',
    'attribute1',    'attribute2',    'attribute3',
    'attribute4',    'attribute5',    'attribute6',
    'attribute7',    'attribute8',    'attribute9',
    'attribute10',    'attribute11',    'attribute12',
    'attribute13',    'attribute14',    'attribute15',
)

class Bank_MasterForm(forms.ModelForm):
    class Meta:
        model = Bank_Master
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Bank_MasterForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        # self.fields["payment_type"].queryset= LookupDet.objects.filter(lookup_type_fk__lookup_type_name='payment_type_list')

#####################################################################################################

class PayrollMasterForm(forms.ModelForm):
    class Meta:
        model = Payroll_Master
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(PayrollMasterForm, self).__init__(*args, **kwargs)
        self.fields['first_pay_period'].widget.input_type = 'date'
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.fields['period_type'].queryset = LookupDet.objects.filter(lookup_type_fk__lookup_type_name='PERIOD_TYPE')
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True

class AssignmentBatchForm(forms.ModelForm):
    class Meta:
        model = Assignment_Batch
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(AssignmentBatchForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True

class AssignmentBatchIncludeForm(forms.ModelForm):
    class Meta:
        model = Assignment_Batch_Include
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(AssignmentBatchIncludeForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

BatchIncludeFormSet = forms.inlineformset_factory(Assignment_Batch, Assignment_Batch_Include, form=AssignmentBatchIncludeForm, can_delete=False)

class AssignmentBatchExcludeForm(forms.ModelForm):
    class Meta:
        model = Assignment_Batch_Exclude
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(AssignmentBatchExcludeForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False

BatchExcludeFormSet = forms.inlineformset_factory(Assignment_Batch, Assignment_Batch_Exclude, form=AssignmentBatchExcludeForm, can_delete=False)

class Payment_Type_Form(forms.ModelForm):
    class Meta:
        model = Payment_Type
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Payment_Type_Form, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['category'].queryset = LookupDet.objects.filter(lookup_type_fk__lookup_type_name='PAYMENT_TYPE_CATEGORY')

class Payment_Method_Form(forms.ModelForm):
    class Meta:
        model = Payment_Method
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Payment_Method_Form, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'checkbox'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
PaymentMethodInline = forms.inlineformset_factory(Payment_Type, Payment_Method, form=Payment_Method_Form, can_delete=False)
