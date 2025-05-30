from django.contrib import admin
from .models import *

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'activo', 'eliminado']

    def get_username(self, obj):
        return obj.usuario.username
    get_username.short_description = 'Usuario'

@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'administrador', 'estado', 'valor', 'visibilidad', 'estado_tramitacion', 'activo']
    list_filter = ['estado', 'estado_tramitacion', 'visibilidad']
    search_fields = ['titulo', 'descripcion']

@admin.register(ImagenPropiedad)
class ImagenPropiedadAdmin(admin.ModelAdmin):
    list_display = ['get_propiedad', 'imagen']

    def get_propiedad(self, obj):
        return obj.propiedad.titulo
    get_propiedad.short_description = 'Propiedad'


admin.site.register(CaracteristicaPropiedad)