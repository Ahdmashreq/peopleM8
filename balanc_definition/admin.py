from django.contrib import admin
from balanc_definition.models import Cost_Level, Cost_Detail

@admin.register(Cost_Level)
class CostLevelAdmin(admin.ModelAdmin):
    fields = (
          'level_name',
          'start_date',
          'end_date',
    )

@admin.register(Cost_Detail)
class CostDetailAdmin(admin.ModelAdmin):
    fields = (
            'level_Department',
            'level_Job',
            'level_Grade',
            'level_Position',
            'debit_account',
            'credit_account',
    )
