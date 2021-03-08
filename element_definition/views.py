from django.shortcuts import render, get_object_or_404, reverse, redirect , HttpResponse
from django.contrib import messages
from django.core import management
from datetime import date
from django.db.models import Q
from django.core.management import call_command
from django.utils.translation import to_locale, get_language
from django.core.management.commands import loaddata
from company.models import Department, Grade, Position, Job
from element_definition.forms import (ElementMasterForm, ElementMasterInlineFormset, ElementBatchForm,
                                      ElementLinkForm, CustomPythonRuleForm, ElementForm, SalaryStructureForm,
                                      ElementInlineFormset)
from element_definition.models import (
    Element_Batch, Element_Master, Element_Batch_Master, Element_Link, Element, SalaryStructure, StructureElementLink)
from employee.models import Employee, Employee_Element, JobRoll, EmployeeStructureLink
from manage_payroll.models import Payroll_Master
from defenition.models import LookupDet
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import to_locale, get_language
from payroll_run.payslip_functions import PayslipFunction
from django.http import JsonResponse
import unicodedata


################################################################################
'''
    Element_Master is not used in models, views and forms
    TODO delete Element_Master
'''


def installElementMaster(request):
    element_type_obj = LookupDet.objects.get(id=7)
    element_class_obj = LookupDet.objects.get(id=9)
    user_lang = to_locale(get_language())
    if user_lang == 'ar':
        element_name = 'الأساسي'
    else:
        element_name = 'Basic'
    company_basic_db_name = str(request.user.company.id) + '00001'
    basic_element = Element_Master(
        enterprise=request.user.company,
        element_name=element_name,
        db_name=company_basic_db_name,
        basic_flag=True,
        element_type=element_type_obj,
        classification=element_class_obj,
        retro_flag=0,
        tax_flag=1,
        start_date=date.today(),
        created_by=request.user,
        creation_date=date.today(),
        last_update_date=date.today()
    )
    basic_element.save()
    return redirect('element_definition:list-element')


######################################## Element view functions ##################################################


def getDBSec(n, company_id):
    if n < 1:
        return str(company_id) + str(1).zfill(3)
    else:
        return str(company_id) + str(n + 1).zfill(3)


def generate_element_code(word):
    '''
        generate code based on word to use it in element-code "called in create_new_element"
        author: Mamdouh
        created_at: 08/03/2021
    '''
    ar_string = ''
    for c in word:
        id = unicodedata.name(c).lower()
        if 'arabic letter' in id:
            ar_string += id.split()[2][0]
        if 'space' in id:
            ar_string += '-'
        if 'latin' in id:
            ar_string += c
    return ar_string

def create_new_element(request):
    element_form = ElementForm(user=request.user)
    rows_number = Element_Master.objects.all().count()
    if request.method == "POST":
        user_lang = to_locale(get_language())
        element_form = ElementForm(request.POST, user=request.user)
        if element_form.is_valid():
            elem_obj = element_form.save(commit=False)
            element_code = getDBSec(
                    rows_number, request.user.company.id) + '-' + generate_element_code(elem_obj.element_name)
            elem_obj.code = element_code
            elem_obj.created_by = request.user
            elem_obj.enterprise = request.user.company
            elem_obj.save()
            success_msg = make_message(user_lang, True)
            messages.success(request, success_msg)
            return redirect('element_definition:list-element')
        else:
            failure_msg = make_message(user_lang, False)
            messages.error(request, failure_msg)
            print(element_form.errors)

    myContext = {
        "page_title": _("Create new Pay"),
        'element_master_form': element_form,
    }
    return render(request, 'create-element2.html', myContext)



def make_message(user_lang, success):
    if success:
        if user_lang == 'ar':
            msg = 'تمت العملية بنجاح'
        else:
            msg = 'Create Successfully'
    else:
        if user_lang == 'ar':
            msg = 'لم يتم الانشاء بنجاح'
        else:
            msg = 'The form is not valid.'
    return msg

