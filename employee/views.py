from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import to_locale, get_language
from element_definition.models import Element_Master, Element_Link
from employee.models import (Employee, JobRoll, Payment, Employee_Element)
from employee.forms import (EmployeeForm, JobRollForm, Employee_Payment_formset,
                            EmployeeElementForm, Employee_Element_Inline)
from payroll_run.models import Salary_elements
from payroll_run.forms import SalaryElementForm
from employee.fast_formula import FastFormula
from manage_payroll.models import Payment_Method
from django.utils.translation import ugettext_lazy as _

############################Employee View #################################
@login_required(login_url='/login')
def createEmployeeView(request):
    emp_form = EmployeeForm()
    jobroll_form = JobRollForm(user_v = request.user)
    payment_form = Employee_Payment_formset(queryset=Payment.objects.none())
    for payment in payment_form:
        payment.fields['payment_method'].queryset = Payment_Method.objects.filter(payment_type__enterprise = request.user.company).filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True))
    emp_element_form = Employee_Element_Inline(queryset=Employee_Element.objects.none())
    for element in emp_element_form:
        element.fields['element_id'].queryset = Element_Master.objects.none()
    if request.method == 'POST':
        emp_form = EmployeeForm(request.POST)
        jobroll_form = JobRollForm(request.user, request.POST)
        payment_form = Employee_Payment_formset(request.POST)
        emp_element_form = Employee_Element_Inline(request.POST)
        if emp_form.is_valid() and jobroll_form.is_valid() and payment_form.is_valid() and emp_element_form.is_valid():
            emp_obj = emp_form.save(commit=False)
            emp_obj.enterprise = request.user.company
            emp_obj.created_by = request.user
            emp_obj.last_update_by = request.user
            emp_obj.save()
            job_obj = jobroll_form.save(commit=False)
            job_obj.emp_id_id = emp_obj.id
            job_obj.created_by = request.user
            job_obj.last_update_by = request.user
            job_obj.save()
            payment_form = Employee_Payment_formset(
                request.POST, instance=emp_obj)
            if payment_form.is_valid():
                emp_payment_obj = payment_form.save(commit=False)
                for x in emp_payment_obj:
                    x.created_by = request.user
                    x.last_update_by = request.user
                    x.save()
            else:
                user_lang=user_lang=to_locale(get_language())
                if user_lang=='ar':
                    error_msg = '{}, لم يتم التسجيل'.format(emp_payment_obj)
                else:
                    error_msg = '{}, has somthig wrong'.format(emp_payment_obj)
                # error_msg = '{}, has somthig wrong'.format(emp_payment_obj)
                messages.success(request, success_msg)
            emp_element_form = Employee_Element_Inline(
                request.POST, instance=emp_obj)
            if emp_element_form.is_valid():
                element_obj = emp_element_form.save(commit=False)
                for x in element_obj:
                    x.created_by = request.user
                    x.last_update_by = request.user
                    x.save()
            else:

                user_lang=to_locale(get_language())
                if user_lang=='ar':
                    error_msg = '{}, لم يتم التسجيل'.format(element_obj)
                    success_msg = ' {},تم تسجيل الموظف'.format(emp_obj.emp_name)
                else:
                    error_msg = '{}, has somthig wrong'.format(element_obj)
                    success_msg = 'Employee {}, has been created successfully'.format(emp_obj.emp_name)


                    messages.success(request, success_msg)
            return redirect('employee:list-employee')
        else:
            messages.error(request, emp_form.errors)
            messages.error(request, jobroll_form.errors)
    myContext = {
        "page_title": _("create employee"),
        "emp_form": emp_form,
        "jobroll_form": jobroll_form,
        "payment_form": payment_form,
        "emp_element_form": emp_element_form,
    }
    return render(request, 'create-employee.html', myContext)


@login_required(login_url='/login')
def copy_element_values():
    element_master_obj = Element_Master.objects.filter().exclude(global_value=0)
    emp_element = Employee_Element.objects.filter()
    for x in element_master_obj:
        for z in emp_element:
            if z.element_id_id == x.id:
                z.element_value = x.global_value
                z.save()


@login_required(login_url='/login')
def listEmployeeView(request):
    emp_list = Employee.objects.filter(enterprise = request.user.company)
    myContext = {
        "page_title": _("List employees"),
        "emp_list": emp_list,
    }
    return render(request, 'list-employees.html', myContext)


@login_required(login_url='/login')
def listEmployeeCardView(request):
    emp_list = Employee.objects.filter(enterprise = request.user.company)
    myContext = {
        "page_title": _("List employees"),
        "emp_list": emp_list,
    }
    return render(request, 'list-employees-card.html', myContext)


