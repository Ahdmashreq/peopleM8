from django.contrib import admin
from defenition.models import LookupType, LookupDet, InsuranceRule, TaxRule, TaxSection, New_Tax_Section


####################################### Inlines Goes Here #############################################
class LookupDetInline(admin.TabularInline):
    model = LookupDet
    fields = (
        'lookup_type_fk',
        'name',
        'code',
        'description',
        'start_date',
        'end_date',
    )


####################################### Admin Forms #############################################
@admin.register(LookupType)
class LookupTypeAdmin(admin.ModelAdmin):
    fields = (
            'enterprise',
            'lookup_type_name',
            'lookup_type_description',
            'start_date',
            'end_date',
    )
    inlines=[
        LookupDetInline,
    ]
    # save the TabularInline data
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.enterprise = request.user.company
            instance.created_by = request.user
            instance.last_update_by = request.user
            instance.save()
        formset.save_m2m()
    # save the ModelAdmin data here
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.last_update_by = user
        instance.save()
        form.save_m2m()

@admin.register(InsuranceRule)
class SocialInsuranceAdmin(admin.ModelAdmin):
    model = InsuranceRule
    fields = (
        'name',
        'enterprise_name',
        'basic_deduction_percentage',
        'variable_deduction_percentage',
        'maximum_insurable_basic_salary',
        'maximum_insurable_variable_salary',
        'start_date',
        'end_date',
    )

@admin.register(TaxRule)
class TaxRuleAdmin(admin.ModelAdmin):
    model = TaxRule
    fields = (
        'name',
        'enterprise',
        'personal_exemption',
        'round_down_to_nearest_10',
    )

@admin.register(TaxSection)
class TaxSectionAdmin(admin.ModelAdmin):
    model = TaxSection
    fields = (
        'name',
        'tax_rule_id',
        'salary_from',
        'salary_to',
        'tax_percentage',
        'tax_discount_percentage',
        'section_execution_sequence',
    )

@admin.register(New_Tax_Section)
class NewTaxAdmin(admin.ModelAdmin):
    model = New_Tax_Section
    fields = (
        'name',
        'tax_rule_id',
        'salary_from',
        'salary_to',
        'tax_percentage',
        'tax_difference',
        'section_execution_sequence',
    )
    list_display = ['name', 'tax_difference']
