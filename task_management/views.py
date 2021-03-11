from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
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
from MashreqPayroll.utils import allowed_user
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
    loged_in_user_groups = request.user.groups.filter(user=request.user)
    if  'Admin' or 'PYTHON_DEV' in loged_in_user_groups:
        all_tasks = Project_Task.objects.all()
    else:
        all_tasks = Project_Task.objects.filter(assigned_to=request.user)

    grouped_project = all_tasks.values('project__name','project__id').annotate(project_count=Count('project_id'))
    project_context = {
                       'page_title':'List All Tasks',
                       'all_tasks':all_tasks,
                       'grouped_project':grouped_project,
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


def load_parent_tasks(request):
    """
    function view to load parent tasks according to project tasks
    By: amira
    Date: 11/3
    """
    print(request.GET)
    try:
        project_id = request.GET.get('project')
        parent_tasks = Project_Task.objects.filter(project=project_id)
        context = {
            'tasks': parent_tasks
        }
    except Exception as e:
        print('load parent tasks error --> ', e)
        context = {}
    return render(request, 'tasks_dropdown_list_options.html', context)
