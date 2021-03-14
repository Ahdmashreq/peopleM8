from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect , HttpResponse
from django.views.generic import DetailView, ListView, View
from django.contrib import messages
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils.translation import to_locale, get_language
from django.db.models import Q
import calendar
from django.db.models import Avg, Count
from payroll_run.models import Salary_elements
from payroll_run.forms import SalaryElementForm, Salary_Element_Inline
from element_definition.models import Element_Master, Element_Batch, Element_Batch_Master, Element , SalaryStructure
from manage_payroll.models import Assignment_Batch, Assignment_Batch_Include, Assignment_Batch_Exclude
from employee.models import Employee_Element, Employee, JobRoll, Payment, EmployeeStructureLink
from employee.forms import Employee_Element_Inline
from django.utils.translation import ugettext_lazy as _
# ############################################################
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration  # amira: fixing error on print
# ############################################################
from .new_tax_rules import Tax_Deduction_Amount
from payroll_run.salary_calculations import Salary_Calculator


@login_required(login_url='home:user-login')
def listSalaryView(request):
    salary_list = Salary_elements.objects.filter(
        (Q(end_date__gt=date.today()) | Q(end_date__isnull=True))).values(
        'salary_month', 'salary_year',
        'is_final').annotate(num_salaries=Count('salary_month'))
    salaryContext = {
        "page_title": _("salary list"),
        "salary_list": salary_list,
    }
    return render(request, 'list-salary.html', salaryContext)


# @login_required(login_url='home:user-login')
def includeAssignmentEmployeeFunction(batch):
    included_emps = set()
    assignment_batch = Assignment_Batch.objects.get(id=batch.id)
    include_query = Assignment_Batch_Include.objects.filter(include_batch_id=assignment_batch).exclude(
        Q(end_date__gte=date.today()) | Q(end_date__isnull=False))
    dept_set = set()
    job_set = set()
    position_set = set()
    emp_set = set()
    for x in include_query:
        if x.dept_id is not None:
            dept_set.add(x.dept_id.id)
        if x.position_id is not None:
            position_set.add(x.position_id.id)
        if x.job_id is not None:
            job_set.add(x.job_id.id)
        if x.emp_id is not None:
            emp_set.add(x.emp_id.id)
    filtered_emps = JobRoll.objects.filter(
        (
                Q(position__department__id__in=dept_set) |
                Q(position__id__in=position_set) |
                Q(position__job__id__in=job_set) |
                Q(emp_id__id__in=emp_set))
    )
    for emp in filtered_emps:
        included_emps.add(emp.emp_id.id)
    return included_emps


# @login_required(login_url='home:user-login')
def excludeAssignmentEmployeeFunction(batch):
    excluded_emps = set()
    assignment_batch = Assignment_Batch.objects.get(id=batch.id)
    exclude_query = Assignment_Batch_Exclude.objects.filter(exclude_batch_id=assignment_batch).exclude(
        (Q(end_date__gte=date.today()) | Q(end_date__isnull=False)))
    dept_set = set()
    job_set = set()
    position_set = set()
    emp_set = set()
    for x in exclude_query:
        if x.dept_id is not None:
            dept_set.add(x.dept_id.id)
        if x.position_id is not None:
            position_set.add(x.position_id.id)
        if x.job_id is not None:
            job_set.add(x.job_id.id)
        if x.emp_id is not None:
            emp_set.add(x.emp_id.id)
    filtered_emps = JobRoll.objects.filter(
        (
                Q(position__department__id__in=dept_set) |
                Q(position__id__in=position_set) |
                Q(position__job__id__in=job_set) |
                Q(emp_id__id__in=emp_set))
    )
    for emp in filtered_emps:
        excluded_emps.add(emp.emp_id.id)
    return excluded_emps


