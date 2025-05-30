from django.db import models
from django.contrib.auth.models import User

from PIL import Image
import fitz  # -pip install django pillow pymupdf
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone

from administrador.models import Propiedad



class Dueno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    tipo_dueno = models.CharField(max_length=20, choices=[('persona', 'Persona'), ('empresa', 'Empresa')])
    intencion = models.CharField(max_length=20, choices=[('vender', 'Vender'), ('arrendar', 'Arrendar')])
    rut = models.CharField(max_length=20)
    documento = models.FileField(upload_to='documentos/', blank=True, null=True)


    def __str__(self):
        return self.nombre_completo
    
# ////////////////////////////////////////////////////////////////////

class MultimediaItem(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.titulo
    

class Documento(models.Model):

    TIPOS = [
    ('IMG', 'Imagen'),
    ('PDF', 'PDF'),
]

    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='documentos/')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    
    kb = models.FloatField(null=True, blank=True)
    fecha_carga_doc = models.DateTimeField(default=timezone.now) 
    


    def __str__(self):
        return self.titulo or os.path.basename(self.archivo.name)
    
# /////////////////////////////////////////////////////////////
# mensajes del dueño a usuarios base

class DocumentoPropiedades(models.Model):
        propiedad = models.OneToOneField(Propiedad, on_delete=models.CASCADE, related_name='documentoPropiedad')
        dueno = models.ForeignKey('dueno.Dueno', on_delete=models.CASCADE, null=True, blank=True)