def update_element_view(request, pk):
    element = get_object_or_404(Element, pk=pk)
    element_master_form = ElementForm(instance=element, user=request.user)
    if request.method == 'POST':
        user_lang = to_locale(get_language())
        element_master_form = ElementForm(
            request.POST, instance=element, user=request.user)
        if element_master_form.is_valid():
            element_obj = element_master_form.save(commit=False)
            element_obj.last_update_by = request.user
            element_obj.save()
            success_msg = make_message(user_lang, True)
            messages.success(request, success_msg)
            return redirect('element_definition:list-element')
        else:
            failure_msg = make_message(user_lang, False)
            messages.error(request, failure_msg)
            print(element_master_form.errors)

    myContext = {
        "page_title": _("Update Element"),
        'element_master_form': element_master_form,
    }
    return render(request, 'create-element2.html', myContext)


def delete_element_view(request, pk):
    required_element = get_object_or_404(Element, pk=pk)
    required_element.end_date = date.today()
    required_element.save(update_fields=['end_date'])
    success_msg = '{} was deleted successfully'.format(required_element)
    messages.success(request, success_msg)
    return redirect('element_definition:list-element')


def list_elements_view(request):
    if request.method == 'GET':
        element_master = Element.objects.filter(enterprise=request.user.company).filter(
            (Q(end_date__gt=date.today()) | Q(end_date__isnull=True)))
        company_basic_db_name = str(request.user.company.id) + '00001'

    myContext = {
        'page_title': _('Pays'),
        'element_master': element_master,
    }
    return render(request, 'backup_list-elements.html', myContext)


def list_salary_structures(request):
    structure_list = SalaryStructure.objects.all().filter(
        (Q(end_date__gt=date.today()) | Q(end_date__isnull=True)))
    context = {
        "page_title": _("Salary Structures"),
        'structure_list': structure_list,
    }
    return render(request, 'backup_list-salary-structures.html', context)