@login_required(login_url='home:user-login')
def createSalaryView(request):
    sal_form = SalaryElementForm(user=request.user)
    employees_dont_have_structurelink = []
    employees = 0
    if request.method == 'POST':
        sal_form = SalaryElementForm(request.POST, user=request.user)
        if sal_form.is_valid():
            sal_obj = sal_form.save(commit=False)
            element = None
            # run employee on all emps.
            if sal_obj.elements_type_to_run == 'appear':
                elements = Employee_Element.objects.filter(element_id__appears_on_payslip=True).filter(
                    (Q(start_date__lte=date.today()) & (
                            Q(end_date__gt=date.today()) | Q(end_date__isnull=True)))).values('element_id')
            else:
                elements = Employee_Element.objects.filter(element_id=sal_obj.element).filter(
                    Q(start_date__lte=date.today()) & (
                        (Q(end_date__gt=date.today()) | Q(end_date__isnull=True)))).values('element_id')
                if len(elements) != 0:
                    element = Element.objects.get(id=elements[0]['element_id'])
            if sal_obj.assignment_batch is not None:
                emps = Employee.objects.filter(
                    id__in=includeAssignmentEmployeeFunction(
                        sal_obj.assignment_batch)).exclude(
                    id__in=excludeAssignmentEmployeeFunction(
                        sal_obj.assignment_batch))
            else:
                emps = Employee.objects.filter(
                    (Q(end_date__gt=date.today()) | Q(end_date__isnull=True)))
            # TODO: review the include and exclude assignment batch
            for x in emps:
                emp_elements = Employee_Element.objects.filter(element_id__in=elements, emp_id=x).values('element_id')
                sc = Salary_Calculator(company=request.user.company, employee=x, elements=emp_elements)
                # calculate all furmulas elements for 'x' employee
                # Employee_Element.set_formula_amount(x)
                try:
                    emp = EmployeeStructureLink.objects.get(employee=x)
                    structure = emp.salary_structure.structure_type
                    #print(structure)
                    if structure == 'Gross to Net' :
                        s = Salary_elements(
                            emp=x,
                            elements_type_to_run=sal_obj.elements_type_to_run,
                            salary_month=sal_obj.salary_month,
                            salary_year=sal_obj.salary_year,
                            run_date=sal_obj.run_date,
                            created_by=request.user,
                            incomes=sc.calc_emp_income(),
                            element=element,
                            insurance_amount=sc.calc_employee_insurance(),
                            # TODO need to check if the tax is applied
                            tax_amount=sc.calc_taxes_deduction(),
                            deductions=sc.calc_emp_deductions_amount(),
                            gross_salary=sc.calc_gross_salary(),
                            net_salary=sc.calc_net_salary(),

                        )
                    else :
                        
                        s = Salary_elements(
                            emp=x,
                            elements_type_to_run=sal_obj.elements_type_to_run,
                            salary_month=sal_obj.salary_month,
                            salary_year=sal_obj.salary_year,
                            run_date=sal_obj.run_date,
                            created_by=request.user,
                            incomes=sc.calc_emp_income(),
                            element=element,
                            insurance_amount=sc.calc_employee_insurance(),
                            # TODO need to check if the tax is applied
                            tax_amount=sc.net_to_tax(),
                            deductions=sc.calc_emp_deductions_amount(),
                            gross_salary=sc.net_to_gross(),
                            net_salary=sc.calc_basic_net(),
                        )
                                
                    s.save()
                except Exception as e: 
                    employees_dont_have_structurelink.append(x.emp_name)
                    employees =  ', '.join(employees_dont_have_structurelink) + ': dont have structurelink, add structurelink to them'
                #gross= sc.net_to_gross()
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم تشغيل راتب شهر {} بنجاح'.format(
                    calendar.month_name[sal_obj.salary_month])

            else:
                success_msg = 'Payroll for month {} done successfully'.format(
                    calendar.month_name[sal_obj.salary_month] ) 
            messages.success(request, success_msg)
            # # the user select element batch to run on without assignment batch.
            # elif sal_obj.element_batch and sal_obj.assignment_batch == None:
            #     elements_in_batch = get_list_or_404(
            #         ElementBatchMaster, element_batch_fk=sal_obj.element_batch)
            #     emp_in_batch = Employee_Element.objects.filter(
            #         element_id__elementMaster__in=elements_in_batch)
            #     emps = set()
            #     for x in emp_in_batch:
            #         emps.add(x.emp_id)
            #     for x in emps:
            #         sc = Salary_Calculator(company=request.user.company, employee=x)
            #         # calculate all formulas elements for 'x' employee
            #         # Employee_Element.set_formula_amount(x)
            #         # # ################################################
            #         # # # getting informations for the salary
            #         s = Salary_elements(
            #             emp=x,
            #             salary_month=sal_obj.salary_month,
            #             salary_year=sal_obj.salary_year,
            #             run_date=sal_obj.run_date,
            #             created_by=request.user,
            #             incomes=sc.calc_emp_income(),
            #             insurance_amount=sc.calc_employee_insurance(),
            #             tax_amount=sc.calc_taxes_deduction(),
            #             deductions=sc.calc_emp_deductions_amount(),
            #             gross_salary=sc.calc_gross_salary(),
            #             net_salary=sc.calc_net_salary(),
            #         )
            #         s.save()
            #     user_lang = to_locale(get_language())
            #     if user_lang == 'ar':
            #         success_msg = 'تم تشغيل الراتب بنجاح {} '.format(
            #             sal_obj.salary_month)
            #     else:
            #         success_msg = 'Payroll for month {} done successfully'.format(
            #             sal_obj.salary_month)
            #     messages.success(request, success_msg)
            # # the user select assignment batch without element batch to run on.
            # elif sal_obj.assignment_batch and sal_obj.element_batch == None:
            #     emps = Employee.objects.filter(
            #         id__in=includeAssignmentEmployeeFunction(
            #             sal_obj.assignment_batch)).exclude(
            #         id__in=excludeAssignmentEmployeeFunction(
            #             sal_obj.assignment_batch))
            #     for x in emps:
            #         # calculate all furmulas elements for 'x' employee
            #         # Employee_Element.set_formula_amount(x)
            #         sc = Salary_Calculator(company=request.user.company, employee=x)
            #         # # # getting informations for the salary
            #         s = Salary_elements(
            #             emp=x,
            #             salary_month=sal_obj.salary_month,
            #             salary_year=sal_obj.salary_year,
            #             run_date=sal_obj.run_date,
            #             created_by=request.user,
            #             incomes=sc.calc_emp_income(),
            #             insurance_amount=sc.calc_employee_insurance(),
            #             tax_amount=sc.calc_taxes_deduction(),
            #             deductions=sc.calc_emp_deductions_amount(),
            #             gross_salary=sc.calc_gross_salary(),
            #             net_salary=sc.calc_net_salary(),
            #         )
            #         s.save()
            #     user_lang = to_locale(get_language())
            #     if user_lang == 'ar':
            #         success_msg = 'تم تشغيل الراتب بنجاح {} '.format(
            #             sal_obj.salary_month)
            #     else:
            #         success_msg = 'Payroll for month {} done successfully'.format(
            #             sal_obj.salary_month)
            #     messages.success(request, success_msg)
            # # the user select both assignment batch and element batch to run on.
            # elif sal_obj.assignment_batch and sal_obj.element_batch:
            #     all_emps = set()
            #     emp_in_assignment = Employee.objects.filter(
            #         id__in=includeAssignmentEmployeeFunction(
            #             sal_obj.assignment_batch)).exclude(
            #         id__in=excludeAssignmentEmployeeFunction(
            #             sal_obj.assignment_batch))
            #     for emp in emp_in_assignment:
            #         all_emps.add(emp)
            #     elements_in_batch = get_list_or_404(
            #         ElementBatchMaster, element_batch_fk=sal_obj.element_batch)
            #     emp_in_element_batch = Employee_Element.objects.filter(
            #         element_id__elementMaster__in=elements_in_batch)
            #     for emp in emp_in_element_batch:
            #         all_emps.add(x.emp_id)
            #     for x in all_emps:
            #         # calculate all furmulas elements for 'x' employee
            #         Employee_Element.set_formula_amount(x)
            #         sc = Salary_Calculator(company=request.user.company, employee=x)
            #         # # # getting informations for the salary
            #         s = Salary_elements(
            #             emp=x,
            #             salary_month=sal_obj.salary_month,
            #             salary_year=sal_obj.salary_year,
            #             run_date=sal_obj.run_date,
            #             created_by=request.user,
            #             incomes=sc.calc_emp_income(),
            #             insurance_amount=sc.calc_employee_insurance(),
            #             tax_amount=sc.calc_taxes_deduction(),
            #             deductions=sc.calc_emp_deductions_amount(),
            #             gross_salary=sc.calc_gross_salary(),
            #             net_salary=sc.calc_net_salary(),
            #         )
            #         s.save()
            #     user_lang = to_locale(get_language())
            #     if user_lang == 'ar':
            #         success_msg = 'تم تشغيل الراتب بنجاح {} '.format(
            #             sal_obj.salary_month)
            #     else:
            #         success_msg = 'Payroll for month {} done successfully'.format(
            #             sal_obj.salary_month)
            #     messages.success(request, success_msg)

    else:  # Form was not valid
        messages.error(request, sal_form.errors)
    salContext = {
        'page_title': _('create salary'),
        'sal_form': sal_form,
        'employees' :employees,
    }
    return render(request, 'create-salary.html', salContext)