@login_required(login_url='/login')
def viewEmployeeView(request, pk):
    required_employee = get_object_or_404(Employee, pk=pk)
    required_jobRoll = JobRoll.objects.filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True)).get(emp_id=pk)
    all_jobRoll = JobRoll.objects.filter(emp_id=pk)
    all_payment = Payment.objects.filter(emp_id=pk, end_date__isnull=True)
    all_elements = Employee_Element.objects.filter(emp_id=pk, end_date__isnull=True)
    myContext = {
        "page_title": _("view employee"),
        "required_employee": required_employee,
        "required_jobRoll": required_jobRoll,
        "all_payment": all_payment,
        "all_elements": all_elements,
        "all_jobRoll" :all_jobRoll,
    }
    return render(request, 'view-employee.html', myContext)


@login_required(login_url='/login')
def updateEmployeeView(request, pk):
    required_employee = get_object_or_404(Employee, pk=pk)
    required_jobRoll = JobRoll.objects.get(emp_id=required_employee)
    emp_form = EmployeeForm(instance=required_employee)
    jobroll_form = JobRollForm(user_v=request.user, instance=required_jobRoll)
    payment_form = Employee_Payment_formset(instance=required_employee)
    elements_form = Employee_Element_Inline(queryset=Employee_Element.objects.filter(end_date__isnull=True), instance=required_employee)

    # elements = Element_Link.objects.filter(
    #                                       Q(payroll_fk=required_jobRoll.payroll) | Q(payroll_fk__isnull=True),
    #                                       Q(element_position_id_fk=required_jobRoll.position) | Q(element_position_id_fk__isnull=True)
    #                                       )
    # for element in elements_form:
    #     element.fields['element_id'].queryset = elements

    if request.method == 'POST':
        emp_form = EmployeeForm(request.POST, instance=required_employee)
        jobroll_form = JobRollForm(request.user, request.POST, instance=required_jobRoll)
        payment_form = Employee_Payment_formset( request.POST, instance=required_employee)
        elements_form = Employee_Element_Inline( request.POST, instance=required_employee)
        if emp_form.is_valid():
            emp_obj = emp_form.save(commit=False)
            emp_obj.created_by = request.user
            emp_obj.last_update_by = request.user
            emp_obj.save()
        else:
            messages.error(request, emp_form.errors)
        if jobroll_form.is_valid():
            job_obj = jobroll_form.save(commit=False)
            job_obj.emp_id_id = emp_obj.id
            job_obj.created_by = request.user
            job_obj.last_update_by = request.user
            job_obj.save()
        else:
            messages.error(request, jobroll_form.errors)
        payment_form = Employee_Payment_formset(request.POST, instance=emp_obj)
        if payment_form.is_valid():
            emp_payment_obj = payment_form.save(commit=False)
            for x in emp_payment_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
        else:
            messages.error(request, payment_form.errors)
        emp_element_form = Employee_Element_Inline(request.POST, instance=emp_obj)
        if emp_element_form.is_valid():
            emp_element_obj = emp_element_form.save(commit=False)
            for x in emp_element_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
        else:
            messages.error(request, emp_element_form.errors)
        Employee_Element.set_formula_amount(required_employee)

        user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = ' {},تم تسجيل الموظف'.format(emp_obj.emp_name)
        else:
            success_msg = 'Employee {}, has been created successfully'.format(emp_obj.emp_name)

        success_msg = 'Employee {} updated successfully'.format(emp_obj.emp_name)
        # messages.success(request, success_msg)
        return redirect('employee:list-employee')

    myContext = {
        "page_title": _("update employee"),
        "emp_form": emp_form,
        "jobroll_form": jobroll_form,
        "payment_form": payment_form,
        "emp_element_form": elements_form,
    }
    return render(request, 'create-employee.html', myContext)


@login_required(login_url='/login')
def deleteEmployeeView(request, pk):
    required_employee = get_object_or_404(Employee, pk=pk)
    required_jobRoll = get_object_or_404(JobRoll, emp_id=pk)
    try:
        emp_form = EmployeeForm(instance=required_employee)
        end_date_obj = emp_form.save(commit=False)
        end_date_obj.end_date = date.today()
        end_date_obj.save(update_fields=['end_date'])
        user_lang=to_locale(get_language())
        if user_lang=='ar':

            success_msg = ' {},تم حذف الموظف'.format(required_employee)
        else:

            success_msg = 'Employee {} was deleted successfully'.format(
                required_employee)

        # success_msg = 'Employee {} was deleted successfully'.format(
            # required_employee)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = '{} لم يتم حذف '.format(required_employee)
        else:
            success_msg = '{} cannot be deleted '.format(required_employee)
        # success_msg = 'Employee {} cannot be deleted'.format(
            # required_employee)
        messages.error(request, success_msg)
        raise e
    return redirect('employee:list-employee')
