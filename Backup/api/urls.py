from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from . import views

urlpatterns = [
 
    path('upload/', views.upload_pdf_view, name ='upload_file'), 
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('login/', views.login_view, name='api-login'),
    path('register/', views.register, name='register'),
    path('whoami/', views.whoami_view, name='api-whoami'),
    path('get_files/',views.list_files,name='get_files'),
    path('server_pdf/', views.server_pdf, name='server_pdf'),
    path('logout/', views.logout_view, name='logout'),
   
    path('', views.FrontendAppView.as_view(), name='home'),
    path('summarise/', views.summarise_information, name='summarise_text'),
    path('map/', views.map_data, name='map_data'),
    path('recommend/', views.recommend, name='recommend'),
]
