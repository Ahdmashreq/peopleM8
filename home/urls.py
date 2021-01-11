from django.urls import path, include
from home import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

app_name = 'home'

urlpatterns=[
        path('en/', views.viewEN, name='en'),
        path('ar/', views.viewAR, name='ar'),
        path('login/', views.user_login, name='user-login'),
        path('logout/', views.user_logout, name='logout'),
        path('register/', views.register, name='register'),
        path('add-user/', views.addUserView, name='new-user'),
        path('', views.homepage, name='homepage'),
        # path('', views.pie_chart, name='pie-chart'),
        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
          name='password_change_done'),

        path('password_change/', views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
          name='password_change'),

        path('password_reset/done/', views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),

        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
        #groups
        path('groups/',include([
            path('',views.group_list,name='group_list'),
            path('<int:pk>/',views.group_view,name='group_view'),
            path('new/',views.create_groups,name='create_group'),
            path('update/<int:pk>',views.edit_groups,name='update_group'),

        ])),
]