def month_name(month_number):
    return calendar.month_name[month_number]


@login_required(login_url='home:user-login')
def listSalaryFromMonth(request, month, year):
    salaries_list = Salary_elements.objects.filter(
        salary_month=month, salary_year=year)
    monthSalaryContext = {
        'page_title': _('salaries for month {}').format(month_name(month)),
        'salaries_list': salaries_list,
        'v_month': month,
        'v_year': year
    }
    return render(request, 'list-salary-month.html', monthSalaryContext)


@login_required(login_url='home:user-login')
def changeSalaryToFinal(request, month, year):
    draft_salary = Salary_elements.objects.filter(
        salary_month=month, salary_year=year)
    for draft in draft_salary:
        draft.is_final = True
        draft.save()
    return redirect('payroll_run:list-salary')


@login_required(login_url='home:user-login')
def userSalaryInformation(request, month_number, salary_year, salary_id, emp_id , tmp_format):
    salary_obj = get_object_or_404(
        Salary_elements,
        salary_month=month_number,
        salary_year=salary_year,
        pk=salary_id
    )
    appear_on_payslip = salary_obj.elements_type_to_run
    if appear_on_payslip == 'appear':

        elements = Employee_Element.objects.filter(element_id__appears_on_payslip=True).filter(
            (Q(start_date__lte=date.today()) & (
                    Q(end_date__gt=salary_obj.run_date) | Q(end_date__isnull=True)))).values('element_id')
    else:
        elements = Employee_Element.objects.filter(element_id__id=salary_obj.element.id,
                                                   element_id__appears_on_payslip=False).filter(
            (Q(start_date__lte=date.today()) & (
                    Q(end_date__gt=salary_obj.run_date) | Q(end_date__isnull=True)))).values('element_id')

    emp_elements_incomes = Employee_Element.objects.filter(
        element_id__in=elements,
        emp_id=emp_id,
        element_id__classification__code='earn',

    ).order_by('element_id__sequence')
    emp_elements_deductions = Employee_Element.objects.filter(element_id__in=elements, emp_id=emp_id,
                                                              element_id__classification__code='deduct',
                                                              ).order_by('element_id__sequence')
    emp_payment = Payment.objects.filter((Q(end_date__gte=date.today()) | Q(end_date__isnull=True)), emp_id=emp_id)
    monthSalaryContext = {
        'page_title': _('salary information for {}').format(salary_obj.emp),
        'salary_obj': salary_obj,
        'emp_elements_incomes': emp_elements_incomes,
        'emp_elements_deductions': emp_elements_deductions,
        'emp_payment': emp_payment,
    }
    # emp_elements = Employee_Element.objects.filter(emp_id=emp_id).values('element_id')

    # sc = Salary_Calculator(company=request.user.company, employee=emp_id, elements=emp_elements)
    # test = sc.calc_emp_deductions_amount()
    if tmp_format=="table":
        return render(request, 'emp-payslip.html', monthSalaryContext)
    elif tmp_format=="list":
        return render(request, 'emp-payslip-report.html', monthSalaryContext)


