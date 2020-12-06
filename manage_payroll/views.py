from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import to_locale, get_language
from django.utils.translation import ugettext_lazy as _
from manage_payroll.models import (Assignment_Batch, Assignment_Batch_Exclude,
                                   Assignment_Batch_Include, Payment_Type, Payment_Method,
                                   Bank_Master, Payroll_Master)
from manage_payroll.forms import (AssignmentBatchForm, BatchIncludeFormSet,
                                  BatchExcludeFormSet, Payment_Type_Form, Payment_Method_Form,
                                  PaymentMethodInline, Bank_MasterForm, PayrollMasterForm)


@login_required(login_url='home:user-login')
def listAssignmentBatchView(request):
    batch_list = Assignment_Batch.objects.all().filter((Q(end_date__gte=date.today())|Q(end_date__isnull=True)))
    batchContxt = {"page_title":_("Assignment Batchs") , 'batch_list': batch_list}
    return render(request, 'list-assignment-batch.html', batchContxt)


@login_required(login_url='home:user-login')
def createAssignmentBatchView(request):
    batch_form = AssignmentBatchForm()
    batch_include_form = BatchIncludeFormSet(
        queryset=Assignment_Batch_Include.objects.none())
    batch_exclude_form = BatchExcludeFormSet(
        queryset=Assignment_Batch_Exclude.objects.none())
    if request.method == 'POST':
        batch_form = AssignmentBatchForm(request.POST)
        batch_include_form = BatchIncludeFormSet(request.POST)
        batch_exclude_form = BatchExcludeFormSet(request.POST)
        if batch_form.is_valid() and batch_include_form.is_valid() and batch_exclude_form.is_valid():
            batch_form_obj = batch_form.save(commit=False)
            batch_form_obj.created_by = request.user
            batch_form_obj.last_update_by = request.user
            batch_form_obj.save()
            batch_include_form = BatchIncludeFormSet(
                request.POST, instance=batch_form_obj)
            batch_include_obj = batch_include_form.save(commit=False)
            for x in batch_include_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            batch_exclude_form = BatchExcludeFormSet(
                request.POST, instance=batch_form_obj)
            batch_exclude_obj = batch_exclude_form.save(commit=False)
            for x in batch_exclude_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
                user_lang=user_lang=to_locale(get_language())
                if user_lang=='ar':
                    success_msg = 'تمت العملية بنجاح'
                else:
                    success_msg ='Create Successfully'
            # success_msg = 'Assignment Batch {}, has been created successfully'.format(
                # batch_form_obj.assignment_name)
                messages.success(request, success_msg)
            return redirect('manage_payroll:list-assignBatch')
        else:
            if batch_form.has_error:
                messages.error(request, batch_form.errors)
            elif batch_exclude_form.has_error:
                messages.error(request, batch_exclude_form.errors)
            elif batch_include_form.has_error:
                messages.error(request, batch_include_form.errors)
    batchContext = {
        "page_title": _("Create new Assignment Batch"),
        'batch_form': batch_form,
        'batch_include_form': batch_include_form,
        'batch_exclude_form': batch_exclude_form
    }
    return render(request, 'create-assignment-batch.html', batchContext)


