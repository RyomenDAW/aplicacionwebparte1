# Crea una URL que muestre una lista de todos los proyectos 
# de la aplicación con sus datos correspondientes.

from django.db.models import Q, Count, Avg  # Para filtros OR, agregaciones, y operaciones con modelos
from django.shortcuts import render,redirect
from django.db.models import Prefetch
from django.forms import modelform_factory
from .models import *
from .forms import *
from django.contrib import messages
from datetime import datetime
from django.views.generic import ListView
from django.views.defaults import page_not_found


def mi_error_404(request, exception=None):
    # ERROR 404: NO SE ENCUENTRA LA PÁGINA SOLICITADA.
    return render(request, 'errores/404.html', None, None, 404)

def mi_error_400(request, exception=None):
    # ERROR 400: SOLICITUD INCORRECTA, GENERALMENTE DEBIDO A UN MAL FORMATO.
    return render(request, 'errores/400.html', None, None, 400)

def mi_error_403(request, exception=None):
    # ERROR 403: ACCESO PROHIBIDO, NO TIENE PERMISOS PARA VER ESTE RECURSO. (ADMIN)
    return render(request, 'errores/403.html', None, None, 403)

def mi_error_500(request, exception=None):
    # ERROR 500: ERROR INTERNO DEL SERVIDOR, OCURRE CUANDO HAY UN PROBLEMA NO ESPECIFICADO.
    return render(request, 'errores/500.html', None, None, 500)



from django.shortcuts import render
from .models import (
    Procesador,
    Grafica,
    FuenteAlimentacion,
    PlacaBase,
    Monitor,
    Ram,
    DiscoDuroHdd,
    DiscoDuroSsd,
    DiscoDuroNvme,
    Disipador,
    GraficaProcesador
)
#=================================================================================================================================================================

#ESTA ES LA PAGINA INDEX, AQUI IRA TODAN LAS URLS, EN TOTAL 10.
def inicio(request):
    return render(request, 'home/index.html')
#=================================================================================================================================================================


#ESTA VISTA DEVOLVERÁ TODOS LOS PROCESADORES CON SUS CARACTERÍSTICAS (ATRIBUTOS), TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA
#AL PROCESADOR
# def lista_procesadores(request):
#     procesadores = Procesador.objects.all()
#     return render (request, 'procesadores/lista_procesadores.html', {'procesadores': procesadores})


#=================================================================================================================================================================

# USANDO UN PARAMETRO ENTERO.

#ESTA VISTA DEVOLVERÁ TODOS LOS PROCESADORES QUE TENGAN EL NUMERO DE HILOS EXACTO QUE SE LE PASA, ES UN INTEGER, PUEDE SER NEGATIVO EL VALOR.
#TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA AL PROCESADOR

def lista_procesadores_segunhilos(request, numero_hilos):
    procesadores = Procesador.objects.filter(hilos = numero_hilos).all()
    return render (request, 'procesadores/lista_procesadores_segunhilos.html', {'procesadores': procesadores})
#=================================================================================================================================================================

#USANDO UN PARAMETRO TIPO STRING

#ESTA VISTA DEVOLVERÁ TODOS LOS PROCESADORES QUE PERTENEZCAN A LA FAMILIA QUE SE LE INDIQUE COMO PARAMETRO, POR EJEMPLO 'Intel', Y FILTRARÁ LOS PROCESADORES
#EN CONSECUENCIA, TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA AL PROCESADOR.

def lista_procesadores_segunfamilia(request, nombre_familia):
    #Aqui es un choices realmente, pero funcionaria de todas maneras ya que el campo es de tipo text (String)
    procesadores = Procesador.objects.filter(familiaprocesador = nombre_familia).all()
    return render (request, 'procesadores/lista_procesadores_segunfamilia.html', {'procesadores': procesadores})

#=================================================================================================================================================================

#USANDO DOS PARAMETROS
#ESTA VISTA DEVOLVERÁ LA LISTA DE GRAFICAS QUE CUMPLAN AMBOS PARAMETROS, EL ATRIBUTO DE SU FAMILIA (Ejemplo: 'Nvidia') y LA CANTIDAD DE VRAM ASIGNADA, 
#EN CONSECUENCIA, TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA A LA GRAFICA.

