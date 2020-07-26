from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserCreationForm, AddUserForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from custom_user.models import User
from employee.models import Employee, JobRoll
from service.models import Bussiness_Travel
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest
from django.utils import translation
from datetime import date, datetime
from django.urls import reverse_lazy
from django.utils import formats
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import to_locale, get_language
from company.models import Enterprise
from notification.models import Notification
from leave.models import Leave
from datetime import datetime, timezone

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next:
                    return redirect(next)
                if user.employee_type == 'A':
                    return redirect(reverse('home:homepage'))
                else:
                    return redirect(reverse('attendance:list-attendance'))
            else:
                messages.error(request, 'Inactive Account')
                return render(request, 'login.html')
        else:
            messages.error(request, _(
                'Login Failed, Please Check the Username or Password'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required(login_url='/login')
def homepage(request):
    if request.user.employee_type =="A":
        return render(request, 'index.html', context=None)
    else:
        return render(request, 'index_user.html', context=None)

@login_required(login_url='/login')
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
                           name = form.cleaned_data.get('company_name'),
                           business_unit_name = form.cleaned_data.get('business_unit_name'),
                           reg_tax_num = form.cleaned_data.get('reg_tax_num'),
                           commercail_record = form.cleaned_data.get('commercail_record'),
                           created_by_id = user.id,
                           last_update_by_id = user.id,
                           )
            comp.save()
            user.company_id = comp.id
            user.save(update_fields=['company'])
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home:homepage'))
            else:
                user_lang=user_lang=to_locale(get_language())
                if user_lang=='ar':
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
            user = form.save(commit=False)
            user.company = request.user.company
            user.save()
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

class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
