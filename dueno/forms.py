from django import forms
from .models import Dueno
from .models import MultimediaItem
import os
from django.contrib.auth.models import User
from administrador.models import CaracteristicaPropiedad, Propiedad, DocumentoPropiedad
from django.forms import ValidationError, modelformset_factory


class DuenoRegistroForm(forms.ModelForm):
    username = forms.CharField(label='Nombre Usuario', max_length=150)
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    rut = forms.CharField(label='Ingrese su Rut sin (.) puntos ni (-) guion')
    acepto_terminos = forms.BooleanField(label='Acepto los términos y condiciones')
    documento = forms.FileField(required=False)

    class Meta:
        model = Dueno
        fields = ['nombre_completo', 'telefono', 'tipo_dueno', 'intencion', 'rut', 'documento']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

# ////////////////////////////////////////////////////////////////////Borrar todo dedes aqui!!


class MultimediaForm(forms.ModelForm):
    class Meta:
        model = MultimediaItem
        fields = '__all__'



# /////////Documentos a Trabajar!!!
# MODELOS DEL APP EXTERNO!!!
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'archivo', 'tipo']

    def clean(self):
        cleaned_data = super().clean()
        archivo = cleaned_data.get('archivo')
        tipo = cleaned_data.get('tipo')  # 'IMG' o 'PDF'

        if archivo and tipo:
            ext = os.path.splitext(archivo.name)[1].lower()
            imagenes_permitidas = ['.jpg', '.jpeg', '.png', '.webp']
            if tipo == 'PDF' and ext != '.pdf':
                raise forms.ValidationError("Debes subir un archivo con extensión .pdf.")
            elif tipo == 'IMG' and ext not in imagenes_permitidas:
                raise forms.ValidationError("Debes subir una imagen (.jpg, .jpeg, .png, .webp).")

        return cleaned_data
    


class PropiedadFormDueno(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = [
            'titulo', 'descripcion', 'estado', 'valor',
            'fecha_inicio', 'fecha_termino',
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
        }

class CaracteristicaForm(forms.ModelForm):
    class Meta:
        model = CaracteristicaPropiedad
        fields = [
            'informacion_dueno', 'direccion', 'color_general',
            'superficie_terreno', 'metros_cuadrados',
            'habitacion', 'estacionamiento', 'cocina', 'sala', 'pisos',
            'tipo_propiedad'
        ]

# Formset que no requiere que todos los campos estén completos
DocumentoFormSet = modelformset_factory(
    DocumentoPropiedad,
    fields=('tipo', 'archivo', 'descripcion'),
    extra=5,
    can_delete=False,
    widgets={
        'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
    }
)