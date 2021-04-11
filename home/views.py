from django.shortcuts import render, reverse, redirect , HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash, user_logged_in, user_logged_out
from django.contrib.auth.forms import (PasswordChangeForm, )
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.dispatch.dispatcher import receiver
from django.contrib.sessions.models import Session
from .forms import CustomUserCreationForm, AddUserForm, GroupAdminForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from custom_user.models import User, UserCompany
from employee.models import Employee, JobRoll
from service.models import Bussiness_Travel
from django.contrib.auth.decorators import login_required
from django.utils import translation
from datetime import date, datetime
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import to_locale, get_language
from company.models import Enterprise
from leave.models import Leave
from custom_user.models import UserCompany, Visitor
from django.contrib.auth.models import Group
from .forms import GroupForm, GroupViewForm
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from MashreqPayroll.utils import allowed_user


def viewAR(request):
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
    request.session.modified = True
    user_language = 'ar'
    translation.activate(user_language)
    request.LANGUAGE_CODE = translation.get_language()
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def viewEN(request):
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
    request.session.modified = True
    user_language = 'en'
    translation.activate(user_language)
    request.LANGUAGE_CODE = translation.get_language()
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    request.LANGUAGE_CODE = translation.get_language()
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@never_cache
def user_login(request):
    next = request.GET.get('next')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # check if the user has employee record if not cannot login
                employee = Employee.objects.filter(user=user) if Employee.objects.filter(user=user) else None
                if employee is None:
                    messages.error(request, _(
                        'These Credentials are not assigned to an Employee yet, Please Contact an admin '))
                    return render(request, 'login.html')
                login(request, user)
                if next:
                    return redirect(next)
                if str(request.user.groups.first()) == "Admin":
                    return redirect(reverse('home:homepage'))
                else:
                    return redirect(reverse('attendance:user-list-attendance'))
            else:
                messages.error(request, 'Inactive Account')
                return render(request, 'login.html')
        else:
            messages.error(request, _(
                'Login Failed, Please Check the Username or Password'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required(login_url='home:user-login')
def user_home_page(request):
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)

    leave_count = Leave.objects.filter(
        user=request.user, status='pending').count()

    birthdays_count = Employee.objects.filter(
        date_of_birth__month=date.today().month).count()
    employee_count = Employee.objects.all().count()

    emps_birthdays = Employee.objects.filter(
        date_of_birth__month=date.today().month)

    # List MY Bussiness_Travel/services
    bussiness_travel_service = Bussiness_Travel.objects.filter(
        Q(emp=employee) | Q(manager=employee), status='pending')
    # get a list of all notifications related to the current user within the current month
    my_notifications = request.user.notifications.filter(timestamp__year=datetime.now().year,
                                                         timestamp__month=datetime.now().month)

    context = {
        'birthdays': emps_birthdays,
        'count_birthdays': birthdays_count,
        'count_employees': employee_count,
        'count_leaves': leave_count,
        'bussiness_travel_service': bussiness_travel_service,
        'my_notifications': my_notifications,
    }
    return render(request, 'index_user.html', context=context)


@login_required(login_url='home:user-login')
def admin_home_page(request):

    '''
    Ziad
    4/3/2021
    Display total employees and today's absence and approved leaves in dashboard
    '''
    emp_list = Employee.objects.filter(enterprise=request.user.company).filter(
        (Q(emp_end_date__gt=date.today()) | Q(emp_end_date__isnull=True)))
    num_of_emp = len(emp_list)
    list_leaves = Leave.objects.filter(status='Approved')
    now_date = datetime.date(datetime.now())
    Today_Approved_Leaves = 0
    for leave in list_leaves :
        if leave.enddate >= now_date and leave.startdate <= now_date :
            Today_Approved_Leaves+=1
    today_present = num_of_emp - Today_Approved_Leaves

    user_companies_count = UserCompany.objects.filter(
        user__company=request.user.company).count()
    if user_companies_count == 0:
        return redirect('company:user-companies-list')
        pass
    else:
        # employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
        # get a list of all notifications related to the current user within the current month

        my_notifications = request.user.notifications.filter(timestamp__year=datetime.now().year,
                                                             timestamp__month=datetime.now().month)
        context = {'my_notifications': my_notifications, 'num_of_emp' : num_of_emp ,
        'Today_Approved_Leaves' : Today_Approved_Leaves , 'today_present' : today_present ,}

        return render(request, 'index.html', context=context)


@login_required(login_url='home:user-login')
def homepage(request):
    if request.user.employee_type == "A":
        return admin_home_page(request)
    else:
        return user_home_page(request)


@login_required(login_url='home:user-login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:user-login'))


def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            comp = Enterprise(
                name=form.cleaned_data.get('company_name'),
                business_unit_name=form.cleaned_data.get('business_unit_name'),
                reg_tax_num=form.cleaned_data.get('reg_tax_num'),
                commercail_record=form.cleaned_data.get('commercail_record'),
                created_by_id=user.id,
                last_update_by_id=user.id,
            )
            comp.save()
            user.company_id = comp.id
            user.save(update_fields=['company'])
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home:homepage'))
            else:
                user_lang = user_lang = to_locale(get_language())
                if user_lang == 'ar':
                    messages.error(request, 'This account is deactivated!')
                else:
                    messages.error(request, 'This Account is inactive!')
                return render(request, 'login.html')
    return render(request, 'register.html', {'register_form': form})


def addUserView(request):
    form = AddUserForm()
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.company = request.user.company
            user_obj.save()
            user_company = UserCompany(
                user=user_obj,
                company=request.user.company,
                active=True,
                created_by=request.user,
                creation_date=date.today(),
            )
            user_company.save()
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم الانشاء بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
            return redirect('home:new-user')
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            messages.error(request, form.errors)
    myContext = {
        'page_title': _("Create New User"),
        'add_user': form,
    }
    return render(request, 'add-user.html', myContext)


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home:homepage')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@allowed_user(allowed_roles=['Admin'])
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'groups_list.html', {'groups': groups})


def group_view(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupViewForm(instance=group)
    return render(request, 'group-view.html', {'form': form})


def create_groups(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم الانشاء بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
            return redirect('home:group_list')
    return render(request, 'group-create.html', {'form': form})


def edit_groups(request, pk):
    group = get_object_or_404(Group, id=pk)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect('/contracts')
    else:
        form = GroupForm(instance=group)
    return render(request, 'group-create.html', {'form': form})


def assign_role(request):
    form = GroupAdminForm()
    if request.method == "POST":
        form = GroupAdminForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user = User.objects.get(id=form.data['user'])
            my_group = Group.objects.get(id=form.data['group'])
            user.groups.add(my_group)
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم الإنشاء بنجاح'
            else:
                success_msg = 'Created Successfully'
                messages.success(request, success_msg)
        return redirect('home:user_groups')
    return render(request, 'group_assign.html', {'form': form})


def user_group_list(request):
    users = User.objects.all()
    return render(request, 'user_group_list.html', {'users': users})


def user_group_delete(request, pk):
    user = User.objects.get(id=pk)
    user.groups.clear()
    user_lang = to_locale(get_language())
    if user_lang == 'ar':
        success_msg = 'تم المسح بنجاح'
    else:
        success_msg = 'Deleted Successfully'
        messages.success(request, success_msg)
    return redirect('home:user_groups')
