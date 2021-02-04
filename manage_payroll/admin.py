from django.contrib import admin
from manage_payroll.models import (Bank_Master, Payment_Type, Payment_Method,
                                   Payroll_Period, Payroll_Master, Assignment_Batch, Assignment_Batch_Include,
                                   Assignment_Batch_Exclude)


################################ Model Admin ######################################
@admin.register(Bank_Master)
class BankAdmin(admin.ModelAdmin):
    fields = (
        'bank_name',
        'branch_name',
        'country',
        'address',
        'currency',
        'start_date',
        'end_date',
    )
    list_display = (
        'bank_name',
        'country',
        )

@admin.register(Payroll_Master)
class PayrollMasterAdmin(admin.ModelAdmin):
    fields = (
          'enterprise',
          'first_pay_period',
          'payroll_name',
          'payment_method',
          'period_type',
          'social_insurance',
          'tax_rule',
          'start_date',
          'end_date',
    )


@admin.register(Payment_Type)
class Payment_Typedmin(admin.ModelAdmin):
    fields = (
        'enterprise',
        'type_name',
        'category',
        'start_date',
        'end_date',
    )
    list_display = (
        'id',
        'type_name',
        'enterprise',
        )

@admin.register(Payment_Method)
class Payment_MethodAdmin(admin.ModelAdmin):
    fields = (
        'payment_type',
        'method_name',
        'bank_name',
        'account_number',
        'swift_code',
        'start_date',
        'end_date',
    )
    list_display = (
        'id',
        'payment_type',
        'method_name',
        )