@login_required(login_url='home:user-login')
def updateAssignmentBatchView(request, pk):
    required_assignment_batch = Assignment_Batch.objects.get(pk=pk)
    batch_form = AssignmentBatchForm(instance=required_assignment_batch)
    batch_include_form = BatchIncludeFormSet(
        instance=required_assignment_batch)
    batch_exclude_form = BatchExcludeFormSet(
        instance=required_assignment_batch)
    if request.method == 'POST':
        batch_form = AssignmentBatchForm(
            request.POST, instance=required_assignment_batch)
        batch_include_form = BatchIncludeFormSet(
            request.POST, instance=required_assignment_batch)
        batch_exclude_form = BatchExcludeFormSet(
            request.POST, instance=required_assignment_batch)
        if batch_form.is_valid() and batch_include_form.is_valid() and batch_exclude_form.is_valid():
            batch_form_obj = batch_form.save(commit=False)
            batch_form_obj.last_update_by = request.user
            batch_form_obj.save()
            batch_include_obj = batch_include_form.save(commit=False)
            for x in batch_include_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            batch_exclude_obj = batch_exclude_form.save(commit=False)
            for x in batch_exclude_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
                user_lang=user_lang=to_locale(get_language())
                if user_lang=='ar':
                    success_msg = 'تمت العملية بنجاح'
                else:
                    success_msg ='Create Successfully'
            # success_msg = 'Assignment Batch {}, has been created successfully'.format(
                # batch_form_obj.assignment_name)

                messages.success(request, success_msg)
            return redirect('manage_payroll:list-assignBatch')
        else:
            if batch_form.has_error:
                messages.error(request, batch_form.errors)
            elif batch_exclude_form.has_error:
                messages.error(request, batch_exclude_form.errors)
            elif batch_include_form.has_error:
                messages.error(request, batch_include_form.errors)
    batchContext = {
        "page_title": _("update Assignment Batch"),
        'batch_form': batch_form,
        'batch_include_form': batch_include_form,
        'batch_exclude_form': batch_exclude_form
    }
    return render(request, 'create-assignment-batch.html', batchContext)


@login_required(login_url='home:user-login')
def deleteAssignmentBatchView(request, pk):
    required_assignment_batch = get_object_or_404(Assignment_Batch, pk=pk)
    try:
        batch_form = AssignmentBatchForm(instance=required_assignment_batch)
        batch_obj = batch_form.save(commit=False)
        batch_obj.end_date = date.today()
        batch_include_form = BatchIncludeFormSet(
            instance=required_assignment_batch)
        batch_include_obj = batch_include_form.save(commit=False)
        for x in batch_include_obj:
            x.end_date = date.today()
            x.save(update_fields=['end_date'])
        batch_exclude_form = BatchExcludeFormSet(
            instance=required_assignment_batch)
        batch_exclude_obj = batch_exclude_form.save(commit=False)
        for x in batch_exclude_obj:
            x.end_date = date.today()
            x.save(update_fields=['end_date'])
        batch_obj.save(update_fields=['end_date'])
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = '{}تم حذف '.format(required_assignment_batch)
        else:
            success_msg = '{} was deleted successfully '.format(required_assignment_batch)
        # success_msg = '{} was deleted successfully'.format(
            # required_assignment_batch)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang=user_lang=to_locale(get_language())
        if user_lang=='ar':
            error_msg = '{} لم يتم حذف '.format(required_assignment_batch)
        else:
            error_msg = '{} cannot be deleted '.format(required_assignment_batch)
        # error_msg = '{} cannot be deleted '.format(required_assignment_batch)
            messages.error(request, error_msg)
        raise e
    return redirect('manage_payroll:list-assignBatch')

###############################################################################
#               Payment type & method inline form
###############################################################################
@login_required(login_url='home:user-login')
def createPaymentView(request):
    payment_type_form = Payment_Type_Form()
    payment_method_inline = PaymentMethodInline()
    if request.method == 'POST':
        payment_type_form = Payment_Type_Form(request.POST)
        payment_method_inline = PaymentMethodInline(request.POST)
        if payment_type_form.is_valid() or payment_method_inline.is_valid():
            payment_object = payment_type_form.save(commit=False)
            payment_object.enterprise = request.user.company
            payment_object.created_by = request.user
            payment_object.last_update_by = request.user
            payment_object.save()
            payment_method_inline = PaymentMethodInline(
                request.POST, instance=payment_object)
            if payment_method_inline.is_valid():
                inline_obj = payment_method_inline.save(commit=False)
                for row in inline_obj:
                    row.created_by = request.user
                    row.last_update_by = request.user
                    row.save()
            user_lang=user_lang=to_locale(get_language())
            if user_lang=='ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg ='Create Successfully'
            messages.success(request, success_msg)
        else:
            messages.error(request, _('Payment form hase invalid data'))
        return redirect('manage_payroll:list-payments')

    paymentContext = {
        "page_title": _("create payment"),
                      'payment_type_form': payment_type_form,
                      'payment_method_inline': payment_method_inline}
    return render(request, 'payment-create.html', paymentContext)


