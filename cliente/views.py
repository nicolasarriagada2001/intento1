from decimal import Decimal
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.core.paginator import Paginator

from login.estructuradoAuth import clienteAuth
from administrador.models import Propiedad
from .models import *
from .forms import ClienteForm

@clienteAuth('cliente')
@login_required  
def pagina(request):
    return render(request, 'pagina/pagina.html')

@clienteAuth('cliente')
@login_required  
def index_cliente(request):
    dolar = euro = uf = "Cargando Valores.."
    iva = Decimal('19.00')

    try:
        cliente = request.user.cliente
    except Exception:
        cliente = None


    propiedades_lista = Propiedad.objects.filter(activo=True).order_by('-fecha_publicacion')
    paginator = Paginator(propiedades_lista, 8)
    pagina = request.GET.get('page')
    propiedades = paginator.get_page(pagina)

    try:
        respuesta = requests.get("https://mindicador.cl/api", timeout=1)
        if respuesta.status_code == 200:
            dato_respuesta = respuesta.json()
            dolar = dato_respuesta["dolar"]["valor"]
            euro = dato_respuesta["euro"]["valor"]
            uf = dato_respuesta["uf"]["valor"]
    except Exception as e:
        print("No se pudo acceder a la API de valores de mercado:", e)

    return render(request, 'cliente/index.html', {
        'cliente': cliente,
        'propiedades': propiedades,
        'dolar': dolar,
        'euro': euro,
        'uf': uf,
        'iva': iva,
        'clp': dolar,
    })
# ////////////////////////////////////////////////////////////////////////

# @clienteAuth('cliente')
# @login_required   
def detalle_propiedad_cliente(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    if propiedad.activo:
        return render(request, 'propiedadCli/detalle_propiedad.html', {'propiedad': propiedad})
    return render(request, 'propiedadCli/propiedad_no_activa.html', {'propiedad': propiedad})


@clienteAuth('cliente')
@login_required 
def galeria_propiedad(request):
    return render(request, 'lista-propiedades/galeriaPropiedad.html')

@clienteAuth('cliente')
@login_required 
def config_cliente(request):
    return render(request, 'config/configCliente.html')

@clienteAuth('cliente')
@login_required 
def perfil(request):
    cliente = getattr(request.user, 'cliente', None)
    if not cliente:
        messages.warning(request, "No tienes perfil de cliente asociado.")
    return render(request, 'perfil/perfil.html', {'cliente': cliente})

@clienteAuth('cliente')
@login_required 
def nav_cliente(request):
    return render(request, 'nav_cliente/nav_cliente.html')


# //////////////////////////////////////////////////////////////////////////////////////////


def detalle_propiedad(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)
    imagenes = propiedad.imagenes.all()

    interes_del_usuario = False
    if request.user.is_authenticated:
        interes_del_usuario = ContactoClientePropiedad.objects.filter(cliente=request.user, propiedad=propiedad).exists()

    return render(request, 'propiedadCli/detalle_propiedad.html', {
        'propiedad': propiedad,
        'imagenes': imagenes,
        'interes_del_usuario': interes_del_usuario
    })

def registrar_interes(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)
    cliente = request.user

    contacto_existente = ContactoClientePropiedad.objects.filter(cliente=cliente, propiedad=propiedad).first()
    if not contacto_existente:
        ContactoClientePropiedad.objects.create(cliente=cliente, propiedad=propiedad)

    return redirect('cliente_detalles_propiedad', id=id)

def cancelar_interes(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)
    cliente = request.user

    contacto = ContactoClientePropiedad.objects.filter(cliente=cliente, propiedad=propiedad).first()
    if contacto:
        contacto.delete()

    return redirect('cliente_detalles_propiedad', id=id) 

# //////////////////////////////////////////////////////////////////////////////////////////

def actualizar_cli(request, id):
    cliente = get_object_or_404(Cliente, user=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_index')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'perfil/actualizar_cli.html', {'form': form})


