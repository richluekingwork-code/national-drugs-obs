from django.urls import path
from . import views  

urlpatterns = [
    # ------------------ Logs Urls ------------------------
    #===============================================================================================
    #                                   Moj Head page Urls
    #===============================================================================================
    path('national/drug/observatory/moj/head/home/', views.moj_head_home, name='moj_head_home'),
    
    #===============================================================================================
    #                                  MOJ Officers page Urls
    #===============================================================================================
    path('national/drug/observatory/moj/officers/home/', views.moj_officers_home, name='moj_officers_home'),    
    path('national/drug/observatory/moj/officers/create/cases/update/', views.moj_officers_create_court_cases_update, name='create_cases_update'),
    path('national/drug/observatory/moj/officers/view/court/cases/update/', views.moj_officers_view_court_cases_update, name='view_cases_update'),
    path('national/drug/observatory/LDEA/officers/view/court/cases/detail <str:id>/', views.moj_officers_court_cases_detail, name='court_cases_detail'),
    path('national/drug/observatory/moj/officers/create/victim/details/', views.moj_officers_create_victim_details, name='create_victim_details'),
    path('national/drug/observatory/moj/officers/view/victim/details/', views.moj_officers_view_victim_details, name='view_victim_details'),
    
    
    #===============================================================================================
    #                                  LMoJ IT User page Urls
    #===============================================================================================
    path('national/drug/observatory/moj/it/head/home/', views.moj_admin_home, name='moj_it_head'),
    path('national/drug/observatory/moj/admin/create/LDEA/account/', views.moj_create_ldea_account, name='ceate_ldea_account'),
    path('national/drug/observatory/moj/admin/view/LDEA/account/', views.moj_view_ldea_account, name='view_ldea_account'),
    path('national/drug/observatory/moj/admin/create/MoJ/account/', views.moj_create_account, name='ceate_moj_account'),
    path('national/drug/observatory/moj/admin/view/MoJ/account/', views.moj_view_account, name='view_moj_account'),
    
    path('national/drug/observatory/moj/admin/create/Moh/account/', views.moj_create_moh_account, name='ceate_moh_account'),
    path('national/drug/observatory/moj/admin/view/Moh/account/', views.moh_view_account, name='view_moh_account'), 
    
    path('national/drug/observatory/moj/admin/create/MoG/account/', views.moj_create_mog_account, name='ceate_mog_account'),
    path('national/drug/observatory/moj/admin/view/MoG/account/', views.moj_view_mog_account, name='view_mog_account'), 
    
    
    
    path('national/drug/observatory/moj/admin/create/MoYS/account/', views.moj_create_moys_account, name='ceate_moys_account'),
    path('national/drug/observatory/moj/admin/view/MoYS/account/', views.moj_view_moys_account, name='view_moys_account'), 
    
    
    
    path('national/drug/observatory/moj/admin/activate/deactivate/users/', views.moj_admin_activate_deactivate_users, name='activate_deactivate_users'), 
    path('moj/users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('national/drug/observatory/moj/admin/audit/users/logs/', views.moj_admin_audit_logs, name='audit_logs'), 
    
        
]