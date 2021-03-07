from django import forms
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
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'estimated_date_of_travel_to' : forms.DateInput(attrs={'class': 'form-control',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'duration_of_hotel_from' : forms.DateInput(attrs={'class': 'form-control',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'duration_of_hotel_to' : forms.DateInput(attrs={'class': 'form-control',
                                                                          'data-provide':"datepicker",
                                                                          'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2"}),
                 'prupose_of_trip' : forms.TextInput(attrs={'class': 'form-control'}),
                 'project_name' : forms.TextInput(attrs={'class': 'form-control'}),
                 'transportation_type_to_des' : forms.Select(attrs={'class': 'form-control'}),
                 'emp' : forms.Select(attrs={'class': 'form-control'}),
                 'manager' : forms.Select(attrs={'class': 'form-control'}),
                 'department' : forms.Select(attrs={'class': 'form-control'}),
                 'position' : forms.Select(attrs={'class': 'form-control'}),
                 'destination' : forms.TextInput(attrs={'class': 'form-control'}),
                 'ticket_cost' : forms.NumberInput(attrs={'class': 'form-control prc'}),
                 'fuel_cost' : forms.NumberInput(attrs={'class': 'form-control prc'}),
                 'transportation_type_in_city' : forms.Select(attrs={'class': 'form-control'}),
                 'cost' : forms.NumberInput(attrs={'class': 'form-control prc'}),
                 'hotel_name' : forms.TextInput(attrs={'class': 'form-control'}),
                 'cost_per_night' : forms.NumberInput(attrs={'class': 'form-control prc'}),
                 'status' : forms.TextInput(attrs={'class': 'form-control'}),
                 'accomodation': forms.RadioSelect(),
        }
    def __init__(self, *args, **kwargs):
        super(FormAllowance, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

class PurchaseRequestForm(forms.ModelForm):
    class Meta():
        """
        Ziad
        7/3/2021
        Delete payment method and vendor details 
        """
        model = Purchase_Request
        fields = ['department' , 'date_of_purchase' , 'office' , 'purpose']
        exclude = ['ordered_by','created_by', 'creation_date', 'last_update_by', 'last_update_date']
        widgets = {
                 'date_of_purchase' : forms.DateInput(attrs={'class': 'form-control',
                                                             'data-provide':"datepicker",
                                                             'wtx-context':"2A377B0C-58AD-4885-B9FB-B5AC9788D0F2",
                                                             'required' : True }),
                 'order_number' : forms.TextInput(attrs={'class': 'form-control'}),
                 'ordered_by' : forms.Select(attrs={'class': 'form-control'}),
                 'department' : forms.Select(attrs={'class': 'form-control', 'required' : True}),
                 'office' : forms.TextInput(attrs={'class': 'form-control', 'required' : True}),
                 'purpose' : forms.Textarea(attrs={
                                                   'rows': 2,'cols': 40,
                                                   'style': 'height: 6em;',
                                                   'class': 'form-control','required' : True}),
                 
        }
    def __init__(self, *args, **kwargs):
        super(PurchaseRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

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

Purchase_Item_formset = forms.inlineformset_factory(Purchase_Request, Purchase_Item,form=PurchaseItemsForm, extra=3, can_delete=True)
