from django.db import models
from django.contrib.auth.models import User
from cliente.models import Cliente
from administrador.models import *
from django.utils.timezone import now


class Corredor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agencia = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion_oficina = models.CharField(max_length=255, blank=True)
    licencia = models.CharField(max_length=50, blank=True)
    experiencia = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='corredores/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=now)

    created_by = models.ForeignKey(
        Administrador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='corredores_creados'
    )

    eliminado_por = models.ForeignKey(
        Administrador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='corredores_eliminados'
    )

    def __str__(self): 
        return self.user.username
    

class SeguimientoContacto(models.Model):
    # Opciones para tipo de campaña
    TIPO_CAMPAÑA = [
        ('atraccion', 'Atracción'),
        ('interaccion', 'Interacción'),
        ('conversion', 'Conversión'),
        ('fidelizacion', 'Fidelización'),
        ('ninguna', 'Ninguna'),
    ]

    # Opciones para estado del contacto
    ESTADO_CONTACTO = [
        ('no_contactado', 'No contactado'),
        ('llamada', 'Llamada'),
        ('interesado', 'Interesado'),
        ('no_interesado', 'No interesado'),
        ('reunion', 'Reunión'),
        ('cierre', 'Cierre'),
        ('pendiente', 'Pendiente'),
        ('ninguna', 'Ninguna'),
    ]

    fecha = models.DateField(auto_now_add=True)
    corredor = models.ForeignKey(Corredor, on_delete=models.CASCADE, related_name='seguimientos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='seguimientos')
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='seguimientos')

    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    tipo_campaña = models.CharField(max_length=20, choices=TIPO_CAMPAÑA, default='ninguna')
    estado = models.CharField(max_length=20, choices=ESTADO_CONTACTO, default='no_contactado')

    descripcion = models.TextField(blank=True, null=True)
    
    fecha_contacto = models.DateField(blank=True, null=True)
    fecha_siguiente = models.DateField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)

    def finalizar(self):
        """Marca o desmarca la fecha de cierre."""
        if self.fecha_cierre:
            self.fecha_cierre = None
        else:
            self.fecha_cierre = timezone.now().date()
        self.save()

    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()} ({self.propiedad.titulo})"