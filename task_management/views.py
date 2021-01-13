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
from task_management.models import Project, Project_Task
from task_management.forms import ProjectForm, Project_Tasks_ModelFormset

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
        task_form = Project_Tasks_ModelFormset()
        if request.method == 'POST':
            task_form = Project_Tasks_ModelFormset(request.POST)
            if task_form.is_valid():
                task_obj = task_form.save(commit=False)
                for task in task_obj:
                    task.created_by = request.user
                    task.save()
        project_context = {
                           'page_title':'Create New Project',
                           'task_form':task_form,
        }
        return render(request, 'tasks-create.html', project_context)


@login_required(login_url='home:user-login')
def project_task_update_view(request):
    pass
