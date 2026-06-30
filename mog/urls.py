from django.urls import path
from . import views  

urlpatterns = [
    path('national/drug/observatory/MoG/head/page', views.mog_head_home, name='mog_head_home'),
    
    
    path('national/drug/observatory/MoG/officers/page', views.moh_officers_home, name='mog_officers_home'),
    
    path('national/drug/observatory/MoG/officers/creat/initial/assessment/form', views.mog_officers_creat_initial_assessment_form, name='creat_initial_assessment_form'),
    path('national/drug/observatory/MoG/officers/view/initial/assessment/form', views.mog_officers_view_initial_assessment_form, name='view_initial_assessment_form'),
    path('national/drug/observatory/MoG/officers/detaile/initial/assessment/form <str:id>/', views.mog_officers_detaile_initial_assessment_form, name='detaile_initial_assessment_form'),  
    
    path('national/drug/observatory/MoG/officers/create/follow/form', views.mog_officers_create_follow_form, name='create_follow_form'),
    path('national/drug/observatory/MoG/officers/view/follow/form', views.mog_officers_view_follow_form, name='view_follow_form'),
    path('national/drug/observatory/MoG/officers/detail/follow/form <str:id>/', views.mog_officers_detail_follow_form, name='detail_follow_form'),  
    
    path('national/drug/observatory/MoG/officers/creat/parent/guardian/verification', views.moh_officers_creat_parent_guardian_verification, name='parent_guardian_verification'),
    path('national/drug/observatory/MoG/officers/view/parent/guardian/verification', views.moh_officers_view_parent_guardian_verification, name='view_parent_guardian_verification'),
    path('national/drug/observatory/MoG/officers/detail/parent/guardian/verification <str:id>/', views.mog_officers_detail_parent_guardian_verification_form, name='detail_parent_guardian_verification'),
    
    path('national/drug/observatory/MoG/officers/creat/beneficiary/verification', views.moh_officers_creat_beneficiary_verification, name='creat_beneficiary_verification'),
    path('national/drug/observatory/MoG/officers/view/beneficiary/verification', views.moh_officers_view_beneficiary_verification, name='view_beneficiary_verification'),
    path('national/drug/observatory/MoG/officers/detail/beneficiary/verification <str:id>/', views.mog_officers_detail_beneficiary_verification_form, name='detail_beneficiary_verification'),
    
    path('national/drug/observatory/MoG/officers/creat/beneficiary/handover', views.moh_officers_creat_beneficiary_handover, name='creat_beneficiary_handover'),
    path('national/drug/observatory/MoG/officers/view/beneficiary/handover', views.moh_officers_view_beneficiary_handover, name='view_beneficiary_handover'),
    path('national/drug/observatory/MoG/officers/detail/beneficiary/handover <str:id>/', views.mog_officers_detail_beneficiary_handover_form, name='detail_beneficiary_handover'),
    
    path('national/drug/observatory/MoG/officers/creat/tracing/action/taken', views.moh_officers_creat_tracing_action_taken, name='creat_tracing_action_taken'),
    path('national/drug/observatory/MoG/officers/view/tracing/action/taken', views.moh_officers_view_tracing_action_taken, name='view_tracing_action_taken'),
    path('national/drug/observatory/MoG/officers/detail/tracing/action/taken <str:id>/', views.mog_officers_detail_tracing_action_taken, name='detail_tracing_action_taken'),
    
    path('national/drug/observatory/MoG/officers/creat/community/level/report', views.mog_officers_creat_community_level_report, name='creat_community_Level_report'),
    path('national/drug/observatory/MoG/officers/view/community/level/report', views.moh_officers_view_community_level_report, name='view_community_Level_report'),
    path('national/drug/observatory/MoG/officers/detail/community/level/report <str:id>/', views.mog_officers_detail_community_level_report, name='detail_community_Level_report'),
    
    path('national/drug/observatory/MoG/officers/creat/case/closure/form', views.mog_officers_creat_case_closure_form, name='creat_case_closure_form'),
    path('national/drug/observatory/MoG/officers/view/case/closure/form', views.mog_officers_view_case_closure_form, name='view_case_closure_form'),
    path('national/drug/observatory/MoG/officers/detail/case/closure/form <str:id>/', views.mog_officers_detail_case_closure_form, name='detail_case_closure_form'),
        
]