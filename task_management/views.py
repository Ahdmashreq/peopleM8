from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.translation import to_locale, get_language
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from custom_user.models import User
from task_management.models import Project, Project_Task
from task_management.forms import ProjectForm, Project_Tasks_ModelFormset, ProjectTaskForm

@login_required(login_url='home:user-login')
def project_list_view(request):
    all_projects = Project.objects.filter()
    project_context = {
                       'page_title':'List All Projects',
                       'all_projects':all_projects,
    }
    return render(request, 'list-projects.html', project_context)


@login_required(login_url='home:user-login')
def project_create_view(request):
    project_form = ProjectForm()
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_obj = project_form.save(commit=False)
            project_obj.company = request.user.company
            project_obj.created_by = request.user
            project_obj.save()
    project_context = {
                       'page_title':'Create New Project',
                       'project_form':project_form,
    }
    return render(request, '', project_context)


@login_required(login_url='home:user-login')
def project_update_view(request):
    pass

# ##############################################################################

@login_required(login_url='home:user-login')
def project_task_list_view(request):
    all_tasks = Project_Task.objects.filter()
    project_context = {
                       'page_title':'List All Tasks',
                       'all_tasks':all_tasks,
    }
    return render(request, 'list-tasks.html', project_context)


@login_required(login_url='home:user-login')
def project_task_create_view(request):
        task_form = ProjectTaskForm()
        task_form.fields['assigned_to'].queryset = User.objects.filter(
            company=request.user.company)
        if request.method == 'POST':
            task_form = ProjectTaskForm(request.POST)
            if task_form.is_valid():
                task_obj = task_form.save(commit=False)
                # for task in task_obj:
                task_obj.created_by = request.user
                task_obj.save()
                return redirect('task_management:task-list')
                messages.success(request, 'Saved Successfully.')
            else:
                messages.error(request, task_form.errors)
        project_context = {
                           'page_title':'Create New Project',
                           'task_form':task_form,
        }
        return render(request, 'task-create.html', project_context)


@login_required(login_url='home:user-login')
def project_task_update_view(request, task_id):
    required_task = Project_Task.objects.get(id=task_id)
    task_form = ProjectTaskForm(instance=required_task)
    task_form.fields['assigned_to'].queryset = User.objects.filter(
        company=request.user.company)
    if request.method == 'POST':
        task_form = ProjectTaskForm(request.POST, instance=required_task)
        if task_form.is_valid():
            task_obj = task_form.save(commit=False)
            # for task in task_obj:
            task_obj.created_by = request.user
            task_obj.save()
            return redirect('task_management:task-list')
            messages.success(request, 'Saved Successfully.')
        else:
            messages.error(request, task_form.errors)
    project_context = {
                       'page_title':'Create New Project',
                       'task_form':task_form,
    }
    return render(request, 'task-create.html', project_context)
