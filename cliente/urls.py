from django.urls import path
from . import views
from django.conf.urls.static import static
from PropiedadesWeb import settings

urlpatterns = [
    path('index/', views.index_cliente, name='cliente_index'),
    path('lista-propiedades/', views.galeria_propiedad, name='galeria_propiedad'),
    path('config/', views.config_cliente, name='configCliente'),
    path('nav_cliente/', views.nav_cliente, name='nav_cliente'),
    
    path('detalles_propiedad/<int:id>/', views.detalle_propiedad, name='cliente_detalles_propiedad'),

    path('actualizar_cli/<int:id>/', views.actualizar_cli, name='actualizar_cli'),
    path('pagina/', views.pagina, name='pagina'),

    path('detalles_propiedad/<int:id>/interes/', views.registrar_interes, name='registrar_interes'),
    path('detalles_propiedad/<int:id>/cancelar/', views.cancelar_interes, name='cancelar_interes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)