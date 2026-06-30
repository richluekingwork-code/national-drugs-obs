"""
URL configuration for national_drug_obs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    
Develop By: 
    Charles E S Boimah
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    # ------------------ Admin Urls ------------------------
    path('admin/', admin.site.urls), 
    
    # ------------------ Accoubts App Urls ------------------------
    path('', include('accounts.urls')),
    path('', include('ldea.urls')),
    path('', include('moj.urls')),
    path('', include('moh.urls')),
    path('', include('mog.urls')),
     
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
