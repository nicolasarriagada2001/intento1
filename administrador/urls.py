from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index_administrador'),
    path('panel_admin/', views.panel_admin, name='panel_admin'),
    path('crear_propiedades/', views.crear_propiedades, name='propiedad_creada'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('logout_admin/', views.logout_view, name='logout_admin'),
    path('listar_propiedades/', views.listar_propiedades, name='listar_propiedades'),
    path('detalles_propiedad/<int:propiedad_id>/', views.detalles_propiedad, name='detalles_propiedad'),
    path('buzon_mensaje/', views.buzon_mensaje, name='buzon_mensaje'),
    path('lista_general_cli_corr/', views.lista_general_cli_corr, name='lista_general_cli_corr'),
    path('panel/corredores/', views.panel_corredores, name='panel_corredores'),
    path('bloquear_corredor/<int:corredor_id>/', views.bloquear_corredor, name='bloquear_corredor'),
    path('eliminar_corredor/<int:corredor_id>/', views.eliminar_corredor, name='eliminar_corredor'),
]
