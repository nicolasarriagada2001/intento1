from django import forms
from administrador.models import Propiedad, ImagenPropiedad, CaracteristicaPropiedad  
from .models import *

class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        exclude = ['activo']
       

class ImagenForm(forms.ModelForm):
    class Meta:
        model = ImagenPropiedad
        fields = ['imagen']

class CaracteristicaForm(forms.ModelForm):
    class Meta:
        model = CaracteristicaPropiedad 
        exclude = ['propiedad']



class SeguimientoContactoForm(forms.ModelForm):
    class Meta:
        model = SeguimientoContacto
        fields = [
            'corredor', 'cliente', 'propiedad',
            'nombre', 'telefono', 'correo',
            'tipo_campaña', 'estado', 'descripcion',
            'fecha_contacto', 'fecha_siguiente', 'fecha_cierre'
        ]
        widgets = {
            'fecha_contacto': forms.DateInput(attrs={'type': 'date'}),
            'fecha_siguiente': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cierre': forms.DateInput(attrs={'type': 'date'}),
        }