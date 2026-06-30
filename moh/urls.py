from django.urls import path
from . import views  

urlpatterns = [
    # ------------------ Logs Urls ------------------------
    #===============================================================================================
    #                                   Moj Head page Urls
    #===============================================================================================
    path('national/drug/observatory/moh/head/home/', views.moh_head_home, name='moh_head_home'),
    path('national/drug/observatory/view/chat/report/', views.moh_view_chat_report, name='view_chat_report'),
    path('national/drug/observatory/view/detail/report/', views.moh_view_detail_report, name='view_detail_report'),
    path('national/drug/observatory/detail/report/ <str:id>/', views.moh_detail_report, name='detail_report'),
    
    #===============================================================================================
    #                                   Moj Officers page Urls
    #===============================================================================================
    path('national/drug/observatory/moh/officers/home/', views.moh_officers_home, name='moh_officers_home'),
    path('national/drug/observatory/moh/officers/create_beneficial/', views.moh_officers_create_beneficial, name='create_beneficial'), 

    
    path('national/drug/observatory/moh/officers/demand_reduction/', views.moh_officers_demand_reduction, name='demand_reduction'),
    path('national/drug/observatory/view/demand_reduction/', views.moh_officers_view_demand_reduction, name='view_demand_reduction'),
    path('national/drug/observatory/demand_reduction/detail/<str:id>/', views.moh_officers_demand_reduction_detail, name='demand_reduction_detail'),
    
    
    path('national/drug/observatory/creat/prevention/', views.moh_officers_creat_prevention, name='creat_prevention'),
    path('national/drug/observatory/view/prevention/', views.moh_officers_view_prevention, name='view_prevention'),
    path('national/drug/observatory/view/prevention/<int:id>/', views.moh_officers_view_prevention_detail, name='prevention_detail'),
    
    path('national/drug/observatory/creat/treatment/facility/', views.moh_officers_creat_treatment_facility, name='creat_treatment_facility'),
    path('national/drug/observatory/view/treatment/facility/', views.moh_officers_view_treatment_facility, name='view_treatment_facility'),
] 