def lista_graficas_segunfamilia_y_vram(request, nombre_familia, cantidad_vram):
    graficas = Grafica.objects.filter(familiagrafica = nombre_familia, memoriavram = cantidad_vram ).all()
    return render (request, 'graficas/lista_graficas_segunfamilia_y_vram.html', {'graficas': graficas})

#=================================================================================================================================================================

#SE UTILIZA LA PARTE DE AGGREGATE QUE SE TENIA QUE INVESTIGAR, SE UTILIZA PARA PODER HACER AGREGACIONES SIN CARGAR EN LA MEMORIA TODOS LOS VALORES Y DEVOLVER EL
#RESULTADO DE LAS OPERACIONES REALIZADAS CON ESOS VALORES, AHORRANDO RECURSO Y OPTIMIZANDO.

#La vista nos obtiene la media (avg) del campo nucleos de todos los objetos en el modelo Procesador, tener en cuenta que es negativo algunos valores.


def promedio_nucleos(request):
    promedio_nucleos = Procesador.objects.aggregate(promedio_nucleos=Avg('nucleos'))
    return render(request, 'procesadores/promedio_nucleos.html', {'promedio_nucleos': promedio_nucleos})


#=================================================================================================================================================================




#ESTA VISTA NOS DEVUELVE A TRAVES DE UN FILTER CON UN AND OBLIGATORIO Y DENTRO DE 2 OR, QUE POR LO MENOS SE CUMPLA UNO

#En este caso: procesadores que tengan más de 8 núcleos o que pertenezcan a la familia 'Intel', pero que además tengan más de 12 hilos (greaterthan)
def filtrar8nucleos_OR_intel_AND_12hilos(request):
    procesadores = Procesador.objects.filter(  (Q(nucleos__gt=8) | Q(familiaprocesador='Intel')) & Q(hilos__gt=12) ).all()
    return render( request,  'procesadores/filtrar8nucleos_OR_intel_AND_12hilos.html', {'procesadores': procesadores}
    )
    
    
    
#=================================================================================================================================================================

#ESTA VISTA DEVUELVE CON UN FILTRO DE ORDER BY QUE SERIA DE FORMA DESCEDENTE, LA FECHA, TODAS LAS GRAFICAS AL SER CON SEEDERS SALEN CON LA MISMA FECHA.

def filtrargraficas_segunfecha(request):
    graficas = Grafica.objects.order_by('-fecha_salida')
    return render ( request, 'graficas/filtrargraficas_segunfecha.html', {'graficas': graficas })

# Ordenar Ascendente: Model.objects.order_by('field_name')
# Ordenar Descendente: Model.objects.order_by('-field_name')
# Ordenar por Múltiples Campos: Model.objects.order_by('field1', '-field2')
#Da error si da string (urinary error)

#=================================================================================================================================================================

# ESTA VISTA OBTIENE UNA GRAFICA ESPECIFICA SEGUN SU ID Y DEVUELVE LOS PROCESADORES ASOCIADOS A ESA GRAFICA.
# SI NO EXISTE LA GRAFICA, GENERARA UN ERROR.
# UTILIZA EL NOMBRE RELACIONADO PARA FILTRAR LOS PROCESADORES CONECTADOS, ESTOS DEVUELVEN TAMBIEN TODOS SUS ATRIBUTOS.

def procesadores_segun_grafica(request, grafica_id):
    # Obtener la gráfica específica; generará un error si no existe
    grafica_especifica = Grafica.objects.get(id_grafica=grafica_id)

    # Usar el related_name para acceder a los procesadores conectados a esta gráfica
    procesadores_conectados = Procesador.objects.filter(procesadores_reverse=grafica_especifica)

    # Renderizar la plantilla con la gráfica y los procesadores asociados
    return render(request, 'reverse/procesadores_segun_grafica.html', {
        'grafica': grafica_especifica,
        'procesadores': procesadores_conectados,
    })

#=================================================================================================================================================================
# ESTA VISTA OBTIENE LAS PRIMERAS 5 INSTANCIAS DE DISCODUROSSD Y LAS MUESTRA EN LA PLANTILLA.
# NO SE APLICA NINGÚN FILTRO ESPECIAL, SÓLO SE LIMITA A 5 RESULTADOS.

def primeros_5_ssd(request):
    # Obtener las primeras 5 instancias de DiscoDuroSsd según su ID
    ssds = DiscoDuroSsd.objects.all()[:5]

    return render(request, 'ssd/primeros_5_ssd.html', {
        'ssds': ssds,
    })

