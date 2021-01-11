from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from custom_user.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple


class CustomUserCreationForm(UserCreationForm):
    company_name = forms.CharField(max_length=60, required=True, help_text='This Field is Required.',label=_('Name'))
    business_unit_name = forms.CharField(max_length=40, required=True,label=_('Business Unit Name'))
    reg_tax_num = forms.CharField(max_length=40, required=True,label=_('Reg Tax Num'))
    commercail_record = forms.CharField(max_length=40, required=True,label=_('Commercail Record '))
    class Meta(UserCreationForm):
        model = User
        fields = ('company_name', 'business_unit_name',
                   'reg_tax_num', 'commercail_record','username', 'email')
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'employee_type', 'email')

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'employee_type', 'email')

#group forms
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows': '3'}),
        }
        def __init__(self, *args, **kwargs):
            super(EmployeeStructureLinkForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
            self.helper = FormHelper()
            self.helper.form_show_labels = True

class GroupViewForm(forms.ModelForm):
    class Meta:
        model=Group
        fields='__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows': '3','disabled':True}),
            'name':forms.TextInput(attrs={'readonly':'readonly'}),
            # 'permissions':forms.TextInput(attrs={'readonly':'readonly'})
        }
        
                
