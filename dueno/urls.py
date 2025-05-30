from django.urls import path
from . import views



urlpatterns = [
    path('index/', views.index, name='dueno_index'),
    path('crear_propiedad/', views.registrar_propiedad, name='crear_propiedad'),  
    path('listar_propiedad/', views.listar_propiedad, name='listar_propiedad'),
    path('detalle_propiedad/<int:propiedad_id>/', views.detalle_propiedad, name='detalle_propiedad'),
    path('mis_propiedad/', views.mis_propiedad, name='mis_propiedad'),
    path('panel_tramites/', views.panel_tramites, name='panel_tramites'),
# ////////////////////////////////////////////////////////////////////

    path('lista/', views.lista_items, name='lista'),
    path('crear/', views.crear_item, name='crear'),
    path('actualizar/<int:pk>/', views.actualizar_item, name='actualizar'),
    path('eliminar/<int:pk>/', views.eliminar_item, name='eliminar'),

# /////////////////////////////////////////////////////////////////////

    path('listaDocu/', views.lista_documentos, name='listaDocu'),
    path('subir/', views.subir_documento, name='subir'),
    path('eliminarDocu/<int:pk>/', views.eliminar_documento, name='eliminarDocu'),

# /////////////////////////////////////////////////////////

]
