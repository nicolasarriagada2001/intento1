from django.core.paginator import Paginator
from django.db.models import Sum
from decimal import Decimal

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.http import HttpResponse
from login.estructuradoAuth import adminAuth 
from cliente.models import Cliente
from corredor.models import Corredor
import requests
from formContacto.models import formulario
from cliente.models import *
from dueno.models import Dueno

@adminAuth('administrador')
@login_required  
def index(request):
# ////////////////////////////////////////////////////////////////////////////

    


# ///////////////////////////////////////////////////////////////////////////////9/
    conteo_total_solicitan_propiedad = ContactoClientePropiedad.objects.all().count()
    conteo_total_tipo_propiedad_solicitada_casa = ContactoClientePropiedad.objects.filter(propiedad__caracteristicas__tipo_propiedad="casa").values('propiedad_id').distinct().count()
    conteo_total_tipo_propiedad_solicitada_depa = ContactoClientePropiedad.objects.filter(propiedad__caracteristicas__tipo_propiedad="departamento").values('propiedad_id').distinct().count()
    conteo_total_tipo_propiedad_solicitada_terreno = ContactoClientePropiedad.objects.filter(propiedad__caracteristicas__tipo_propiedad='terreno').values('propiedad_id').distinct().count()

    conteo_total_propiedades = Propiedad.objects.all().count()
    conteo_total_propiedades_solicitadas = ContactoClientePropiedad.objects.filter().values('propiedad_id').distinct().count()
    total_casa = Propiedad.objects.filter(caracteristicas__tipo_propiedad="casa").values('id').distinct().count()
    total_depto = Propiedad.objects.filter(caracteristicas__tipo_propiedad="departamento").values('id').distinct().count()
    total_terreno = Propiedad.objects.filter(caracteristicas__tipo_propiedad="terreno").values('id').distinct().count()

    total_cliente = Cliente.objects.all().count()
    if total_cliente:
        print(":", total_cliente)