#=================================================================================================================================================================

#ESTA VISTA DEVOLVERA TODAS LAS GRAFICAS SIN CUELLO DE BOTELLA, ES DECIR, TODAS AQUELLAS GRAFICAS QUE TENGAN EN LA RELACION MANYTOMANY (GRAFICAPROCESADOR), EL ATRIBUTO
#DE CUELLODEBOTELLA EN 0 (FALSE), ADEMAS TE INCLUIRE A QUE PROCESADOR VA ASOCIADA ESA GRAFICA, Y LOS ATRIBUTOS DE ESTE.
def graficas_sin_cuello_de_botella(request):
    # Filtrar las relaciones donde cuellodebotella es None (o False (0), si es un BooleanField)
    graficas_sin_cuello = GraficaProcesador.objects.filter(cuellodebotella=False)  # O None si lo defines como Nullable

    return render(request, 'intermedia/graficas_sin_cuello_de_botella.html', {
        'graficas_sin_cuello': graficas_sin_cuello,
    })




#Tecnicamente desde aqui ya te cumplo todos los requisitos, me queda 1 URL, asi que vamos por lo facil ya que ahora no se pide ningun requisito mas, work smart, not hard.



#=================================================================================================================================================================

#ESTA VISTA DEVOLVERÁ TODAS LAS GRAFICAS CON SUS CARACTERÍSTICAS (ATRIBUTOS), TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA
#A LA TARJETA GRAFICA
def lista_graficas(request):
    graficas = Grafica.objects.all()
    return render (request, 'graficas/lista_graficas.html', {'graficas': graficas})
#=================================================================================================================================================================



#No se si te molestan las lineas pero yo lo veo mejor asi.

#=================================================================================================================================================================


def crear_procesador(request):
    if request.method == 'POST':
        form = ProcesadorForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo procesador en la base de datos
            return redirect('lista_procesadores.html')  # Cambia al nombre de tu URL para la lista
    else:
        form = ProcesadorForm()

    return render(request, 'procesadores/crear_procesador.html', {'form': form})



from django.shortcuts import render
from .models import Procesador
from .forms import BusquedaAvanzadaProcesador

def lista_procesadores(request):
    # Inicializar el formulario de búsqueda
    form = BusquedaAvanzadaProcesador(request.GET)

    # Filtrar los procesadores según los criterios del formulario
    procesadores = Procesador.objects.all()

    if form.is_valid():
        nombre = form.cleaned_data.get('nombreBusqueda')
        nucleos = form.cleaned_data.get('nucleos')
        hilos = form.cleaned_data.get('hilos')
        familiaprocesador = form.cleaned_data.get('familiaprocesador')

        if nombre:
            procesadores = procesadores.filter(nombre__icontains=nombre)
        if nucleos:
            procesadores = procesadores.filter(nucleos=nucleos)
        if hilos:
            procesadores = procesadores.filter(hilos=hilos)
        if familiaprocesador:
            procesadores = procesadores.filter(familiaprocesador__in=familiaprocesador)

    return render(request, 'procesadores/lista_procesadores.html', {'form': form, 'procesadores': procesadores})

from django.shortcuts import render, get_object_or_404
from .models import Procesador
from .forms import ProcesadorForm

def editar_procesador(request, id_procesador):
    procesador = get_object_or_404(Procesador, id_procesador=id_procesador)  # Recupera el procesador por id
    if request.method == 'POST':
        form = ProcesadorForm(request.POST, instance=procesador)
        if form.is_valid():
            form.save()
            return redirect('lista_procesadores')
    else:
        form = ProcesadorForm(instance=procesador)
    
    return render(request, 'procesadores/editar_procesador.html', {'form': form, 'procesador': procesador})


def eliminar_procesador(request, id_procesador):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    procesador = get_object_or_404(Procesador, id_procesador=id_procesador)
    
    if request.method == 'POST':
        try:
            procesador.delete()  # Eliminar el procesador de la base de datos
            return redirect('lista_procesadores')  # Redirigir a la lista de procesadores
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar el procesador: {e}")
            return render(request, 'eliminar_procesador.html', {'procesador': procesador, 'error': 'Hubo un error al eliminar el procesador.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'eliminar_procesador.html', {'procesador': procesador})
