from decimal import Decimal
from pyexpat.errors import messages
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
from login.estructuradoAuth import duenoAuth
from administrador.forms import DocumentoPropiedad
from administrador.models import Propiedad, ImagenPropiedad

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import fitz # -pip install django pillow pymupdf
import os

from .models import *
from .forms import *
   

@duenoAuth('dueno')
@login_required 
def index(request):
    dolar = euro = uf = "Cargando Valores.."
    iva = Decimal('19.00')
    propiedades = Propiedad.objects.filter(activo=True, visibilidad='visible')
# //////////////////////////////////////////////////////////////////////////////
    try:
        dueno = Dueno.objects.get(user=request.user)
    except Dueno.DoesNotExist:
        dueno = None

    propiedadesPropietario = Propiedad.objects.filter(
        dueno=dueno,
    ) if dueno else Propiedad.objects.none()

    # //////////////////////////////////////////////////////////////////
    # API_Monetario
    try:
        respuesta = requests.get("https://mindicador.cl/api", timeout=1)
        if respuesta.status_code == 200:
            dato_respuesta = respuesta.json()
            dolar = dato_respuesta["dolar"]["valor"]
            euro = dato_respuesta["euro"]["valor"]
            uf = dato_respuesta["uf"]["valor"]
    except Exception as e:
        print("No se Pudo Acceder a la Api-Valor-Mercado:", e)

    return render(request, 'dueno/index.html', {
        'propiedades' : propiedades,
        'propiedadesPropietario': propiedadesPropietario,
        'dueno': dueno,
        'dolar': dolar,
        'euro': euro,
        'uf': uf,
        'iva': iva,
        'clp': dolar,
    })


# @duenoAuth('dueno')
# @login_required 

def panel_tramites(request):
     return render(request, 'tramite_propiedad/panel_tramites.html')

@login_required
def registrar_propiedad(request):
    if request.method == 'POST':
        propiedad_form = PropiedadFormDueno(request.POST)
        caracteristica_form = CaracteristicaForm(request.POST)
        documento_formset = DocumentoFormSet(request.POST, request.FILES, queryset=DocumentoPropiedad.objects.none())

        if propiedad_form.is_valid() and caracteristica_form.is_valid() and documento_formset.is_valid():
            propiedad = propiedad_form.save(commit=False)
            propiedad.dueno = request.user.dueno 
            propiedad.save()

            caracteristica = caracteristica_form.save(commit=False)
            caracteristica.propiedad = propiedad
            caracteristica.save()

            for form in documento_formset:
                if form.cleaned_data and form.cleaned_data.get('archivo'):
                    documento = form.save(commit=False)
                    documento.propiedad = propiedad
                    documento.save()

            return redirect('listar_propiedad')
    else:
        propiedad_form = PropiedadFormDueno()
        caracteristica_form = CaracteristicaForm()
        documento_formset = DocumentoFormSet(queryset=DocumentoPropiedad.objects.none())

    return render(request, 'propiedad/crear_propiedad.html', {
        'propiedad_form': propiedad_form,
        'caracteristica_form': caracteristica_form,
        'documento_formset': documento_formset,
    })


@login_required
@duenoAuth('dueno') 
def listar_propiedad(request):
    try:
        dueno = Dueno.objects.get(user=request.user)
    except Dueno.DoesNotExist:
        dueno = None

    propiedades= Propiedad.objects.filter(
        dueno=dueno,
    ) if dueno else Propiedad.objects.none()
    return render(request, 'propiedad/listar_propiedad.html', {
        'propiedades': propiedades
    })


# @login_required
# @duenoAuth('dueno') 
def detalle_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    if propiedad.activo == True:
            return render(request, 'propiedad/detalle_propiedad.html', {
        'propiedad': propiedad    
    }) 
    if propiedad.activo == False:
            return HttpResponse("<h1 style='color: red;'>Su propiedad esta en Proceso de 'activacion' por el administrador, visite sus propiedades y observe el estado de actividad, si esta True esta activo para ver sus detalles y si esta False entonces esta su propiedad en proceso de 'Activacion'<h1>", status=404)
    



@login_required
@duenoAuth('dueno') 
def mis_propiedad(request):
    dueno_actual = request.user.dueno
    propiedades = Propiedad.objects.filter(dueno=dueno_actual)
    return render(request, 'propiedad/mis_propiedad.html', {
        'propiedades': propiedades
    })




# ////////////////////////////////////////////////////////////////////Borrar Todo lo que aqui 

from .models import MultimediaItem
from .forms import MultimediaForm


def lista_items(request):
    items = MultimediaItem.objects.all()
    items = MultimediaItem.objects.filter(activo=True)

# objects.all() — devuelve todos los registros.

# objects.filter(**kwargs) — devuelve los registros que cumplen con la condición.

# objects.exclude(**kwargs) — devuelve los registros que no cumplen la condición.

# objects.get(**kwargs) — devuelve un solo registro que cumple la condición (y falla si hay más de uno o ninguno).

# objects.order_by(*fields) — ordena los registros por uno o más campos.

# objects.count() — cuenta cuántos registros hay.

# objects.create(**kwargs) — crea y guarda un nuevo objeto directamente.

# objects.update(**kwargs) — actualiza los registros que coinciden con una consulta (generalmente usado con filter()).

# objects.delete() — elimina registros.
    return render(request, 'tu_app/lista.html', {'items': items})

