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
from custom_user.models import User
from django.core.exceptions import ObjectDoesNotExist
from employee.models import Employee, JobRoll


@login_required(login_url='home:user-login')
def listPerformance(request):
    performances_list = Performance.objects.all()
    context = {
        'page_title': _('Performances List'),
        'performances_list': performances_list,
    }
    return render(request, 'performance-list.html', context)

@login_required(login_url='home:user-login')
def performanceView(request,pk):
    try:
        performance = Performance.objects.get(id=pk)
    except ObjectDoesNotExist as e:
        return False
    page_title = ''
    overall_segments = Segment.objects.filter(performance = performance ,rating= 'Over all')
    core_segments = Segment.objects.filter(performance = performance ,rating= 'Core')
    job_segments = Segment.objects.filter(performance = performance ,rating= 'Job')


    context = {
        'page_title': 'Performance Overview',
        'performance' :performance,
        'overall_segments': overall_segments,
        'core_segments' : core_segments,
        'job_segments' : job_segments,
    }
    return render(request, 'performances.html', context)
    

@login_required(login_url='home:user-login')
def createPerformance(request):
    user = User.objects.get(id=request.user.id)
    company = user.company
    performance_form = PerformanceForm(company)
    if request.method == 'POST':
        performance_form = PerformanceForm(company, request.POST)
        if performance_form.is_valid():
            performance_obj = performance_form.save(commit=False)
            performance_obj.company = company
            performance_obj.save() 

            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = ' {},تم إنشاء التقييم'.format(performance_obj)
            else:
                success_msg = 'performance {}, has been updated successfully'.format(
                    performance_obj)
            messages.success(request, success_msg)        
            if 'Save and exit' in request.POST:
                    return redirect('performance:performance-list')
            elif 'Save and add' in request.POST:
                    return redirect('performance:rating-create',
                        per_id = performance_obj.id)
        else:
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = '{} لم يتم الإنشاء '.format(performance_obj)
            else:
                success_msg = '{} cannot be created '.format(performance_obj)
            messages.error(request, success_msg)
            print(performance_form.errors) 
            return redirect('performance:performance-list')                 
    else:
        myContext = {
        "page_title": _("create performance"),
        "performance_form": performance_form,
        "company":company,
    }
    return render(request, 'create-performance.html', myContext)

@login_required(login_url='home:user-login')
def updatePerformance(request, pk):
    performance = Performance.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    company = user.company
    performance_form = PerformanceForm(company, instance=performance)
    if request.method == 'POST':
        performance_form = PerformanceForm(company, request.POST, instance=performance)
        if performance_form.is_valid() :
            performance_form.save()
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = ' {},تم تعديل التقييم'.format(performance)
            else:
                success_msg = 'performance {}, has been updated successfully'.format(
                    performance)
            messages.success(request, success_msg)        
            return redirect('performance:performance-list')
        else:
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = '{} لم يتم التعديل '.format(performance)
            else:
                success_msg = '{} cannot be updated '.format(performance)
            messages.error(request, success_msg)
            return redirect('performance:performance-edit',pk=pk )
    else:
        myContext = {
        "page_title": _("update performance"),
        "performance_form": performance_form,
        "company":company,
    }
    return render(request, 'create-performance.html', myContext)   

@login_required(login_url='home:user-login')
def deletePerformance(request, pk):
    performance = Performance.objects.get(id=pk)
    try:
        performance.delete()
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = ' {},تم حذف التقييم'.format(performance)
        else:
            success_msg = 'Performance {} was deleted successfully'.format(
                performance)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = '{} لم يتم حذف '.format(performance)
        else:
            success_msg = '{} cannot be deleted '.format(performance)
        messages.error(request, success_msg)
        raise e
    return redirect('performance:performance-list')


############################################################

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
                
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = ' {},تم إنشاء التقييم'.format(obj)
            else:
                success_msg = 'rating {}, has been updated successfully'.format(
                    obj)
            messages.success(request, success_msg)        
            if 'Save and exit' in request.POST:
                return redirect('performance:management',
                        pk = performance.id)
            elif 'Save and add' in request.POST:
                return redirect('performance:rating-create',
                        per_id = per_id)
        else:
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = '{} لم يتم الإنشاء '.format(obj)
            else:
                success_msg = '{} cannot be updated '.format(obj)
            messages.error(request, success_msg)

            print(performance_rating_formset.errors) 
            return redirect('performance:rating-create',
                        per_id = per_id)
                        
    else:
        myContext = {
        "page_title": _("create rating"),
        "performance_rating_formset": performance_rating_formset,
    }
    return render(request, 'create-rating.html', myContext)



@login_required(login_url='home:user-login')
def performanceManagement(request,pk):
    try:
        performance = Performance.objects.get(id=pk)
    except ObjectDoesNotExist as e:
        return False 

    context = {
        'page_title': performance.performance_name,
        'pk' : pk,
    }
    return render(request, 'performance-management.html', context)

############################################################################

@login_required(login_url='home:user-login')
def listSegment(request,pk, ret_id):
    try:
        performance = Performance.objects.get(id=pk)
    except ObjectDoesNotExist as e:
        return False
    page_title = ''
    segments =[]
    if ret_id == 1:
        segments = Segment.objects.filter(performance = performance ,rating= 'Over all')
        page_title = 'Overall Segments'

    elif ret_id == 2:
        segments = Segment.objects.filter(performance = performance ,rating= 'Core')
        page_title  = 'Core Segments'

    elif ret_id == 3:
        segments = Segment.objects.filter(performance = performance ,rating= 'Job')
        page_title  =  'Jobrole Segments'


    context = {
        'page_title': page_title,
        'segments': segments,
        'ret_id' : ret_id,
        'pk' : pk,
    }
    return render(request, 'segment-list.html', context)



