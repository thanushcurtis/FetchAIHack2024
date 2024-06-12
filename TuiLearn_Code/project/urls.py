from django.conf import settings
from django.contrib import admin
from django.urls import include, path
#from django.http import HttpResponse
from django.conf.urls.static import static
from django.views.generic import TemplateView
 
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import login_view
handler404 = 'api.views.custom_404'

urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/', include('api.urls')),   
        #path('auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('auth/', login_view, name='login'),
      path('', TemplateView.as_view(template_name='index.html'), name='home'),
     # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
