from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index_corredor'),
    path('crear_propiedades/', views.crear_propiedades, name='crear_propiedades'),
    path('propiedad/<int:propiedad_id>/', views.detalle_propiedad, name='detalle_propiedad_corredor'),
    path('mensajes_publico_corredor/', views.mensajes_publico_corredor, name='mensajes_publico_corredor'),  
    path('mensajes_privada_corredor/', views.mensajes_privado_corredor, name='mensajes_privado_corredor')

    
    
]