def listElementView(request):
    if request.method == 'GET':
        element_flag = False
        element_master = Element_Master.objects.filter(enterprise=request.user.company).filter(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        company_basic_db_name = str(request.user.company.id) + '00001'
        for x in element_master:
            if x.db_name == company_basic_db_name and x.enterprise == request.user.company:
                element_flag = True
    myContext = {
        'page_title': _('Pays'),
        'element_master': element_master,
        'basic_flag': element_flag,
    }
    return render(request, 'list-elements.html', myContext)


######################################## ElementBatch view functions ##################################################


def listElementBatchView(request):
    batch_link = Element_Batch_Master.objects.all().filter(
        (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
    batch_list = Element_Batch.objects.all().filter(
        (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
    batchContext = {
        "page_title": _("batch list"),
        'batch_list': batch_list,
        'batch_link': batch_link
    }
    return render(request, 'list-batchs.html', batchContext)


def createElementBatchView(request):
    batch_form = ElementBatchForm()
    batch_form.fields['payroll_fk'].queryset = Payroll_Master.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    batch_detail_form = ElementMasterInlineFormset()
    for form in batch_detail_form:
        form.fields['element_master_fk'].queryset = Element_Master.objects.filter(
            enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    if request.method == 'POST':
        batch_form = ElementBatchForm(request.POST)
        batch_detail_form = ElementMasterInlineFormset(request.POST)
        if batch_form.is_valid():
            obj_master = batch_form.save(commit=False)
            obj_master.created_by = request.user
            obj_master.last_update_by = request.user
            obj_master.save()
            batch_detail_form = ElementMasterInlineFormset(
                request.POST, instance=obj_master)
            if batch_detail_form.is_valid():
                obj_det = batch_detail_form.save(commit=False)
                for obj in obj_det:
                    obj.created_by = request.user
                    obj.last_update_by = request.user
                    obj.save()
                success_msg = 'Batch {} created Successfully'.format(
                    obj_master)
                messages.success(request, success_msg)
                return redirect('element_definition:list-batchs')
        else:
            messages.success(request, batch_form.errors)
            messages.success(request, batch_detail_form.errors)
    batchContext = {
        "page_title": _("Create Pay Batch"),
        'batch_form': batch_form,
        'batch_detail_form': batch_detail_form
    }
    return render(request, 'create-batch.html', batchContext)


def create_salary_structure_with_elements_view(request):
    structure_form = SalaryStructureForm()
    elements_inlines = ElementInlineFormset(form_kwargs={'user': request.user})
    if request.method == 'POST':
        structure_form = SalaryStructureForm(request.POST)
        elements_inlines = ElementInlineFormset(
            request.POST, form_kwargs={'user': request.user})
        if structure_form.is_valid():
            structure_obj = structure_form.save(commit=False)
            structure_obj.created_by = request.user
            structure_obj.enterprise = request.user.company
            structure_obj.save()
            elements_inlines = ElementInlineFormset(
                request.POST, instance=structure_obj, form_kwargs={'user': request.user})
            if elements_inlines.is_valid():
                elements_objs = elements_inlines.save(commit=False)
                for elements_obj in elements_objs:
                    elements_obj.created_by = request.user
                    elements_obj.save()
                return redirect('element_definition:list-batchs')
            else:
                print(elements_inlines.errors)
        else:
            print(structure_form.errors)
    context = {'page_title': "New Salary Structure", 'structure_form': structure_form,
               'elements_inlines': elements_inlines}
    return render(request, 'backup_create-salary-structure.html', context=context)


def update_salary_structure_with_elements_view(request, pk):
    structure_instance = SalaryStructure.objects.get(pk=pk)
    structure_form = SalaryStructureForm(instance=structure_instance)
    list_of_active_links = StructureElementLink.objects.filter(salary_structure=structure_instance).filter(
        Q(end_date__gt=date.today()) | Q(end_date__isnull=True))
    elements_inlines = ElementInlineFormset(
        instance=structure_instance, queryset=list_of_active_links, form_kwargs={'user': request.user})
    if request.method == 'POST':
        structure_form = SalaryStructureForm(
            request.POST, instance=structure_instance)
        elements_inlines = ElementInlineFormset(
            request.POST, instance=structure_instance, form_kwargs={'user': request.user})
        if structure_form.is_valid() and elements_inlines.is_valid():
            structure_obj = structure_form.save(commit=False)
            structure_obj.last_update_by = request.user
            structure_obj.save()
            elements_inlines = ElementInlineFormset(
                request.POST, instance=structure_obj, form_kwargs={'user': request.user})
            if elements_inlines.is_valid():
                obj_det = elements_inlines.save(commit=False)
                for obj in obj_det:
                    obj.created_by = (
                        request.user if obj.pk is None else obj.created_by)
                    obj.last_update_by = request.user
                    obj.save()
                success_msg = 'Salary structure {} updated Successfully'.format(
                    structure_obj.structure_name)
            messages.success(request, success_msg)
            return redirect('element_definition:list-batchs')
        else:
            messages.error(request, structure_form.errors)
            messages.error(request, elements_inlines.errors)
    context = {
        "page_title": _("Update Salary Structure"),
        'structure_form': structure_form,
        'elements_inlines': elements_inlines
    }
    return render(request, 'backup_create-salary-structure.html', context=context)


def delete_salary_structure_with_elements_view(request, pk):
    required_salary_structure = get_object_or_404(SalaryStructure, pk=pk)
    try:

        required_salary_structure.end_date = date.today()
        required_salary_structure.save(update_fields=['end_date'])
        required_linked_elements = StructureElementLink.objects.filter(
            salary_structure=required_salary_structure).filter(
            Q(end_date__isnull=True) | Q(end_date__gt=date.today()))
        required_employee_elements = Employee_Element.objects.filter(
            element_id__in=required_linked_elements.values('element')).filter(
            Q(end_date__isnull=True) | Q(end_date__gt=date.today()))
        required_employee_structure = EmployeeStructureLink.objects.filter(
            salary_structure=required_salary_structure).filter(Q(end_date__isnull=True) | Q(end_date__gt=date.today()))

        for x in required_linked_elements:
            x.end_date = date.today()
            x.save(update_fields=['end_date'])
        for z in required_employee_structure:
            z.end_date = date.today()
            z.save(update_fields=['end_date'])
        for y in required_employee_elements:
            y.delete()

        success_msg = '{} was deleted successfully'.format(
            required_salary_structure)
        messages.success(request, success_msg)
    except Exception as e:
        error_msg = '{} cannot be deleted '.format(required_salary_structure)
        messages.error(request, error_msg)
        raise e
    return redirect('element_definition:list-batchs')


def updateElementBatchView(request, pk):
    batch_instance = Element_Batch.objects.get(pk=pk)
    batch_form = ElementBatchForm(instance=batch_instance)
    batch_form.fields['payroll_fk'].queryset = Payroll_Master.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    batch_det_instance = Element_Batch_Master.objects.filter(
        element_batch_fk=pk)
    batch_detail_form = ElementMasterInlineFormset(instance=batch_instance)
    for form in batch_detail_form:
        form.fields['element_master_fk'].queryset = Element_Master.objects.filter(
            enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    if request.method == 'POST':
        batch_form = ElementBatchForm(request.POST, instance=batch_instance)
        batch_detail_form = ElementMasterInlineFormset(
            request.POST, instance=batch_instance)
        if batch_form.is_valid() and batch_detail_form.is_valid():
            batch_obj = batch_form.save(commit=False)
            batch_obj.created_by = request.user
            batch_obj.last_update_by = request.user
            batch_obj.save()
            batch_detail_form = ElementMasterInlineFormset(
                request.POST, instance=batch_obj)
            if batch_detail_form.is_valid():
                obj_det = batch_detail_form.save(commit=False)
                for obj in obj_det:
                    obj.created_by = request.user
                    obj.last_update_by = request.user
                    obj.save()
            success_msg = 'Batch {} updated Successfully'.format(
                batch_obj.batch_name)
            messages.success(request, success_msg)
            return redirect('element_definition:list-batchs')
        else:
            messages.warning(request, batch_form.errors)
            messages.warning(request, batch_detail_form.errors)
    batchContext = {
        "page_title": _("Update Batch"),
        'batch_form': batch_form,
        'batch_detail_form': batch_detail_form
    }
    return render(request, 'create-batch.html', batchContext)


def deleteElementBatchView(request, pk):
    required_batch = get_object_or_404(Element_batch, pk=pk)
    try:
        batch_form = ElementBatchForm(instance=required_batch)
        batch_obj = batch_form.save(commit=False)
        batch_obj.end_date = date.today()
        batch_det_form = ElementMasterInlineFormset(instance=required_batch)
        batch_det_obj = batch_det_form.save(commit=False)
        for x in batch_det_obj:
            x.end_date = date.today()
            x.save(update_fields=['end_date'])
        batch_obj.save(update_fields=['end_date'])
        success_msg = '{} was deleted successfully'.format(required_batch)
        messages.success(request, success_msg)
    except Exception as e:
        error_msg = '{} cannot be deleted '.format(required_batch)
        messages.error(request, error_msg)
        raise e
    return redirect('element_definition:list-batchs')


######################################## ElementLink view functions ##################################################


def linkElementToEmps(link_to_all=False, payroll_v=None, dept_v=None,
                      job_v=None, grade_v=None, position_v=None,
                      element_id=None, global_v=0, user_id=None):
    if link_to_all == True:
        all_emps = Employee.objects.all().filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    elif payroll_v != None:
        all_emps = JobRoll.objects.filter(payroll=payroll_v).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    elif dept_v != None:
        all_emps = JobRoll.objects.filter(department=dept_v).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    elif job_v != None:
        all_emps = JobRoll.objects.filter(job_name=job_v).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    elif grade_v != None:
        all_emps = JobRoll.objects.filter(grade=grade_v).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    elif position_v != None:
        all_emps = JobRoll.objects.filter(position=position_v).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))

    for emp in all_emps:
        emp_element = Employee_Element(
            emp_id=(emp if link_to_all == True else emp.emp_id),
            element_id=element_id,
            element_value=global_v,
            created_by=user_id,
            last_update_by=user_id,
        )
        emp_element.save()


def linkElementsInBatchToTmps(link_to_all=False, payroll_v=None, dept_v=None,
                              job_v=None, grade_v=None, position_v=None,
                              batch_v=None, user_id=None):
    element_qset = Element_Batch_Master.objects.filter(
        element_batch_fk=batch_v)
    for x in element_qset:
        linkElementToEmps(link_to_all=link_to_all, payroll_v=payroll_v, dept_v=dept_v,
                          job_v=job_v, grade_v=grade_v, position_v=position_v,
                          element_id=x.element_master_fk, global_v=x.element_master_fk.fixed_amount,
                          user_id=user_id)


def listElementLinkView(request):
    list_links = Element_Link.objects.filter(Q(element_master_fk__enterprise=request.user.company)
                                             | Q(batch__payroll_fk__enterprise=request.user.company)).filter(
        Q(end_date__gte=date.today()) | Q(end_date__isnull=True)
    )
    linkContext = {
        "page_title": _("link Pays"),
        'list_links': list_links
    }
    return render(request, 'list-links.html', linkContext)


def createElementLinkView(request):
    link_form = ElementLinkForm()
    link_form.fields['element_master_fk'].queryset = Element_Master.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['batch'].queryset = Element_Batch.objects.filter(
        payroll_fk__enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['payroll_fk'].queryset = Payroll_Master.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['element_dept_id_fk'].queryset = Department.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['element_job_id_fk'].queryset = Job.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['element_grade_fk'].queryset = Grade.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['element_position_id_fk'].queryset = Position.objects.filter(
        department__enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['employee'].queryset = Employee.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))

    if request.method == 'POST':
        link_form = ElementLinkForm(request.POST)
        if link_form.is_valid():
            element_link_obj = link_form.save(commit=False)
            element_link_obj.created_by = request.user
            element_link_obj.last_update_by = request.user
            if element_link_obj.element_master_fk:  # select element not batch to link
                if element_link_obj.link_to_all_payroll_flag:
                    linkElementToEmps(link_to_all=True,
                                      element_id=element_link_obj.element_master_fk,
                                      global_v=element_link_obj.element_master_fk.fixed_amount,
                                      user_id=request.user)
                elif element_link_obj.payroll_fk != None:
                    linkElementToEmps(payroll_v=element_link_obj.payroll_fk,
                                      element_id=element_link_obj.element_master_fk,
                                      global_v=element_link_obj.element_master_fk.fixed_amount,
                                      user_id=request.user)
                elif element_link_obj.element_dept_id_fk != None:
                    linkElementToEmps(dept_v=element_link_obj.element_dept_id_fk,
                                      element_id=element_link_obj.element_master_fk,
                                      global_v=element_link_obj.element_master_fk.fixed_amount,
                                      user_id=request.user)
                elif element_link_obj.element_job_id_fk != None:
                    linkElementToEmps(job_v=element_link_obj.element_job_id_fk,
                                      element_id=element_link_obj.element_master_fk,
                                      global_v=element_link_obj.element_master_fk.fixed_amount,
                                      user_id=request.user)
                elif element_link_obj.element_grade_fk != None:
                    linkElementToEmps(grade_v=element_link_obj.element_grade_fk,
                                      element_id=element_link_obj.element_master_fk,
                                      global_v=element_link_obj.element_master_fk.fixed_amount,
                                      user_id=request.user)
                elif element_link_obj.element_position_id_fk != None:
                    linkElementToEmps(position_v=element_link_obj.element_position_id_fk,
                                      element_id=element_link_obj.element_master_fk,
                                      global_v=element_link_obj.element_master_fk.fixed_amount,
                                      user_id=request.user)
            else:  # select batch not one element to link
                if element_link_obj.link_to_all_payroll_flag:
                    linkElementsInBatchToTmps(link_to_all=True,
                                              batch_v=element_link_obj.batch,
                                              user_id=request.user)
                elif element_link_obj.payroll_fk != None:
                    linkElementsInBatchToTmps(payroll_v=element_link_obj.payroll_fk,
                                              batch_v=element_link_obj.batch,
                                              user_id=request.user)
                elif element_link_obj.element_dept_id_fk != None:
                    linkElementsInBatchToTmps(dept_v=element_link_obj.element_dept_id_fk,
                                              batch_v=element_link_obj.batch,
                                              user_id=request.user)
                elif element_link_obj.element_job_id_fk != None:
                    linkElementsInBatchToTmps(job_v=element_link_obj.element_job_id_fk,
                                              batch_v=element_link_obj.batch,
                                              user_id=request.user)
                elif element_link_obj.element_grade_fk != None:
                    linkElementsInBatchToTmps(grade_v=element_link_obj.element_grade_fk,
                                              batch_v=element_link_obj.batch,
                                              user_id=request.user)
                elif element_link_obj.element_position_id_fk != None:
                    linkElementsInBatchToTmps(position_v=element_link_obj.element_position_id_fk,
                                              batch_v=element_link_obj.batch,
                                              user_id=request.user)

            element_link_obj.save()
            if 'add_next' in request.POST:
                success_msg = 'تم اضافة "{}" بنجاح'.format(element_link_obj)
                messages.success(request, success_msg)
                return redirect('element_definition:link-create')
            else:
                success_msg = 'تم اضافة "{}" بنجاح'.format(element_link_obj)
                messages.success(request, success_msg)
                return redirect('element_definition:list-links')
        else:
            # Spitting the errors coming from the form
            [messages.error(request, error[0])
             for error in form.errors.values()]
    linkContext = {
        "page_title": _("Create Pay Link"),
        'link_form': link_form}
    return render(request, 'create-element-link.html', linkContext)


def updateElementLinkView(request, pk):
    required_link = get_object_or_404(Element_Link, pk=pk)
    link_form = ElementLinkForm(instance=required_link)
    link_form.fields['element_master_fk'].queryset = Element_Master.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['batch'].queryset = Element_Batch.objects.filter(
        payroll_fk__enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['payroll_fk'].queryset = Payroll_Master.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['element_dept_id_fk'].queryset = Department.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['element_job_id_fk'].queryset = Job.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['element_grade_fk'].queryset = Grade.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['element_position_id_fk'].queryset = Position.objects.filter(
        department__enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    link_form.fields['employee'].queryset = Employee.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))

    if request.method == 'POST':
        link_form = ElementLinkForm(request.POST, instance=required_link)
        if link_form.is_valid():
            element_link_obj = link_form.save()
            success_msg = '{} updated successfully'.format(element_link_obj)
            messages.success(request, success_msg)
            return redirect('element_definition:list-links')
    linkContext = {
        "page_title": _("Update Pay Link"),
        'link_form': link_form}
    return render(request, 'create-element-link.html', linkContext)


def deleteElementLinkView(request, pk):
    required_link = get_object_or_404(Element_Link, pk=pk)
    # if required_link.batch:
    #
    # Employee_Element.objects.filter()
    # try:
    #     link_form = ElementLinkForm(user_v=request.user, instance=required_link)
    #     link_obj = link_form.save(commit=False)
    #     link_obj.end_date = date.today()
    #     link_obj.save(update_fields=['end_date'])
    #     success_msg = '{} was deleted successfully'.format(required_link)
    #     messages.success(request, success_msg)
    # except Exception as e:
    #     error_msg = '{} cannot be deleted '.format(required_link)
    #     messages.error(request, error_msg)
    #     raise e
    required_link.delete()
    return redirect('element_definition:list-links')


#######################################Custom Rule###################################################


def customRulesView(request):
    custom_rule_form = CustomPythonRuleForm()
    if request.method == "POST":
        custom_rule_form = CustomPythonRuleForm(request.POST)
        if form.is_valid():
            custom_rule = form.save()
            success_msg = 'تم اضافة "{}" بنجاح'.format(custom_rule.name)
            messages.success(request, success_msg)
            # # Emptying the form before rerendering it back
            # form = CustomPythonRuleForm()
        else:  # Form was not valid
            # Spitting the errors coming from the form
            [messages.error(request, error[0])
             for error in form.errors.values()]
    else:  # Request is GET
        # Just passing an empty form to be rendered in case of GET
        custom_rule_form = CustomPythonRuleForm()
    context = {'table_title': 'قواعد الاحتساب المخصصة',
               'modal_title': 'اضافة قاعدة جديدة', 'custom_rule_form': custom_rule_form}
    # Finally, and In all the cases, we will always render the same page to the user
    return render(request, 'custom-formula.html', context=context)


def delete_custom_rule(request, pk):
    required_rule = get_object_or_404(Custom_Python_Rule, pk=pk)
    try:
        rule_form = CustomPythonRuleForm(instance=required_rule)
        rule_obj = rule_form.save(commit=False)
        rule_obj.end_date = date.today()
        rule_obj.save(update_fields=['end_date'])
        success_msg = '{} was deleted successfully'.format(required_rule)
        messages.success(request, success_msg)
    except Exception as e:
        error_msg = '{} cannot be deleted '.format(required_rule)
        messages.error(request, error_msg)
        raise e
    return redirect('element_definition:list-custom-rules')


def edit_custom_rule(request, pk):
    try:
        custom_rule = get_object_or_404(Custom_Python_Rule, pk=pk)
        if custom_rule.company_id != request.user.employee.company_id:
            return HttpResponseForbidden("<h1>Access Denied! </h1>")
        if request.method == 'POST':
            form = CustomPythonRuleForm(request.POST, instance=custom_rule)
            if form.is_valid():
                custom_rule = form.save()
                success_msg = 'تم تعديل "{}" بنجاح'.format(custom_rule.name)
                messages.success(request, success_msg)
            else:  # Form was not valid
                # Spitting the errors coming from the form
                [messages.error(request, error[0])
                 for error in form.errors.values()]
        else:  # request method is GET
            form = CustomPythonRuleForm(instance=custom_rule)
            modal_close_url = 'payroll:custom_rules_list'
            context = {'table_title': 'قواعد الاحتساب المخصصة', 'modal_title': 'تعديل القاعدة',
                       'editing': True, 'modal_close_url': modal_close_url, 'form': form}
            try:
                custom_rules = Custom_Python_Rule.objects.filter(
                    company_id=request.user.employee.company_id)
                context['custom_rules'] = custom_rules
            # Just in case the logged user is not tied to an employee account (i.e. doesn't have a company_id)
            except:
                messages.error(
                    request, "لقد حدث خطأ ما، قد يكون هذا الحساب غير مسجل على شركة")
                context.pop('form')
            return render(request, 'payroll/custom_rules_list.html', context=context)
    except:
        error_msg = 'لم يتم العثور على البيان المطلوب، قد يكون قد تم حذفة من قبل'
        messages.error(request, error_msg)
    return redirect('element_definition:custom_rules_list', by='')


def fast_formula(request):
    code = request.GET.get('code')
    arr = code.split()
    element_id = arr[2]
    element = Element.objects.get(id=element_id)
    amount = str(element.fixed_amount)
    arr[2] = amount
    str1 = " "
    string = (str1.join(arr))
    print(string)
    data = {
        'string': string,
    }
    return JsonResponse(data)