@login_required(login_url='home:user-login')
def render_emp_payslip(request, month, year, salary_id, emp_id):
    template_path = 'payslip.html'
    salary_obj = get_object_or_404(
        Salary_elements, salary_month=month, salary_year=year, pk=salary_id)
    emp_elements = Employee_Element.objects.filter(emp_id=emp_id)
    context = {
        'salary_obj': salary_obj,
        'emp_elements': emp_elements,
        'company_name': request.user.company,
    }
    response = HttpResponse(content_type="application/pdf")
    response[
        'Content-Disposition'] = "inline; filename={date}-donation-receipt.pdf".format(
        date=date.today().strftime('%Y-%m-%d'), )
    html = render_to_string(template_path, context)
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response


@login_required(login_url='home:user-login')
def render_all_payslip(request, month, year):
    template_path = 'all-payslip.html'
    all_salary_obj = get_list_or_404(
        Salary_elements, salary_month=month, salary_year=year)
    new_thing = {}
    for sal in all_salary_obj:
        emp_elements = Employee_Element.objects.filter(emp_id=sal.emp.id)
        new_thing['emp_salary'] = sal
        new_thing['emp_elements'] = emp_elements
    context = {
        'all_salary_obj': all_salary_obj,
        'emp_elements': new_thing['emp_elements'],
        'company_name': request.user.company,
    }
    response = HttpResponse(content_type="application/pdf")
    response[
        'Content-Disposition'] = "inline; filename={date}-donation-receipt.pdf".format(
        date=date.today().strftime('%Y-%m-%d'), )
    html = render_to_string(template_path, context)
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response


@login_required(login_url='home:user-login')
def delete_salary_view(request, month, year):
    required_salary = Salary_elements.objects.filter(salary_month=month, salary_year=year)
    for sal in required_salary:
        sal.end_date = date.today()
        sal.save()
    return redirect('payroll_run:list-salary')
