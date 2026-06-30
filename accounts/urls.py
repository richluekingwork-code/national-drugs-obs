from django.urls import path
from . import views  

urlpatterns = [
    # ------------------ Logs Urls ------------------------
    path('', views.dologin, name='dologin'),
    path('national/drug/observatory/logout/', views.delogout, name='logout'),
    
    path('dashboard/redirect/', views.role_based_redirect, name='role_based_redirect'),
    
    # ------------------ User Profile Urls ------------------------
    path('hse/user/profile/page', views.profile, name='profile'),
    
    path('hse/user/my/account/page', views.my_account, name='my_account'),
    
]

# Health check for Sevalla
urlpatterns += [
    path('ht/', views.health_check, name='health_check'),
]