@login_required(login_url='home:user-login')
def listPaymentView(request):
    payment_type_list = Payment_Type.objects.filter().exclude((Q(end_date__gte=date.today())|Q(end_date__isnull=False)))
    payment_method_list = Payment_Method.objects.filter().exclude((Q(end_date__gte=date.today())|Q(end_date__isnull=False)))
    paymentContext = {
        "page_title":_("Payment Types"),
        'payment_type_list':payment_type_list,
        'payment_method_list':payment_method_list,
         }
    return render(request, 'payment-list.html', paymentContext)


@login_required(login_url='home:user-login')
def updatePaymentView(request, pk):
    payment_obj = Payment_Type.objects.get(pk=pk)
    payment_method_obj = Payment_Method.objects.filter(payment_type=pk)
    payment_type_form = Payment_Type_Form(instance=payment_obj)
    payment_method_inline = PaymentMethodInline(instance=payment_obj)
    if request.method == 'POST':
        old_payment_type = Payment_Type(
                                        enterprise = payment_obj.enterprise,
                                        type_name = payment_obj.type_name,
                                        category = payment_obj.category,
                                        start_date = payment_obj.start_date,
                                        end_date = date.today(),
                                        created_by = payment_obj.created_by,
                                        creation_date = payment_obj.creation_date,
                                        last_update_by = payment_obj.last_update_by,
                                        last_update_date = payment_obj.last_update_date,
        )
        old_payment_type.save()
        for x in payment_method_obj:
            old_payment_method = Payment_Method(
                                                payment_type = x.payment_type,
                                                method_name = x.method_name,
                                                bank_name = x.bank_name,
                                                account_number = x.account_number,
                                                swift_code = x.swift_code,
                                                start_date = x.start_date,
                                                end_date = date.today(),
                                                created_by = x.created_by,
                                                creation_date = x.creation_date,
                                                last_update_by = x.last_update_by,
                                                last_update_date = x.last_update_date,
            )
            old_payment_method.save()
        payment_type_form = Payment_Type_Form(request.POST, instance=payment_obj)
        payment_method_inline = PaymentMethodInline(request.POST, instance=payment_obj)
        if payment_type_form.is_valid() and payment_method_inline.is_valid():
            payment_object = payment_type_form.save(commit=False)
            payment_object.enterprise = request.user.company
            payment_object.created_by = request.user
            payment_object.last_update_by = request.user
            payment_object.save()
            payment_method_inline = PaymentMethodInline(
                request.POST, instance=payment_object)
            if payment_method_inline.is_valid():
                inline_obj = payment_method_inline.save(commit=False)
                for row in inline_obj:
                    row.created_by = request.user
                    row.last_update_by = request.user
                    row.save()
            return redirect('manage_payroll:list-payments')
            success_msg = _('Payment Updated Successfully')
            messages.success(request, success_msg)
        else:
            messages.error(request, _('payment_type_form hase invalid data'))
    paymentContext = {
        "page_title":_("update payment"),
                      'payment_type_form': payment_type_form,
                      'payment_method_inline': payment_method_inline}
    return render(request, 'payment-create.html', paymentContext)


