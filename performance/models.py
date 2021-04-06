from django.db import models
from company.models import Enterprise , Department, Job, Position
from datetime import date
import datetime
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from employee.models import Employee
from django.conf import settings


class Performance(models.Model):
    performance_name = models.CharField(max_length=100,  unique=True ,verbose_name=_('Performance Name'))
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
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='rating')
    rating = models.CharField(choices=Rating , max_length=25)
    score_key = models.CharField(choices=ScoreKey,  max_length=25)
    score_value = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.score_key + " - " +  self.score_value 


class Segment(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='segments')
    rating = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField()

    def __str__(self):
        return self.title



class Question(models.Model):
    Type = [
        ('text' , 'text'),
        ('slider' , 'slider'),
    ]
    title = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=255)
    help_text = models.TextField() 
    question_type = models.CharField(choices=Type,  max_length=25)
  

    def __str__(self):
        return self.question 



class EmployeePerformance(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    overall_score = models.ForeignKey(PerformanceRating, on_delete=models.CASCADE, related_name='overall')
    core_score = models.ForeignKey(PerformanceRating, on_delete=models.CASCADE, related_name='core')
    job_score = models.ForeignKey(PerformanceRating, on_delete=models.CASCADE, related_name='job')
    comment = models.TextField( blank=True, null=True) 
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='EmployeePerformance_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='EmployeePerformance_last_updated_by')
    last_update_date = models.DateField(auto_now=True)
   
    def __str__(self):
        return self.employee.emp_name +  self.performance.performance_name




class EmployeeRating(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    score = models.ForeignKey(PerformanceRating, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='EmployeeRating_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='EmployeeRating_last_updated_by')
    last_update_date = models.DateField(auto_now=True)
   
    def __str__(self):
        return self.employee.emp_name +  self.question.question
