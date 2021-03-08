from django import forms
from .models import *
from datetime import date


# gehad : createPerformance forms.
class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PerformanceForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RatingForm(forms.ModelForm):
    class Meta:
        model = PerformanceRating
        fields = ('rating', 'score_key' , 'score_value')
    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

RatingInline = forms.modelformset_factory(PerformanceRating, form=RatingForm, extra=3, can_delete=False)


   