@login_required(login_url='home:user-login')
def correctPaymentView(request, pk):
    payment_obj = Payment_Type.objects.get(pk=pk)
    payment_type_form = Payment_Type_Form(instance=payment_obj)
    payment_method_inline = PaymentMethodInline(instance=payment_obj)
    if request.method == 'POST':
        payment_type_form = Payment_Type_Form(request.POST)
        payment_method_inline = PaymentMethodInline(request.POST, instance=payment_obj)
        if payment_type_form.is_valid() and payment_method_inline.is_valid():
            payment_object = payment_type_form.save(commit=False)
            payment_object.created_by = request.user
            payment_object.last_update_by = request.user
            payment_object.save()
            payment_method_inline = PaymentMethodInline(
                request.POST, instance=payment_object)
            if payment_method_inline.is_valid():
                inline_obj = payment_method_inline.save(commit=False)
                for row in inline_obj:
                    row.created_by = request.user
                    row.last_update_by = request.user
                    row.save()
            return redirect('manage_payroll:list-payments')
            success_msg = _('Payment Updated Successfully')
            messages.success(request, success_msg)
        else:
            messages.error(request, _('payment_type_form hase invalid data'))
    paymentContext = {
        "page_title": _("correct payment"),
                      'payment_type_form': payment_type_form,
                      'payment_method_inline': payment_method_inline}
    return render(request, 'payment-create.html', paymentContext)


@login_required(login_url='home:user-login')
def deletePaymentView(request, pk):
    required_payment_type = get_object_or_404(Payment_Type, pk=pk)
    try:
        type_form = Payment_Type_Form(instance=required_payment_type)
        type_obj = type_form.save(commit=False)
        type_obj.end_date = date.today()
        method_form = PaymentMethodInline(instance=required_payment_type)
        method_obj = method_form.save(commit=False)
        for x in method_obj:
            x.end_date = date.today()
            x.save(update_fields=['end_date'])
        type_obj.save(update_fields=['end_date'])
        user_lang=user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = '{}تم حذف '.format(required_payment_type)
        else:
            success_msg = '{} was deleted successfully '.format(required_payment_type)
        # success_msg = '{} was deleted successfully'.format(
            # required_payment_type)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang=user_lang=to_locale(get_language())
        if user_lang=='ar':
            error_msg = '{} لم يتم حذف '.format(required_payment_type)
        else:
            error_msg = '{} cannot be deleted '.format(required_payment_type)
        # error_msg = '{} cannot be deleted '.format(required_payment_type)
        messages.error(request, error_msg)
        raise e
    return redirect('manage_payroll:list-payments')

#               End of Payment type & method inline form
###############################################################################


@login_required(login_url='home:user-login')
def createBankAccountView(request):
    bank_form = Bank_MasterForm()
    if request.method == 'POST':
        bank_form = Bank_MasterForm(request.POST)
        if bank_form.is_valid():
            master_object = bank_form.save(commit=False)
            master_object.enterprise = request.user.company
            master_object.created_by = request.user
            master_object.last_update_by = request.user
            master_object.save()
            return redirect('manage_payroll:list-banks')
            success_msg = _('Bank Created Successfully')
            messages.success(request, success_msg)
        else:
            [messages.error(request, error[0])
             for error in bank_form.errors.values()]
    myContext = {"page_title":_("Create bank branch") ,
                 'bank_form': bank_form, }
    return render(request, 'create-bank-accounts.html', myContext)


@login_required(login_url='home:user-login')
def listBankAccountsView(request):
    if request.method == 'GET':
        bank_master = Bank_Master.objects.filter((Q(end_date__gte=date.today())|Q(end_date__isnull=True)))
    myContext = {"page_title": _("Bank List"), 'bank_master': bank_master, }
    return render(request, 'list-bank-branchs.html', myContext)


@login_required(login_url='home:user-login')
def updateBankAccountView(request, pk):
    required_bank = Bank_Master.objects.get(pk=pk)
    if request.method == 'POST':
        bank_form = Bank_MasterForm(request.POST, instance=required_bank)
        if bank_form.is_valid():
            bank_form.save()
            return redirect('manage_payroll:list-banks')
            success_msg = _('Bank Updated Successfully')
            messages.success(request, success_msg)
            # redirect_to = reverse('manage_payroll:update-bank', kwargs={'pk': pk})
            # return redirect(redirect_to)
        else:
            [messages.error(request, account_form.errors)]
    else:
        bank_form = Bank_MasterForm(instance=required_bank)
    myContext = {"page_title": _("update bank details"), 'bank_form': bank_form, }
    return render(request, 'create-bank-accounts.html', myContext)


