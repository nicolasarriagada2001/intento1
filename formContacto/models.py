from django.db import models

class formulario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    rut = models.CharField(max_length=11)
    telefono = models.CharField(max_length=11)
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"