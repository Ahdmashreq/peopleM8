from django.urls import path, include
from company import views

app_name = 'company'

urlpatterns = [
    ######################### BusinessGroup URLs ###################################
    path('enterprise/', include([
        path('new/', views.companyCreateView, name='company-create'),
        path('information/list/', views.listCompanyInformation, name='list-company-information'),
        path('update/<int:pk>/', views.updateBusinessGroup, name='update-business-group'),
        path('delete/<int:pk>/', views.deleteBusinessGroup, name='delete-enterprise'),
    ])),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

    path('assinment/', include([
        ######################### Department URLs ###################################
        path('department/list/', views.listDepartmentView, name='list-department'),
        path('list/', views.listAssignmentView, name='list-assignment'),
        path('department/new/', views.createDepartmentView, name='department-create'),
        path('department/update/<int:pk>', views.updateDepartmentView, name='department-update'),
        path('department/view/<int:pk>', views.viewDepartmentView, name='department-view'),
        path('department/correct/<int:pk>', views.correctDepartmentView, name='department-correct'),
        path('department/delete/<int:pk>', views.deleteDepartmentView, name='department-delete'),
        path('hirarchy/', views.viewHirarchy, name='hirarchy'),
        ######################### Jobs URLs #########################################
        path('jobs/list/', views.listJobView, name='list-jobs'),
        path('job/new/', views.createJobView, name='job-create'),
        path('job/update/<int:pk>', views.updateJobView, name='job-update'),
        path('job/correct/<int:pk>', views.correctJobView, name='job-correct'),
        path('job/delete/<int:pk>', views.deleteJobView, name='job-delete'),

        ######################### Grades URLs #######################################
        path('grade/list/', views.listGradeView, name='list-grades'),
        path('grade/new/', views.createGradeView, name='grade-create'),
        path('grade/update/<int:pk>', views.updateGradeView, name='grade-update'),
        path('grade/correct/<int:pk>', views.correctGradeView, name='grade-correct'),
        path('grade/delete/<int:pk>', views.deleteGradeView, name='grade-delete'),

        ######################### Positions URLs ###################################
        path('positions/list/', views.listPositionView, name='list-positions'),
        path('position/new/', views.createPositionView, name='position-create'),
        path('position/update/<int:pk>', views.updatePositionView, name='position-update'),
        path('position/correct/<int:pk>', views.correctPositionView, name='position-correct'),
        path('position/delete/<int:pk>', views.deletePositionView, name='position-delete'),

    ])),
    ######################### Working Hours Policy URLs ###################################
    path('policies/', include([
        ######################### Department URLs ###################################
        path('list/', views.listPoliciesView, name='list-policies'),
        path('working_hrs_policy/new/', views.CreateWorkingPolicyView, name='policy-create'),
        path('working_hrs_policy/list/', views.listWorkingPolicyView, name='working-hrs-policy-list'),
        path('working_hrs_policy/correct/<int:pk>', views.correctPolicyView, name='policy-correct'),
        path('yearly_holidays/list/', views.listYearlyHolidayView, name='yearly-holiday-list'),
        path('yearly_holidays/create/', views.CreateYearlyHolidayView, name='yearly-holiday-create'),
        path('yearly_holidays/correct/<int:pk>', views.correctYearlyHolidayView, name='yearly-holiday-correct'),

    ]
    )),
]