@login_required(login_url='home:user-login')
def createSegment(request,per_id,ret_id):
    question_formset = QuestionInline(queryset=Question.objects.none())
    performance = Performance.objects.get(id = per_id)
    rating =""
    scores = ""

    if ret_id == 1:
        rating = 'Over all'
        scores = PerformanceRating.objects.filter(performance=performance , rating= 'Over all')
    elif ret_id == 2:
        rating = 'Core'
        scores = PerformanceRating.objects.filter(performance=performance , rating= 'Core')
    elif ret_id == 3:
        rating = 'Job'   
        scores = PerformanceRating.objects.filter(performance=performance , rating= 'Job') 
    segment_form = SegmentForm()
    if request.method == 'POST':
        segment_form = SegmentForm(request.POST)
        question_formset = QuestionInline(request.POST)
        if segment_form.is_valid():
            segment_obj = segment_form.save(commit=False)
            segment_obj.performance = performance
            segment_obj.rating = rating
            segment_obj.save()    
            if question_formset.is_valid():
                for form in question_formset:
                    obj = form.save(commit=False)
                    obj.title = segment_obj
                    obj.save()
            else:
                print(question_formset.errors)         
                    
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = ' {},تم إنشاء الشريحة'.format(segment_obj)
            else:
                success_msg = 'segment {}, has been updated successfully'.format(
                        segment_obj)
            messages.success(request, success_msg)                  
                 
        else:
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = '{} لم يتم الإنشاء '.format(segment_obj)
            else:
                success_msg = '{} cannot be updated '.format(segment_obj)
            messages.error(request, success_msg)
            print(segment_form.errors)

        return redirect('performance:segments',
                        pk = per_id,ret_id=ret_id )
                
    else:
        myContext = {
        "page_title": _("Create Segment"),
        "segment_form": segment_form,
        "question_formset": question_formset,
        "scores": scores,
        "per_id":per_id,
        "ret_id":ret_id,
    }
    return render(request, 'create-segment.html', myContext)


@login_required(login_url='home:user-login')
def updateSegment(request,pk,ret_id):
    segment = Segment.objects.get(id=pk)
    performance = segment.performance
    segment_form = SegmentForm(instance=segment)
    question_formset = QuestionInline(queryset=Question.objects.filter(title=segment))
    rating =""
    scores = ""
    if ret_id == 1:
        rating = 'Over all'
        scores = PerformanceRating.objects.filter(performance=performance , rating= 'Over all')
    elif ret_id == 2:
        rating = 'Core'
        scores = PerformanceRating.objects.filter(performance=performance , rating= 'Core')
    elif ret_id == 3:
        rating = 'Job'   
        scores = PerformanceRating.objects.filter(performance=performance , rating= 'Job') 

    if request.method == 'POST':
        segment_form = SegmentForm(request.POST, instance=segment)
        question_formset = QuestionInline(request.POST ,queryset=Question.objects.filter(title=segment))
        print(request.POST.values)
        if segment_form.is_valid() and question_formset.is_valid():
            segment_obj = segment_form.save(commit=False)
            segment_obj.performance = performance
            segment_obj.rating = rating
            segment_obj.save() 

            for form in question_formset:
                obj = form.save(commit=False)
                obj.title = segment_obj
                obj.save()

            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = ' {},تم تعديل الشريحة'.format(segment_obj)
            else:
                success_msg = 'segment {}, has been updated successfully'.format(
                        segment_obj)
            messages.success(request, success_msg) 
                
        else:
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = '{} لم يتم الإنشاء '.format(segment_obj)
            else:
                success_msg = '{} cannot be updated '.format(segment_obj)
            messages.error(request, success_msg)
            print(segment_form.errors) 
            print(question_formset.errors) 
            
        return redirect('performance:segments',
                        pk = performance.id,ret_id=ret_id )
                
    else:
        myContext = {
        "page_title": _("Update Segment"),
        "segment_form": segment_form,
        "question_formset": question_formset,
        "scores": scores,
        "per_id":performance.id,
        "ret_id":ret_id,
    }
    return render(request, 'create-segment.html', myContext)




@login_required(login_url='home:user-login')
def deleteSegment(request, pk, ret_id):
    segment = Segment.objects.get(id=pk)
    performance = segment.performance
    try:
        segment.delete()
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = ' {},تم حذف الشريحة '.format(segment)
        else:
            success_msg = 'segment {} was deleted successfully'.format(
                segment)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = '{} لم يتم حذف '.format(segment)
        else:
            success_msg = '{} cannot be deleted '.format(segment)
        messages.error(request, success_msg)
        raise e
    return redirect('performance:segments',
                        pk = performance.id,ret_id=ret_id )

#####################################################

@login_required(login_url='home:user-login')
def employeesperformance(request):
    user = request.user
    try:
        employee = Employee.objects.get(user = user)
    except ObjectDoesNotExist as e:
        return False
    employees = JobRoll.objects.filter(manager=employee)
    context = {
        'employees': employees, 
        }
    return render(request, 'employees-performance.html', context)



@login_required(login_url='home:user-login')
def employeeSegments(request,emp_pos):
    position = Position.objects.get(id=emp_pos)
    segments = Segment.objects.filter(performance__position = position)
    context = {
        'segments': segments, 
        }
    return render(request, 'employees-segments.html', context)
