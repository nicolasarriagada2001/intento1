from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacto_view, name='formulario_contacto'),
]