# /////////////////////////////////////////////////

    propiedades_lista = Propiedad.objects.all().order_by('-fecha_publicacion')
    paginator = Paginator(propiedades_lista, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    interesados_por_propiedad = {}
    for propiedad in page_obj:
        interesados = ContactoClientePropiedad.objects.filter(propiedad=propiedad)
        interesados_por_propiedad[propiedad.id] = interesados 


#///////////////////////////////////////////////////////////////////
#  
    propiedades = Propiedad.objects.select_related('administrador').all()
    clientes = Cliente.objects.select_related('user').order_by('-id')[:8]
    corredores = Corredor.objects.select_related('user').order_by('-id')[:8]
    total_valor = propiedades.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')

    dolar = euro = uf = "Cargando Valores.."
    iva = Decimal('19.00')
    total_sin_iva = total_valor / (Decimal('1.00') + (iva / Decimal('100.00')))

# ////////////////////////////////////////////////////////////////////////

    try:
        respuesta = requests.get("https://mindicador.cl/api", timeout=1)
        if respuesta.status_code == 200:
            dato_respuesta = respuesta.json()
            dolar = dato_respuesta["dolar"]["valor"]
            euro = dato_respuesta["euro"]["valor"]
            uf = dato_respuesta["uf"]["valor"]
    except Exception as e:
        print("No se Pudo Acceder a la Api-Valor-Mercado:", e)

# ///////////////////////////////////////////////////////////////////////
    formularios = formulario.objects.order_by('-fecha')
    paginator = Paginator(formularios, 10)

    numero_pagina = request.GET.get('pagina') 
    get_paginador = paginator.get_page(numero_pagina)
 

    try:
        admin = Administrador.objects.get(usuario=request.user)
    except Administrador.DoesNotExist:
        admin = None

    return render(request, 'administrador/index.html', {
        'conteo_total_propiedades_solicitadas' : conteo_total_propiedades_solicitadas,
        'conteo_total_propiedades' : conteo_total_propiedades,
        'conteo_total_tipo_propiedad_solicitada_casa' : conteo_total_tipo_propiedad_solicitada_casa,
        'conteo_total_tipo_propiedad_solicitada_depa' : conteo_total_tipo_propiedad_solicitada_depa,
        'conteo_total_tipo_propiedad_solicitada_terreno' : conteo_total_tipo_propiedad_solicitada_terreno,
        'total_cliente' : total_cliente,
        'total_casa' : total_casa,
        'total_terreno' : total_terreno,
        'total_depto' : total_depto,
        'conteo_total_solicitan_propiedad': conteo_total_solicitan_propiedad,
        # /////////////////////////
        'propiedades': propiedades,
        'clientes': clientes,
        'corredores': corredores,
        'total_valor': total_valor,
        'total_sin_iva': total_sin_iva,
        #///////////////////////////
        'dolar': 1,
        'euro': euro,
        'uf': uf,
        'iva': iva,
        'clp': dolar,
        # ///////////////////////////
        'get_paginador': get_paginador,
        # ///////////////////////////
        'admin' : admin,
        # ////////////////////////////
        'propiedades': page_obj,
        'interesados_por_propiedad': interesados_por_propiedad,

    })

@login_required
def panel_admin(request):
    publicaciones = Propiedad.objects.filter(administrador=request.user.administrador)
    return render(request, 'administrador/panel_admin.html', {
        'publicaciones': publicaciones,
        'administrador': request.user.administrador
    })


def crear_propiedades(request):
    if request.method == 'POST':
        propiedad_envio = PropiedadForm(request.POST, request.FILES)

        if propiedad_envio.is_valid():
            Propiedad = propiedad_envio.save(commit=False)
            Propiedad.administrador = request.user.administrador
            Propiedad.save()

            imagenes = request.FILES.getlist('images')
            if len(imagenes) < 3 or len(imagenes) > 15:
                return HttpResponse("<h1 style='color: red;'>Debe subir entre 3 y 14 imágenes.<h1>", status=400)

            for imagen in imagenes:
                ImagenPropiedad.objects.create(propiedad=Propiedad, imagen=imagen)
            return redirect('index_administrador') 

    else:
        propiedad_carga = PropiedadForm()
    return render(request, 'administrador/crear_propiedades.html', {'form': propiedad_carga})


def login_admin(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['username']
        passw = request.POST['password']
        usuario = authenticate(username=nombre_usuario, password=passw)
        if usuario is not None:
            try:
                admin = usuario.administrador
                if admin.activo and not admin.eliminado:
                    login(request, usuario)
                    return redirect('index_administrador') 
                else:
                    return HttpResponse("<h1 style='color: red;'>Este Administrador no está activo o está eliminado.<h1>", status=400)
            except Administrador.DoesNotExist:
                return HttpResponse("<h1 style='color: red;'>No es un Administrador Válido!.<h1>", status=400)
        else:
            return HttpResponse("<h1 style='color: red;'>Credenciales Incorrectas del Administrador!!.<h1>", status=400)
    return render(request, 'administrador/login_admin.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_admin') 


@login_required
@adminAuth('administrador') 
def listar_propiedades(request):
    propiedades = Propiedad.objects.filter(activo=True, visibilidad='visible')
    return render(request, 'administrador/listar_propiedades.html', {
        'propiedades': propiedades
    })


@login_required
@adminAuth('administrador')
def detalles_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id, activo=True)
    return render(request, 'administrador/detalles_propiedad.html', {
        'propiedad': propiedad
    })

def buzon_mensaje(request):
    contactoPublico = formulario.objects.all()
    return render(request, 'administrador/buzon_mensaje.html',
     {'contactoformulario': contactoPublico,
      })



def lista_general_cli_corr(request):
    propiedades = Propiedad.objects.all()

    lista_relaciones = []

    for propiedad in propiedades:
        lista_relaciones.append({
            'titulo': propiedad.titulo,
            'dueno': propiedad.dueno if propiedad.dueno else 'No asignado',
            'corredor': propiedad.corredor if propiedad.corredor else 'No asignado',
            'cliente': propiedad.cliente if propiedad.cliente else 'No asignado',
            'administrador': propiedad.administrador if propiedad.administrador else 'No asignado',
            'estado': propiedad.estado,
            'activo': propiedad.activo,
        })

    return render(request, 'administrador/lista_general_cli_corr.html', {
        'lista_relaciones': lista_relaciones
    })

# //////////////////////////////////////////////////////////

@login_required
def panel_corredores(request):
    try:
        admin = request.user.administrador
    except Administrador.DoesNotExist:
        return redirect('no_autorizado')

    if request.method == 'POST':
        form = CorredorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(admin)
            return redirect('panel_corredores')
    else:
        form = CorredorForm()

    corredores = Corredor.objects.all()
    return render(request, 'administrador/panel_corredores.html', {
        'form': form,
        'corredores': corredores
    })

@login_required
def bloquear_corredor(request, corredor_id):
    corredor = get_object_or_404(Corredor, id=corredor_id)
    corredor.activo = not corredor.activo 
    corredor.save()
    return redirect('panel_corredores')


@login_required
def eliminar_corredor(request, corredor_id):
    corredor = get_object_or_404(Corredor, id=corredor_id)
    administrador = get_object_or_404(Administrador, usuario=request.user)

    corredor.activo = False
    corredor.eliminado_por = administrador
    corredor.save()
    return redirect('panel_corredores')


# /////////////////////////////////////////////////////////////////

