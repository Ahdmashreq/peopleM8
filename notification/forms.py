from django import forms
from django.forms import ValidationError
from django.core import validators
from notification.models import Notification


# standby not used by
class FormNotificationLeave(forms.ModelForm):

    class Meta():
        model = Notification
        fields='__all__'