def crear_item(request):
    form = MultimediaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('lista')
    return render(request, 'tu_app/crear.html', {'form': form})

def actualizar_item(request, pk):
    item = get_object_or_404(MultimediaItem, pk=pk)
    form = MultimediaForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('lista')
    return render(request, 'tu_app/actualizar.html', {'form': form, 'item': item})

def eliminar_item(request, pk):
    item = get_object_or_404(MultimediaItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('lista')
    return render(request, 'tu_app/eliminar.html', {'item': item})



""" Consulta y obtención de datos

    .all() — Devuelve todos los registros.

    .filter(**kwargs) — Devuelve los registros que cumplen con la condición.

    .exclude(**kwargs) — Devuelve los registros que no cumplen con la condición.

    .get(**kwargs) — Devuelve un solo registro que cumple la condición (lanza excepción si hay más o menos de uno).

    .first() — Devuelve el primer registro del QuerySet o None si está vacío.

    .last() — Devuelve el último registro del QuerySet o None.

    .order_by(*fields) — Ordena los registros por uno o más campos.

    .reverse() — Invierte el orden de los registros.

    .distinct() — Devuelve registros únicos (sin duplicados).

    .values(*fields) — Devuelve un QuerySet de diccionarios con solo los campos especificados.

    .values_list(*fields, flat=False) — Devuelve un QuerySet de tuplas con los campos especificados; si flat=True devuelve lista simple si es un solo campo.

    .select_related(*fields) — Realiza un JOIN para cargar relaciones ForeignKey (optimiza consultas).

    .prefetch_related(*fields) — Optimiza la carga de relaciones ManyToMany o ForeignKey en múltiples consultas.

Conteo y existencia

    .count() — Devuelve la cantidad de registros del QuerySet.

    .exists() — Devuelve True si hay al menos un registro en el QuerySet, False si está vacío.

Creación, actualización y eliminación

    .create(**kwargs) — Crea y guarda un nuevo registro directamente.

    .update(**kwargs) — Actualiza los registros del QuerySet con los valores dados.

    .delete() — Elimina los registros del QuerySet (o un objeto si es llamado sobre una instancia).

Agregaciones y anotaciones

    .aggregate(**kwargs) — Realiza operaciones agregadas (suma, promedio, máximo, mínimo, etc.) y devuelve un diccionario.

    .annotate(**kwargs) — Agrega valores calculados a cada objeto en el QuerySet (para luego filtrar u ordenar).

Ejemplo agregaciones comunes:

    Sum('campo')

    Avg('campo')

    Count('campo')

    Max('campo')

    Min('campo')

Otros métodos útiles

    .update_or_create(defaults=None, **kwargs) — Actualiza un registro si existe o lo crea si no.

    .get_or_create(**kwargs) — Obtiene un registro si existe o lo crea.

    .bulk_create(objs) — Crea múltiples objetos en una sola consulta.

    .bulk_update(objs, fields) — Actualiza múltiples objetos en una sola consulta.

    .in_bulk(id_list) — Devuelve un diccionario con objetos indexados por su id.

    .iterator() — Itera sobre el QuerySet usando menos memoria.

    .defer(*fields) — Omite la carga de ciertos campos (lazy loading).

    .only(*fields) — Carga solo los campos especificados. """


# Documentos a Trabajar! >> 27/05/2025
def comprimir_imagen(imagen):
    img = Image.open(imagen)
    img_io = BytesIO()
    img = img.convert('RGB') 
    img.save(img_io, format='JPEG', quality=60)  # Calidad al 60%
    nueva_imagen = ContentFile(img_io.getvalue(), name=imagen.name)
    return nueva_imagen

def comprimir_pdf(pdf_file):
    original_pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
    nuevo_pdf = fitz.open()

    for pagina in original_pdf:
        pix = pagina.get_pixmap(dpi=500)  # Baja calidad (100 DPI)
        img_bytes = pix.tobytes("png")  

        # Crear imagen
        image = Image.open(BytesIO(img_bytes))
        width, height = image.size

        # Crear nueva página con el tamaño de la imagen
        nueva_pagina = nuevo_pdf.new_page(width=width, height=height)

        # Insertar la imagen en la nueva página
        nueva_pagina.insert_image(
            fitz.Rect(0, 0, width, height),
            stream=img_bytes,
            keep_proportion=True
        )

    # Escribir resultado a memoria
    output_bytes = nuevo_pdf.write()
    return ContentFile(output_bytes, name=pdf_file.name)


def lista_documentos(request):
    documentos = Documento.objects.all()
    return render(request, 'archivos/lista.html', {'documentos': documentos})

def subir_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save(commit=False)
            archivo = request.FILES['archivo']
            ext = os.path.splitext(archivo.name)[1].lower()

            if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                doc.archivo = comprimir_imagen(archivo)
            elif ext == '.pdf':
                doc.archivo = comprimir_pdf(archivo)

            doc.save()

            # Calcular tamaño del archivo en KB
            peso_bytes = os.path.getsize(doc.archivo.path)
            doc.kb = round(peso_bytes / 1024, 2)
            doc.save(update_fields=['kb'])

            return redirect('listaDocu')
    else:
        form = DocumentoForm()

    return render(request, 'archivos/subir.html', {'form': form})


def eliminar_documento(request, pk):
    doc = get_object_or_404(Documento, pk=pk)
    doc.delete()
    return redirect('listaDocu')


# ///////////////////////////////////////////////////////////////////////////

# 

