from django.contrib import admin
from element_definition.models import (Element_Batch,
                                       Element_Master, Element_Batch_Master, Element_Link, SalaryStructure, Element,
                                       StructureElementLink, ElementHistory,
                                       )
from import_export.admin import ImportExportModelAdmin, ImportMixin


####################################### Inlines Goes Here #############################################
class ElementBatchMasterInline(admin.TabularInline):
    model = Element_Batch_Master
    fields = (
        'element_master_fk',
        'element_batch_fk',
        'start_date',
        'end_date',
    )


class StructureElementLinkInline(admin.TabularInline):
    model = StructureElementLink


####################################### Admin Forms #############################################
@admin.register(Element_Master)
class ElementMasterAdmin(ImportExportModelAdmin):
    class Meta:
        model = Element_Master

    # fields = (
    #     'enterprise',
    #     'element_name',
    #     'db_name',
    #     'element_type',
    #     'classification',
    #     'effective_date',
    #     'retro_flag',
    #     'tax_flag',
    #     'fixed_amount',
    #     'element_formula',
    #     'start_date',
    #     'end_date',
    # )
    list_display = (
        'element_name',
        'element_type',
        'classification',
        'effective_date',
    )


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    class Meta:
        model = SalaryStructure

    inlines = [
        StructureElementLinkInline
    ]


@admin.register(Element_Batch)
class ElementBatchAdmin(admin.ModelAdmin):
    class Meta:
        model = Element_Batch

    fields = (
        'payroll_fk',
        'batch_name',
        'start_date',
        'end_date',
    )
    inlines = [
        ElementBatchMasterInline
    ]


@admin.register(Element_Link)
class Element_Link_Admin(admin.ModelAdmin):
    class Meta:
        model = Element_Link

    fields = (
        'element_master_fk',
        'payroll_fk',
        'element_dept_id_fk',
        'element_job_id_fk',
        'element_grade_fk',
        'element_position_id_fk',
        'assignment_category',
        'standard_flag',
        'link_to_all_payroll_flag',
        'start_date',
        'end_date',
    )


@admin.register(Element)
class ElementAdmin(ImportExportModelAdmin):
    class Meta:
        model = Element

@admin.register(StructureElementLink)
class StructureElementAdmin(admin.ModelAdmin):
    class Meta:
        model = StructureElementLink


@admin.register(ElementHistory)
class ElementHistoryAdmin(admin.ModelAdmin):
    class Meta:
        model = ElementHistory
