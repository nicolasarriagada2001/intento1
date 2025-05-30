from django.db import models
from django.contrib.auth.models import User
from administrador.models import Propiedad

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    telefono = models.CharField(max_length=15, blank=True)
    documento = models.FileField(upload_to='documentos/clientes/', null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
    
class ContactoClientePropiedad(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    fecha_contacto = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.username} interesado en {self.propiedad.titulo}"

    def get_email(self):
        try:
            return self.cliente.cliente.email
        except Cliente.DoesNotExist:
            return self.cliente.email

    def get_telefono(self):
        try:
            return self.cliente.cliente.telefono
        except Cliente.DoesNotExist:
            return "Sin número"
        
    def get_estado_propiedad(self):
        return self.propiedad.estado
