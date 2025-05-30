from django.contrib import admin
from django.urls import path, include
from PropiedadesWeb import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.inicio, name="inicio"),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('administrador/', include('administrador.urls')),
    path('cliente/', include('cliente.urls')),
    path('corredor/', include('corredor.urls')),
    path('dueno/', include('dueno.urls')),
    path('contacto/', include('formContacto.urls')), 
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)