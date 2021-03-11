from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db import IntegrityError
from django.utils import translation
from django.utils.translation import to_locale, get_language
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q
from company.models import *


# gehad : createPerformance


@login_required(login_url='home:user-login')
def listPerformance(request):
    performances_list = Performance.objects.all()
    context = {
        'page_title': _('User Companies List'),
        'performances_list': performances_list,
    }
    return render(request, 'performance-list.html', context)



@login_required(login_url='home:user-login')
def createPerformance(request):
    performance_form = PerformanceForm()
    if request.method == 'POST':
        performance_form = PerformanceForm(request.POST)
        if performance_form.is_valid():
            performance_obj = performance_form.save()
            if 'Save and exit' in request.POST:
                    return redirect('performance:performance-list')
            elif 'Save and add' in request.POST:
                    return redirect('performance:rating-create',
                        per_id = performance_obj.id)
        else:
            print(performance_form.errors) 
            return redirect('home:homepage')                 
    else:
        myContext = {
        "page_title": _("create performance"),
        "performance_form": performance_form,
    }
    return render(request, 'create-performance.html', myContext)



@login_required(login_url='home:user-login')
def createPerformanceRating(request,per_id):
    performance_rating_formset = RatingInline(queryset=PerformanceRating.objects.none())
    performance = Performance.objects.get(id=per_id)
    if request.method == 'POST':
        performance_rating_formset = RatingInline(request.POST)
        print(len(performance_rating_formset.forms))
        if performance_rating_formset.is_valid():
            print(len(performance_rating_formset))
            for form in performance_rating_formset:
                obj = form.save(commit=False)
                obj.performance = performance
                obj.save()
                print("created")
                if 'Save and exit' in request.POST:
                    return redirect('performance:performance-list')
                elif 'Save and add' in request.POST:
                    return redirect('performance:rating-create',
                        per_id = per_id)
        else:
            print(performance_rating_formset.errors) 
            return redirect('home:homepage')
                        
    else:
        myContext = {
        "page_title": _("create rating"),
        "performance_rating_formset": performance_rating_formset,
    }
    return render(request, 'create-rating.html', myContext)



@login_required(login_url='home:user-login')
def performanceManagement(request):
    context = {
        'page_title': _('Performance Management'),
    }
    return render(request, 'performance-management.html', context)



@login_required(login_url='home:user-login')
def listRatingPerformance(request, ret_id):
    page_title =""
    performances_list =[]
    if ret_id == 1:
        performances_list = PerformanceRating.objects.filter(rating= 'Over all')
        page_title: _('Overall Performances')
    elif ret_id == 2:
        performances_list = PerformanceRating.objects.filter(rating= 'Core')
        page_title : _('Core Performances')
    elif ret_id == 3:
        performances_list = PerformanceRating.objects.filter(rating= 'Job')
        page_title : _('Jobrole Performances')
    context = {
        'page_title': page_title,
        'performances_list': performances_list,
        'ret_id' : ret_id
    }
    return render(request, 'rating-performance-list.html', context)



@login_required(login_url='home:user-login')
def createSegment(request,per_id,ret_id):
    print(per_id)
    performance = Performance.objects.get(id = per_id)
    rating =""

    if ret_id == 1:
        rating = 'Over all'
    elif ret_id == 2:
        rating = 'Core'
    elif ret_id == 3:
        rating = 'Job'    
    segment_form = SegmentForm()
    if request.method == 'POST':
        segment_form = SegmentForm(request.POST)
        if segment_form.is_valid():
            segment_obj = segment_form.save(commit=False)
            segment_obj.performance = performance
            segment_obj.rating = rating
            segment_obj.save()
            print("created")
            return redirect('performance:performance-list')
                        
        else:
            print(segment_form.errors) 
            return redirect('home:homepage')                 
    else:
        myContext = {
        "page_title": _("Create Segment"),
        "segment_form": segment_form,
    }
    return render(request, 'create-segment.html', myContext)