@login_required(login_url='home:user-login')
def deleteBankAccountView(request, pk):
    required_bank = get_object_or_404(Bank_Master, pk=pk)
    try:
        bank_form = Bank_MasterForm(instance=required_bank)
        bank_obj = bank_form.save(commit=False)
        bank_obj.end_date = date.today()
        bank_obj.save(update_fields=['end_date'])
        user_lang=user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = '{} تم حذف'.format(required_bank)
        else:
            success_msg ='{} was deleted successfully'.format(required_bank)
        # success_msg = '{} was deleted successfully'.format(required_bank)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang=user_lang=to_locale(get_language())
        if user_lang=='ar':
            error_msg = '{} لم يتم حذف '.format(required_bank)
        else:
            error_msg = '{} cannot be deleted '.format(required_bank)
        # error_msg = '{} cannot be deleted '.format(required_bank)
        messages.error(request, error_msg)
        raise e
    return redirect('manage_payroll:list-banks')

################################################################################
@login_required(login_url='home:user-login')
def listPayrollView(request):
    list_payroll = Payroll_Master.objects.filter(enterprise=request.user.company).filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True))
    payrollContext = {"page_title":_("payroll list") ,
                      'list_payroll': list_payroll}
    return render(request, 'list-payrolls.html', payrollContext)


@login_required(login_url='home:user-login')
def createPayrollView(request):
    payroll_form = PayrollMasterForm()
    if request.method == 'POST':
        payroll_form = PayrollMasterForm(request.POST)
        if payroll_form.is_valid():
            master_object = payroll_form.save(commit=False)
            master_object.enterprise = request.user.company
            master_object.created_by_id = request.user.id
            master_object.last_update_by_id = request.user.id
            master_object.save()
            return redirect('manage_payroll:list-payroll')
            success_msg = _('Payroll Created Successfully')
            messages.success(request, success_msg)
    payContext = {
        "page_title": _("Create Payroll"),
        'pay_form': payroll_form
    }
    return render(request, 'create-payroll.html', payContext)


@login_required(login_url='home:user-login')
def updatePayrollView(request, pk):
    required_payroll = get_object_or_404(Payroll_Master, pk=pk)
    pay_form = PayrollMasterForm(instance=required_payroll)
    if request.method == 'POST':
        pay_form = PayrollMasterForm(request.POST, instance=required_payroll)
        if pay_form.is_valid():
            pay_form.save()
        return redirect('manage_payroll:list-payroll')
        success_msg = _('Payroll Created Successfully')
        messages.success(request, success_msg)
    payContext = {
        "page_title":_("Update Payroll") ,
        'pay_form': pay_form
    }
    return render(request, 'create-payroll.html', payContext)


@login_required(login_url='home:user-login')
def deletePayrollView(request, pk):
    required_payroll = get_object_or_404(Payroll_Master, pk=pk)
    try:
        payroll_form = PayrollMasterForm(instance=required_payroll)
        payroll_obj = payroll_form.save(commit=False)
        payroll_obj.end_date = date.today()
        payroll_obj.save(update_fields=['end_date'])
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = '{}تم حذف'.format(required_payroll)
        else:
            success_msg = '{} was deleted successfully'.format(required_payroll)
        # success_msg = '{} was deleted successfully'.format(required_payroll)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            error_msg = '{} لم يتم حذف '.format(required_payroll)
        else:
            error_msg = '{} cannot be deleted '.format(required_payroll)
        # error_msg = '{} cannot be deleted '.format(required_payroll)
        messages.error(request, error_msg)
        raise e
    return redirect('manage_payroll:list-payroll')
