from django.urls import path
from . import views  

urlpatterns = [
    #===============================================================================================
    #                                  LDEA/head page Urls
    #===============================================================================================
    path('national/drug/observatory/LDEA/head/page', views.ldea_head_page, name='ldea_head_home'),
    path('national/drug/observatory/LDEA/most/trafficked/drugs/page/', views.ldea_trafficked_drugs_page, name='trafficked_drugs'),
    path('national/drug/observatory/LDEA/most/drug/hotspots/page/', views.ldea_drug_hotspots_page, name='drug_hotspots'),
    path('national/drug/observatory/LDEA/new/substances/page/', views.ldea_new_substances_page, name='new_substances'),
    
    #===============================================================================================
    #                                  LDEA/head page Urls
    #===============================================================================================
    path('national/drug/observatory/LDEA/ops/page', views.ldea_ldea_ops_page, name='ldea_ops_home'),
    path('national/drug/observatory/LDEA/ops/active/cases', views.ldea_ldea_ops_active_cases, name='active_cases'),
        
         
    #===============================================================================================
    #                                   LDEA Officers Urls
    #===============================================================================================
    path('national/drug/observatory/LDEA/officers/page', views.ldea_officers_page, name='officers_home'),
    # LDEA Officers Create and view Arrests Person
    path('national/drug/observatory/LDEA/officers/create/arrests/person/', views.ldea_ceates_arrests_person_page, name='ceate_arrests_person'),
    path('national/drug/observatory/view/arrests/person', views.ldea_view_arrests_person_page, name='view_arrests_person'),
    path('national/drug/observatory/LDEA/view/arrests/person/detail/<str:id>/', views.ldea_officers_arrests_person_detail, name='arrests_person_detail'),
    path('national/drug/observatory/LDEA/view/arrests/', views.ldea_ceates_arrests_page, name='ceart_arrests'),   
    path('national/drug/observatory/LDEA/officers/creat/victim/history', views.ldea_ceates_victim_history, name='create_victim_history'),
    
    # LDEA Officers Create and view Cases 
    path('national/drug/observatory/LDEA/officers/create/cases', views.ldea_officers_create_cases, name='create_case'),
    path('national/drug/observatory/LDEA/officers/view/cases', views.ldea_officers_view_cases, name='view_case'),
    path('national/drug/observatory/LDEA/officers/view/cases/detail <str:id>/', views.ldea_officers_cases_detail, name='cases_detail'),    
    path('national/drug/observatory/LDEA/officers/edit/cases/ <str:id>/', views.ldea_officers_edit_cases, name='edit_cases'),    
    # LDEA Officers Create and view Evidence 
    path('national/drug/observatory/LDEA/officers/create/evidence', views.ldea_officers_create_evidence, name='create_evidence'),
    path('national/drug/observatory/LDEA/officers/edit/evidence/<str:id>/', views.ldea_officers_edit_evidence, name='edit_evidence'),
    path('national/drug/observatory/LDEA/officers/view/evidence', views.ldea_officers_view_evidence, name='view_evidence'),
    # LDEA Officers Create and View Drug Raid Operations
    path('national/drug/observatory/LDEA/officers/create/drug/raid', views.ldea_officers_crate_drug_raid, name='crate_drug_raid'),
    path('national/drug/observatory/LDEA/officers/view/drug/raid', views.ldea_officers_view_drug_raid, name='view_drug_raid'),
    path('national/drug/observatory/LDEA/officers/edit/drug/raid/ <str:id>/', views.ldea_officers_edit_drug_raid, name='edit_drug_raid'),
    
    # LDEA Officers Create and View Seizure
    path('national/drug/observatory/LDEA/officers/create/drug/seizure', views.ldea_officers_create_seizure, name='crate_drug_seizure'),
    path('national/drug/observatory/view/drug/seizure', views.ldea_officers_view_seizure, name='view_drug_seizure'),
    path('national/drug/observatory/LDEA/officers/edit/drug/seizure/ <str:id>/', views.ldea_officers_edit_drug_seizure, name='edit_drug_seizure'),
    
    # LDEA Officers New Drug Raid
    path('national/drug/observatory/LDEA/officers/create/new/drug/', views.ldea_officers_login_new_drug, name='crate_new_drug'),
    path('national/drug/observatory/LDEA/officers/view/new/drug/', views.ldea_officers_view_new_drug, name='view_new_drug'),
    path('national/drug/observatory/LDEA/officers/edit/new/drug/ <str:id>/', views.ldea_officers_edit_new_drug, name='edit_new_drug'),    
]