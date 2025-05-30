from django import forms
from .models import formulario

class ContactoForm(forms.ModelForm):
    class Meta:
        model = formulario
        fields = ['nombre','correo','rut', 'telefono', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Tu correo electrónico'}),
            'rut': forms.NumberInput(attrs={'placeholder': 'Tu Rut'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Tu Numero de Contacto'}),
            'asunto': forms.TextInput(attrs={'placeholder': 'Asunto'}),
            'mensaje': forms.Textarea(attrs={'placeholder': 'Tu mensaje', 'rows': 5}),
        }