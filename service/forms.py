from django import forms
from django.forms import BaseInlineFormSet
from crispy_forms.helper import FormHelper
from django.forms import ValidationError
from django.core import validators
from django.db.models import Sum
from service.models import Bussiness_Travel, Purchase_Request, Purchase_Item

class FormAllowance(forms.ModelForm):
    class Meta():
        model = Bussiness_Travel
        fields = '__all__'
        exclude = ['emp','manager','department','position','status','created_by','creation_date','last_update_by','last_update_date']
        widgets = {
                 'estimated_date_of_travel_from' : forms.DateInput(attrs={'class': 'form-control',
                                                                          'required': 'true',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'estimated_date_of_travel_to' : forms.DateInput(attrs={'class': 'form-control',
                                                                        'required': 'true',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'duration_of_hotel_from' : forms.DateInput(attrs={'class': 'form-control',
                                                                        'required': 'true',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'duration_of_hotel_to' : forms.DateInput(attrs={'class': 'form-control',
                                                                        'required': 'true',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'prupose_of_trip' : forms.TextInput(attrs={'class': 'form-control' , 'required': 'true' }),
                 'project_name' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
                 'emp' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
                 'manager' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
                 'department' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
                 'position' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
                 'destination' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
                 'ticket_cost' : forms.NumberInput(attrs={'class': 'form-control prc', 'required': 'true'}),
                 'fuel_cost' : forms.NumberInput(attrs={'class': 'form-control prc', 'required': 'true'}),
                 'transportation_type_in_city' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
                 'cost' : forms.NumberInput(attrs={'class': 'form-control prc', 'required': 'true'}),
                 'hotel_name' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
                 'cost_per_night' : forms.NumberInput(attrs={'class': 'form-control prc', 'required': 'true'}),
                 'status' : forms.TextInput(attrs={'class': 'form-control' }),
                 'accomodation': forms.RadioSelect(attrs={'required': 'true'}),
        }
    def __init__(self, *args, **kwargs):
        super(FormAllowance, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

class PurchaseRequestForm(forms.ModelForm):
    class Meta():
        model = Purchase_Request
        fields = '__all__'
        exclude = ['ordered_by','created_by', 'creation_date', 'last_update_by', 'last_update_date']
        widgets = {
                 'date_of_purchase' : forms.DateInput(attrs={'class': 'form-control',
                                                             'data-provide':"datepicker",
                                                             'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'order_number' : forms.TextInput(attrs={'class': 'form-control'}),
                 'ordered_by' : forms.Select(attrs={'class': 'form-control'}),
                 'department' : forms.Select(attrs={'class': 'form-control','required': 'true'}),
                 'office' : forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
                 'payment_method' : forms.Select(attrs={'class': 'form-control','required': 'true'}),
                 'purpose' : forms.Textarea(attrs={
                                                   'rows': 2,'cols': 40,
                                                   'style': 'height: 6em;',
                                                   'class': 'form-control', 'required': 'true'}),
                 'vendor_details' :forms.Textarea(attrs={
                                                   'rows': 2,'cols': 40,
                                                   'style': 'height: 6em;',
                                                   'class': 'form-control', 'required': 'true'}),
        }
    def __init__(self, *args, **kwargs):
        super(PurchaseRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

class RequiredFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False

class PurchaseItemsForm(forms.ModelForm):
    class Meta():
        model = Purchase_Item
        fields = '__all__'
        exclude = ['created_by','creation_date','last_update_by','last_update_date']
        widgets = {
                 'item_description' : forms.TextInput(attrs={'class': 'form-control'}),
                 'vendor_name' : forms.TextInput(attrs={'class': 'form-control'}),
                 'unit_price' : forms.NumberInput(attrs={'class': 'form-control'}),
                 'qnt' : forms.NumberInput(attrs={'class': 'form-control'}),
        }

Purchase_Item_formset = forms.inlineformset_factory(Purchase_Request, Purchase_Item,form=PurchaseItemsForm,formset = RequiredFormSet ,extra=1, can_delete=True)
