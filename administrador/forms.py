from django import forms
from .models import *
from corredor.models import Corredor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['titulo', 'descripcion', 'estado', 'valor', 'estado_tramitacion', 'fecha_inicio', 'fecha_termino', 'visibilidad']


class PropiedadImagenForm(forms.ModelForm):
    class Meta:
        model = ImagenPropiedad
        fields = ['imagen']

class PropiedadFormSinActivo(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['titulo', 'descripcion', 'estado', 'valor']


class PropiedadFormSinActivoCorredor(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['titulo', 'descripcion', 'estado', 'valor', 'estado_tramitacion', 'fecha_inicio', 'fecha_termino']


class CorredorForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Corredor
        exclude = ['user', 'created_by', 'fecha_creacion']

    def save(self, admin, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        corredor = super().save(commit=False)
        corredor.user = user
        corredor.created_by = admin
        if commit:
            corredor.save()
        return corredor