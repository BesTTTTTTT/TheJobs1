from django.urls import path
from . import views
from .views import job_search , job_detail ,logout_view ,your_forms_view_name ,cst_detail

urlpatterns = [
    path('',views.home),
    path('base1',views.homes),
    path('login',views.custom_login),
    
    path('add_job',views.add_jobs),
    path('forms',views.apply_custom),
    path('manage_drug',views.manage_drug),

    path('logout/',views.logout_view),
    path('register/', views.register_view, name='register'),
    path('login/', views.logout_view, name='login'),
    path('job_detail/<int:pk>/', job_detail, name='job_detail'),
    path('cst_detail/<int:pk>/', cst_detail, name='cst_detail'),
    path('job_search/logout/', logout_view, name='logout_view'),  
    path('register/',  views.register_view, name='register'),
  
    path('company_login/',  views.login_company, name='company_login'),
    path('company_login/register_company/',  views.register_company, name='register_company'),
    path('company_login/', views.login_company, name='company_login'),
    path('company_login/register_conpany/', views.register_company, name='register_company'),
    path('logout/', logout_view, name='logout'),
    

    path('forms/', views.forms_view, name='your_forms_view_name'),
    path('your_forms_view/<str:title>/<str:company>/', views.your_forms_view_name, name='your_forms_view_name'),
    path('apply_custom/', views.apply_custom, name='apply_custom'),
    path('edit_job/', views.edit_jobs, name='edit_jobs'),  
    path('edit_view/<int:pk>/', views.edit_form, name='edit_view'),
    path('edit_view/<int:pk>/', views.edit_view, name='edit_view'),
    path('edit_view/<int:pk>/', views.edit_form, name='your_edit_view_name'),
    path('custom_list/', views.custom_lists, name='custom_list'),
    path('custom_lists/', views.custom_objects_list, name='custom_lists'),


    path('send_email/', views.send_emails, name='send_email'),
    path('send_email_form/', views.send_emails, name='send_email_form'),
    # path('edit_job/', views.job_searchadmin, name='job_searchadmin'),
    path('job_searchadmin/', views.job_searchadmin, name='job_searchadmin'),
    path('search/', job_search, name='search'),
    path('search/', job_search, name='job_search'),

    
    path('custom_list/logout/', logout_view, name='logout_view'),
    path('search/logout/', logout_view, name='logout_view'),
    path('search/logout/', logout_view, name='search_logout'),
    path('edit_job/logout/', logout_view, name='edit_job_logout'),
    path('forms/logout/', logout_view, name='forms_logout'),
   
    path('company_jobs/logout/', logout_view, name='logout_view'),    
  
    path('add_jobcom/', views.add_jobcompany, name='add_jobcompany'),
    path('company_jobs/', views.company_jobs, name='company_jobs'),
    path('base1/',  views.homes, name='base1'),
    path('base1/', views.homes, name='base1'),
    path('send_emails/', views.send_emails, name='send_emails'),
    path('send_email_form/<str:email>/', views.send_email_form, name='send_email_form'),
    path('delete_custom/<int:custom_id>/', views.delete_custom, name='delete_custom'),
    path('edit_view/<int:pk>/', views.edit_form, name='your_edit_view_name'),

    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),

]