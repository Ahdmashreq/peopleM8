from django.db import models
from company.models import Enterprise , Department, Job, Position
from datetime import date
import datetime
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField



# gehad : Performance models.
class Performance(models.Model):
    performance_name = models.CharField(max_length=100, verbose_name=_('Performance Name'))
    company = models.ForeignKey(Enterprise, on_delete=models.CASCADE, blank=True, null=True,)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True,)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True,)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True,)
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))


    def __str__(self):
        return self.performance_name


class PerformanceRating(models.Model):
    Rating = [
        ('Over all' , 'Over all'),
        ('Core' , 'Core'),
        ('Job' , 'Job')
    ]
    ScoreKey = [
        ('1' , '1'),
        ('2' , '2'),
        ('3' , '3'),
        ('4' , '4'),
        ('5' , '5'),
        ('6' , '6'),
        ('7' , '7'),
        ('8' , '8'),
        ('9' , '9'),
    ]
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    rating = models.CharField(choices=Rating , max_length=25)
    score_key = models.CharField(choices=ScoreKey,  max_length=25, default='1')
    score_value = models.CharField(max_length=255,blank=True, null=True, )

    def __str__(self):
        return self.rating


class PerformanceTitle(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.ForeignKey(PerformanceTitle, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    help_text = models.TextField()   

    def __str__(self):
        return self.question 



