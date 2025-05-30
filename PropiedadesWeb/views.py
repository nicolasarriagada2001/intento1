from django.shortcuts import render
from login.estructuradoAuth import *
from decimal import Decimal
import requests


def base(request):
    return render(request, 'base.html', {

    })

def inicio(request):

    # dolar = euro = uf = "Cargando Valores.."
    # iva = Decimal('19.00')

# ////////////////////////////////////////////////////////////////////////
    # try:
    #     respuesta = requests.get("https://mindicador.cl/api", timeout=1)
    #     if respuesta.status_code == 200:
    #         dato_respuesta = respuesta.json()
    #         dolar = dato_respuesta["dolar"]["valor"]
    #         euro = dato_respuesta["euro"]["valor"]
    #         uf = dato_respuesta["uf"]["valor"]
    # except Exception as e:
    #     print("No se Pudo Acceder a la Api-Valor-Mercado:", e)

    return render(
        request, 'inicio.html',{
        # 'dolar': 1,
        # 'euro': euro,
        # 'uf': uf,
        # 'iva': iva,
        # 'clp': dolar,
        }
    )

def login(request):
    return render(
        request, 'login.html',
    )
    
def registro_cliente(request):
    return render(
        request, 'registro_cliente.html',
    )

def registro_dueno(request):
    return render(
        request, 'registro_dueno.html',
    )


def login_admin(request):
    return render(
        request, 'administrador/login_admin.html',
    )
    
    
