from django import forms
from .models import *
from datetime import date
from company.models import Department , Position , Job , Enterprise
from custom_user.models import User
from django.db.models import Q
from django.db import models




# gehad : createPerformance forms.
class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = '__all__'

        
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PerformanceForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'
        self.fields['department'].queryset = Department.objects.filter(enterprise=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))
        self.fields['job'].queryset = Job.objects.filter(enterprise=user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))
        

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

RatingInline = forms.modelformset_factory(PerformanceRating, form=RatingForm, extra=1, can_delete=False)



class SegmentForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = ('title','desc')

    def __init__(self, *args, **kwargs):
        super(SegmentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','help_text')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

QuestionInline = forms.modelformset_factory(Question, form=QuestionForm, extra=1, can_delete=False)

