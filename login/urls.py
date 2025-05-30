from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/cliente/', views.registro_cliente, name='registro_cliente'),
    path('registro/dueno/', views.registro_dueno, name='registro_dueno'),
]
