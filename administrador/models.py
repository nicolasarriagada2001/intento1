from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) 
    activo = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username

estado_publicado = [
    ('vender', 'Vender'),
    ('arriendo', 'Arriendo'),
]

estado_tramites = [
    ('pendiente', 'Pendiente'),
    ('en_proceso', 'En Proceso'),
    ('completado', 'Completado'),
]

estado_visible = [
    ('visible', 'Visible'),
    ('oculto', 'Oculto'),
]

estado_activo = [
    (True, 'Activo'),
    (False, 'Inactivo'),
]

estado_tipo_propiedad = [
    ('casa', 'Casa'),
    ('departamento', 'Departamento'),
    ('terreno', 'Terreno'),
]

class Propiedad(models.Model):
    administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE, null=True, blank=True)
    corredor = models.ForeignKey('corredor.Corredor', on_delete=models.CASCADE, null=True, blank=True)
    dueno = models.ForeignKey('dueno.Dueno', on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, null=True, blank=True)

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, choices=estado_publicado)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    estado_tramitacion = models.CharField(max_length=20, choices=estado_tramites, default='pendiente')
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    visibilidad = models.CharField(max_length=10, choices=estado_visible, default='visible')
    activo = models.BooleanField(default=False, choices=estado_activo)

    def valor_sin_iva(self):
        iva = Decimal('19.00')
        return self.valor / (Decimal('1.00') + (iva / Decimal('100.00')))

    def __str__(self):
        return self.titulo

class ImagenPropiedad(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='imagenes_propiedades/')

    def __str__(self):
        return f"Imagen de {self.propiedad.titulo}"

class CaracteristicaPropiedad(models.Model):
    propiedad = models.OneToOneField(Propiedad, on_delete=models.CASCADE, related_name='caracteristicas')
    informacion_dueno = models.TextField(max_length=255)
    direccion = models.CharField(max_length=100)
    color_general = models.CharField(max_length=100)
    superficie_terreno = models.IntegerField()
    metros_cuadrados = models.IntegerField()
    habitacion = models.IntegerField()
    estacionamiento = models.IntegerField()
    cocina = models.IntegerField()
    sala = models.IntegerField()
    pisos = models.IntegerField()
    tipo_propiedad = models.CharField(max_length=30, choices=estado_tipo_propiedad, default='casa')

    def __str__(self):
        return f"Las Caracteristicas de la Propiedad: {self.propiedad.titulo}"
    

TIPO_DOCUMENTO = [
    ('titulo_dominio', 'Título de dominio'),
    ('cert_dominio_vigente', 'Certificado de dominio vigente'),
    ('cert_hipotecas', 'Certificado de hipotecas y gravámenes'),
    ('recepcion_final', 'Recepción final'),
    ('cert_gastos_comunes', 'Certificado de gastos comunes'),
    ('otros', 'Otros'),
]

class DocumentoPropiedad(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=50, choices=TIPO_DOCUMENTO)
    archivo = models.FileField(upload_to='documentos_propiedades/')
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.propiedad.titulo}"

class ComunicacionCorredor(models.Model):
        propiedad_mensaje = models.OneToOneField(Propiedad, on_delete=models.CASCADE, related_name='comunicacionCorredor')
        dueno = models.ForeignKey('dueno.Dueno', on_delete=models.CASCADE, null=True, blank=True)
        corredor = models.ForeignKey('corredor.Corredor', on_delete=models.CASCADE, null=True, blank=True)
        administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE, null=True, blank=True)

        
# ////////////////////////////////////////////////////////////////////////////////////



estado_error_tramite = [
    ('Sin-Errores!', 'sin-errores!'),
    ('No-Se-Pudo-Realizar', 'No-Se-Pudo-Realizar'),
    ('Se-Pudo-Finalizar-La-Tramitacion', 'se-pudo-finalizar-la-tramitacion'),
    ('Se-ReAbre-Tramitacion', 'se-reabre-tramitacion'),
]

estado_proceso_pago = [
    ('deposito-aceptado', 'Deposito-Aceptado'),
    ('deposito-rechazado', 'Deposito-Rechazado'),
    ('deposito-en-proceso', 'Deposito-En-Proceso'),
]

estado_final_pago = [
    ('Finalizado', 'finalizado'),
    ('NO-Finalizado', 'no-finalizado')
]

class Pagos(models.Model):

    administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE, null=True, blank=True)
    corredor = models.ForeignKey('corredor.Corredor', on_delete=models.CASCADE, null=True, blank=True)
    dueno = models.ForeignKey('dueno.Dueno', on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, null=True, blank=True)
    propiedad = models.OneToOneField(Propiedad, on_delete=models.CASCADE, related_name='pagoPropiedad')

    titulo_tramite = models.CharField(max_length=255)
    estipulacion_final = models.TextField()
    estado_proceso_pago = models.CharField(max_length=50, choices=estado_proceso_pago)
    valor = models.DecimalField(max_digits=50, decimal_places=0)
    estado_final_pago = models.CharField(max_length=50, choices=estado_final_pago, default='NO-Pagado')
    estado_error_tramite = models.CharField(max_length=50, choices=estado_error_tramite, default='Sin-Errores!')
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()


class Proceso_pago(models.Model):
    propiedad = models.OneToOneField(Propiedad, on_delete=models.CASCADE, related_name='procesoPagoPropiedad')
    corredor = models.ForeignKey('corredor.Corredor', on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, null=True, blank=True)


# ///////////////////////////////////////////////////////////////////////////////////////////
# mensajes

# from django.db import models
# from django.utils import timezone

# class Mensaje(models.Model):
#     emisor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='mensajes_enviados')
#     receptor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='mensajes_recibidos')
#     asunto = models.CharField(max_length=255)
#     contenido = models.TextField()
#     fecha_envio = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"Mensaje de {self.emisor.username} a {self.receptor.username}"
