from django.urls import path, include
from company import views

app_name = 'company'

urlpatterns = [
    ######################### BusinessGroup URLs ###################################
    path('user/companies/list/', views.list_user_companies_view, name='user-companies-list'),
    path('user/companies/create/', views.create_user_companies_view, name='user-companies-create'),
    path('user/companies/makeActive/<int:company_id>/', views.mark_as_active_view, name='user-company-active'),
    path('enterprise/', include([
        path('new/', views.companyCreateView, name='company-create'),
        path('information/list/', views.listCompanyInformation, name='list-company-information'),
        path('update/<int:pk>/', views.updateBusinessGroup, name='update-business-group'),
        path('delete/<int:pk>/', views.deleteBusinessGroup, name='delete-enterprise'),
    ])),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('setup/', views.load_modules, name='setup_company'),

    path('assinment/', include([
        ######################### Department URLs ###################################
        path('department/list/', views.listDepartmentView, name='list-department'),
        path('department/new/', views.createDepartmentView, name='department-create'),
        path('department/update/<int:pk>', views.updateDepartmentView, name='department-update'),
        path('department/view/<int:pk>', views.viewDepartmentView, name='department-view'),
        path('department/correct/<int:pk>', views.correctDepartmentView, name='department-correct'),
        path('department/delete/<int:pk>', views.deleteDepartmentView, name='department-delete'),
        path('department/export/', views.export_department_data, name='department-export'),
        path('hirarchy/', views.viewHirarchy, name='hirarchy'),
        ######################### Jobs URLs #########################################
        path('jobs/list/', views.listJobView, name='list-jobs'),
        path('job/new/', views.createJobView, name='job-create'),
        path('job/update/<int:pk>', views.updateJobView, name='job-update'),
        path('job/correct/<int:pk>', views.correctJobView, name='job-correct'),
        path('job/delete/<int:pk>', views.deleteJobView, name='job-delete'),
        path('job/export/', views.export_job_data, name='job-export'),

        ######################### Grades URLs #######################################
        path('grade/list/', views.listGradeView, name='list-grades'),
        path('grade/new/', views.createGradeView, name='grade-create'),
        path('grade/update/<int:pk>', views.updateGradeView, name='grade-update'),
        path('grade/correct/<int:pk>', views.correctGradeView, name='grade-correct'),
        path('grade/delete/<int:pk>', views.deleteGradeView, name='grade-delete'), 
        path('grade/export/', views.export_grade_data, name='grade-export'),

        ######################### Positions URLs ###################################
        path('positions/list/', views.listPositionView, name='list-positions'),
        path('position/new/', views.createPositionView, name='position-create'),
        path('position/update/<int:pk>', views.updatePositionView, name='position-update'),
        path('position/correct/<int:pk>', views.correctPositionView, name='position-correct'),
        path('position/delete/<int:pk>', views.deletePositionView, name='position-delete'),
        path('position/export/', views.export_position_data, name='position-export'),

    ])),
    ######################### Working Hours Policy URLs ###################################
    path('policies/', include([
        ######################### Department URLs ###################################
        path('years/list/', views.listYearsView, name='list-years'),
        path('working_hrs_policy/new/', views.CreateWorkingPolicyView, name='policy-create'),
        path('working_hrs_policy/list/', views.listWorkingPolicyView, name='working-hrs-policy-list'),
        path('working_hrs_policy/correct/<int:pk>', views.correctWorkingPolicyView, name='policy-correct'),
        path('yearly_holidays/list/<int:year_id>', views.listYearlyHolidayView, name='yearly-holiday-list'),
        path('yearly_holidays/create/<int:year_id>', views.createYearlyHolidayView, name='yearly-holiday-create'),
        path('yearly_holidays/correct/<int:pk>', views.correctYearlyHolidayView, name='yearly-holiday-correct'),
        path('yearly_holidays/delete/<int:pk>', views.deleteYearlyHolidayView, name='yearly-holiday-delete'),
        path('working_hrs_policy/delete/<int:pk>', views.deleteWorkingPolicyView, name='working-hrs-policy-delete'),

        path('working-hrs-deduction-policy/new/', views.create_working_hours_deductions_view, name='hours-deduction-policy-create'),
        path('working-hrs-deductions/list/', views.list_working_hours_deductions_view, name='working-hrs-deductions-list'),

    ]
    )),
]
