from decimal import Decimal
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from corredor.forms import *
from login.estructuradoAuth import corredorAuth
from administrador.forms import *
from administrador.models import Propiedad, ImagenPropiedad
import requests
from cliente.models import *
from django.core.paginator import Paginator
from formContacto.models import formulario

@login_required
@corredorAuth('corredor')
def index(request):

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

    try:
        corredor = request.user.corredor
    except Exception:
        corredor = None

    propiedades_lista = Propiedad.objects.all().order_by('-fecha_publicacion')
    paginator = Paginator(propiedades_lista, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    interesados_por_propiedad = {}
    for propiedad in page_obj:
        interesados = ContactoClientePropiedad.objects.filter(propiedad=propiedad)
        interesados_por_propiedad[propiedad.id] = interesados

# ////////////////////////////////////////////////////////

    dolar = euro = uf = "Cargando Valores.."
    iva = Decimal('19.00')

    try:
        respuesta = requests.get("https://mindicador.cl/api", timeout=1)
        if respuesta.status_code == 200:
            dato_respuesta = respuesta.json()
            dolar = dato_respuesta["dolar"]["valor"]
            euro = dato_respuesta["euro"]["valor"]
            uf = dato_respuesta["uf"]["valor"]
    except Exception as e:
        print("No se pudo acceder a la API-Valor-Mercado:", e)

    return render(request, 'corredor/index.html', {
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
        # /////////////////////////////////////////
        'propiedades': page_obj,
        'interesados_por_propiedad': interesados_por_propiedad,
        'corredor': corredor,
        'dolar': dolar,
        'euro': euro,
        'uf': uf,
        'iva': iva,
        'clp': dolar,
    })

@corredorAuth('corredor') 
@login_required 
def crear_propiedades(request):
    ImagenFormSet = modelformset_factory(ImagenPropiedad, form=ImagenForm, extra=3, max_num=14)

    if request.method == 'POST':
        propiedad_form = PropiedadForm(request.POST)
        imagenes_formset = ImagenFormSet(request.POST, request.FILES, queryset=ImagenPropiedad.objects.none())
        caracteristicas_form = CaracteristicaForm(request.POST)

        if propiedad_form.is_valid() and imagenes_formset.is_valid() and caracteristicas_form.is_valid():
            propiedad = propiedad_form.save()

            for form in imagenes_formset.cleaned_data:
                if form:
                    ImagenPropiedad.objects.create(propiedad=propiedad, imagen=form['imagen'])

            caracteristica = caracteristicas_form.save(commit=False)
            caracteristica.propiedad = propiedad
            caracteristica.save()

            return redirect('index_corredor')

    else:
        propiedad_form = PropiedadForm()
        imagenes_formset = ImagenFormSet(queryset=ImagenPropiedad.objects.none())
        caracteristicas_form = CaracteristicaForm()

    return render(request, 'corredor/crear_propiedades.html', {
        'propiedad_form': propiedad_form,
        'imagenes_formset': imagenes_formset,
        'caracteristicas_form': caracteristicas_form
    })

@login_required
@corredorAuth('corredor')
def detalle_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)

    documentos = DocumentoPropiedad.objects.filter(propiedad=propiedad)

    return render(request, 'corredor/detalle_propiedad.html', {
        'propiedad': propiedad,
        'documentos': documentos
    })
# def crmSistemaCorredor(request):

#     cliente = Cliente.objects.all();

#     return render(request, '', {
#        'cliente'  : cliente,
#     })


# //////////////////////////////////////////////////////

def mensajes_publico_corredor(request):
    contactoPublico = formulario.objects.all()
    return render(request, 'corredor/mensajes_publico_corredor.html',
     {'contactoformulario': contactoPublico,
      })
def mensajes_privado_corredor(request):
    seguimientos = SeguimientoContacto.objects.all().order_by('-fecha')

    edit_id = request.GET.get('edit')
    eliminar_id = request.GET.get('delete')

    if eliminar_id:
        seguimiento_a_eliminar = get_object_or_404(SeguimientoContacto, id=eliminar_id)
        seguimiento_a_eliminar.delete()
        return redirect('mensajes_privado_corredor')

    if request.method == 'POST':
        if request.POST.get('id'):
            seguimiento = get_object_or_404(SeguimientoContacto, id=request.POST.get('id'))
            form = SeguimientoContactoForm(request.POST, instance=seguimiento)
        else:
            form = SeguimientoContactoForm(request.POST)

        if form.is_valid():
            form.save()
            if request.POST.get('id'):
                return redirect(f"{reverse('mensajes_privado_corredor')}?edit={request.POST.get('id')}")
            else:
                return redirect('mensajes_privado_corredor')
    else:
        if edit_id:
            seguimiento = get_object_or_404(SeguimientoContacto, id=edit_id)
            form = SeguimientoContactoForm(instance=seguimiento)
        else:
            form = SeguimientoContactoForm()

    return render(request, 'corredor/mensajes_privado_corredor.html', {
        'form': form,
        'seguimientos': seguimientos,
        'edit_id': edit_id,
    })