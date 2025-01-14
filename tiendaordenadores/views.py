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
from django.contrib.auth import login

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
    
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    return render(request, 'home/index.html')
#=================================================================================================================================================================


#ESTA VISTA DEVOLVERÁ TODOS LOS PROCESADORES CON SUS CARACTERÍSTICAS (ATRIBUTOS), TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA
#AL PROCESADOR
# def lista_procesadores(request):
#     procesadores = Procesador.objects.all()
#     return render (request, 'procesadores/lista_procesadores.html', {'procesadores': procesadores})


def lista_procesadores(request):
    procesadores = Procesador.objects.all()  
    return render(request, 'procesadores/lista_procesadores.html', {'procesadores': procesadores})

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
            return redirect('lista_procesadores')  # Cambia al nombre de tu URL para la lista
    else:
        form = ProcesadorForm()

    return render(request, 'procesadores/crear_procesador.html', {'form': form})



from django.shortcuts import render
from .models import Procesador
from .forms import BusquedaAvanzadaProcesador, BusquedaAvanzadaGrafica

def read_procesadores(request):
    form = BusquedaAvanzadaProcesador(request.GET)

    # Verifica que el formulario se está enviando correctamente
    print(form)

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

    return render(request, 'procesadores/read_procesadores.html', {'form': form, 'procesadores': procesadores})



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
    return render(request, 'procesadores/eliminar_procesador.html', {'procesador': procesador})


#=================================================================================================================================================================

def crear_grafica(request):
    if request.method == 'POST':
        form = GraficaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo procesador en la base de datos
            return redirect('lista_graficas')  # Redirige usando el nombre de la vista
    else:
        form = GraficaForm()

    return render(request, 'graficas/crear_grafica.html', {'form': form})

def read_graficas(request):
    form = BusquedaAvanzadaGrafica(request.GET)

    # Verifica que el formulario se está enviando correctamente
    print(form)

    graficas = Grafica.objects.all()

    if form.is_valid():
        nombre = form.cleaned_data.get('nombreBusqueda')
        potenciacalculo = form.cleaned_data.get('potenciacalculo')
        memoriavram = form.cleaned_data.get('memoriavram')
        familiagrafica = form.cleaned_data.get('familiagrafica')

        if nombre:
            graficas = graficas.filter(nombre__icontains=nombre)
        if potenciacalculo:
            graficas = graficas.filter(potenciacalculo=potenciacalculo)
        if memoriavram:
            graficas = graficas.filter(memoriavram=memoriavram)
        if familiagrafica:
            graficas = graficas.filter(familiagrafica__in=familiagrafica)

    return render(request, 'graficas/read_graficas.html', {'form': form, 'graficas': graficas})


def editar_grafica(request, id_grafica):
    grafica = get_object_or_404(Grafica, id_grafica=id_grafica)  # Recupera el procesador por id
    if request.method == 'POST':
        form = GraficaForm(request.POST, instance=grafica)
        if form.is_valid():
            form.save()
            return redirect('lista_graficas')
    else:
        form = GraficaForm(instance=grafica)
    
    return render(request, 'graficas/editar_grafica.html', {'form': form, 'grafica': grafica})

def eliminar_grafica(request, id_grafica):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    grafica = get_object_or_404(Grafica, id_grafica=id_grafica)
    
    if request.method == 'POST':
        try:
            grafica.delete()  
            return redirect('lista_graficas')  # Redirigir a la lista de graficas
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar la grafica: {e}")
            return render(request, 'eliminar_grafica.html', {'grafica': grafica, 'error': 'Hubo un error al eliminar la grafica.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'graficas/eliminar_grafica.html', {'grafica': grafica})

#=================================================================================================================================================================

def crear_monitor(request):
    if request.method == 'POST':
        form = MonitorForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo procesador en la base de datos
            return redirect('inicio')  # Redirige usando el nombre de la vista
    else:
        form = MonitorForm()

    return render(request, 'monitores/crear_monitor.html', {'form': form})

def read_monitor(request):
    form = BusquedaAvanzadaMonitor(request.GET)
    monitor = Monitor.objects

    # Inicializar variables con valores predeterminados
    hz_min = None
    hz_max = None
    calidad_respuesta = None
    curvo = None
    pantallafiltroplasma = None

    if form.is_valid():
        hz_min = form.cleaned_data.get('hz_min')
        hz_max = form.cleaned_data.get('hz_max')
        calidad_respuesta = form.cleaned_data.get('calidad_respuesta')
        curvo = form.cleaned_data.get('curvo')
        pantallafiltroplasma = form.cleaned_data.get('pantallafiltroplasma')

        # Convertir curvo y pantallafiltroplasma a booleanos
        curvo = curvo == '1'
        pantallafiltroplasma = pantallafiltroplasma == '1'

        if hz_min is not None:
            monitor = monitor.filter(hz__gte=hz_min)
        if hz_max is not None:
            monitor = monitor.filter(hz__lte=hz_max)
        if calidad_respuesta is not None:
            monitor = monitor.filter(calidad_respuesta__lte=calidad_respuesta)
        if curvo is not None:
            monitor = monitor.filter(curvo=curvo)
        if pantallafiltroplasma is not None:
            monitor = monitor.filter(pantallafiltroplasma=pantallafiltroplasma)

    # La impresión ahora no genera errores, incluso si el formulario no es válido
    print(f"hz_min: {hz_min}, hz_max: {hz_max}, calidad_respuesta: {calidad_respuesta}, curvo: {curvo}, pantallafiltroplasma: {pantallafiltroplasma}")

    return render(request, 'monitores/read_monitor.html', {'form': form, 'monitors': monitor.all()})


#Preguntarle a jorge porque en la consulta aparece y no en el read, este falla.

def editar_monitor(request, id_monitor):
    monitor = get_object_or_404(Monitor, id_monitor=id_monitor)
    
    if request.method == "POST":
        # Crear el formulario con los datos del POST y la instancia del monitor
        form = MonitorForm(request.POST, instance=monitor)
        
        if form.is_valid():
            # Si el formulario es válido, guardar los cambios
            form.save()
            return redirect('inicio')


    else:
        # Si no es un POST, simplemente cargar el formulario con los valores actuales del monitor
        form = MonitorForm(instance=monitor)

    return render(request, 'monitores/editar_monitor.html', {'form': form, 'monitor': monitor})


def eliminar_monitor(request, id_monitor):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    monitor = get_object_or_404(Monitor, id_monitor=id_monitor)
    
    if request.method == 'POST':
        try:
            monitor.delete()  
            return redirect('inicio')  # Redirigir a la lista de graficas
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar el monitor: {e}")
            return render(request, 'eliminar_monitor.html', {'monitor': monitor, 'error': 'Hubo un error al eliminar el monitor.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'monitores/eliminar_monitor.html', {'monitor': monitor})

#=================================================================================================================================================================

def crear_fuente(request):
    if request.method == 'POST':
        form = FuenteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo procesador en la base de datos
            return redirect('inicio')  # Redirige usando el nombre de la vista
    else:
        form = FuenteForm()

    return render(request, 'fuentes/crear_fuente.html', {'form': form})


def read_fuente(request):
    form = BusquedaAvanzadaFuente(request.GET)
    fuentes = FuenteAlimentacion.objects.all()  # Comienza con todas las fuentes
    
    if form.is_valid():
        vatios = form.cleaned_data.get('vatios')
        amperaje = form.cleaned_data.get('amperaje')
        conectoresdisponibles = form.cleaned_data.get('conectoresdisponibles')
        calidadfuente = form.cleaned_data.get('calidadfuente')

        # Si vatios tiene un valor y no es vacío, se filtra exactamente por ese valor
        if vatios:
            fuentes = fuentes.filter(vatios=vatios)

        # Otros filtros se aplican de la misma manera, pero no afectarán el resultado si vatios no coincide
        if amperaje:
            fuentes = fuentes.filter(amperaje=amperaje)
        if conectoresdisponibles:
            fuentes = fuentes.filter(conectoresdisponibles__icontains=conectoresdisponibles)
        if calidadfuente:
            fuentes = fuentes.filter(calidadfuente=calidadfuente)

    # Renderizamos la página con el formulario y las fuentes filtradas
    return render(request, 'fuentes/read_fuente.html', {'form': form, 'fuentes': fuentes})

def editar_fuente(request, id_fuente):
    fuente = get_object_or_404(FuenteAlimentacion, id_fuente=id_fuente) 
    
    if request.method == "POST":
        # Crear el formulario con los datos del POST y la instancia del monitor
        form = FuenteForm(request.POST, instance=fuente)
        
        if form.is_valid():
            # Si el formulario es válido, guardar los cambios
            form.save()
            return redirect('inicio')


    else:
        # Si no es un POST, simplemente cargar el formulario con los valores actuales del monitor
        form = FuenteForm(instance=fuente)

    return render(request, 'fuentes/editar_fuente.html', {'form': form, 'fuente': fuente})

def eliminar_fuente(request, id_fuente):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    fuente = get_object_or_404(FuenteAlimentacion, id_fuente=id_fuente)
    
    if request.method == 'POST':
        try:
            fuente.delete()  
            return redirect('inicio')  # Redirigir a la lista de graficas
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar la fuente: {e}")
            return render(request, 'eliminar_fuente.html', {'fuente': fuente, 'error': 'Hubo un error al eliminar la fuente.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'fuentes/eliminar_fuente.html', {'fuente': fuente})



def crear_ram(request):
    if request.method == 'POST':
        form = RamForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo procesador en la base de datos
            return redirect('inicio')  # Redirige usando el nombre de la vista
    else:
        form = RamForm()

    return render(request, 'ram/crear_ram.html', {'form': form})


def read_ram(request):
    form = RamAvanzadaForm(request.GET)  # Usamos request.GET para recibir datos de búsqueda
    rams = Ram.objects.all()  # Comienza con todas las RAM
    
    if form.is_valid():
        mhz = form.cleaned_data.get('mhz')
        familiaram = form.cleaned_data.get('familiaram')
        fecha_fabricacion = form.cleaned_data.get('fecha_fabricacion')
        rgb = form.cleaned_data.get('rgb')
        factormemoria = form.cleaned_data.get('factormemoria')

        # Filtramos por MHz si se proporciona. Aquí usamos 'icontains' ya que mhz es texto ahora.
        if mhz:
            rams = rams.filter(mhz__icontains=mhz)

        # Filtramos por familia de RAM si se proporciona
        if familiaram:
            rams = rams.filter(familiaram=familiaram)
        
        # Filtramos por fecha de fabricación si se proporciona
        if fecha_fabricacion:
            rams = rams.filter(fecha_fabricacion=fecha_fabricacion)

        # Filtramos por RGB si se proporciona
        if rgb is not None:
            rams = rams.filter(rgb=rgb)

        # Filtramos por factor de memoria si se proporciona
        if factormemoria:
            rams = rams.filter(factormemoria__icontains=factormemoria)

    # Renderizamos la página con el formulario y las RAM filtradas
    return render(request, 'ram/read_ram.html', {'form': form, 'rams': rams})


def editar_ram(request, id_ram):
    # Recupera el objeto RAM específico
    ram = get_object_or_404(Ram, id_ram=id_ram)
    
    # Si el método de la solicitud es POST, procesamos el formulario con los datos del usuario
    if request.method == 'POST':
        form = RamForm(request.POST, instance=ram)
        if form.is_valid():
            form.save()
            return redirect('inicio') 
    else:
        form = RamForm(instance=ram)  # Cargar el formulario con los datos actuales de la RAM

    # Siempre devolver una respuesta (renderiza el formulario de edición)
    return render(request, 'ram/editar_ram.html', {'form': form, 'ram': ram})


def eliminar_ram(request, id_ram):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    ram = get_object_or_404(Ram, id_ram=id_ram)
    
    if request.method == 'POST':
        try:
            ram.delete()  
            return redirect('inicio')  # Redirigir a la lista de graficas
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar la RAM: {e}")
            return render(request, 'eliminar_ram.html', {'ram': ram, 'error': 'Hubo un error al eliminar la RAM.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'ram/eliminar_ram.html', {'ram': ram})

def crear_hdd(request):
    if request.method == 'POST':
        form = HDDForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo procesador en la base de datos
            return redirect('inicio')  # Redirige usando el nombre de la vista
    else:
        form = HDDForm()

    return render(request, 'discoshdd/crear_hdd.html', {'form': form})



def read_hdd(request):
    hdds = DiscoDuroHdd.objects.all()  # Empieza con todos los discos duros
    form = HDDBusquedaAvanzadaForm(request.GET)

    if form.is_valid():
        # Obtener los datos del formulario
        rpm = form.cleaned_data.get('rpm')
        capacidad = form.cleaned_data.get('capacidad')
        peso = form.cleaned_data.get('peso')
        tiempomediofallos = form.cleaned_data.get('tiempomediofallos')
        pulgadas = form.cleaned_data.get('pulgadas')

        # Filtrado eliminatorio: Solo se filtra por el primer campo con valor no vacío
        if rpm and rpm.isdigit() and int(rpm) > 0:
            hdds = hdds.filter(rpm=rpm)  # Filtra los discos que coincidan con el valor de rpm
        elif capacidad and capacidad.isdigit() and int(capacidad) > 0:
            hdds = hdds.filter(capacidad=capacidad)  # Filtra los discos que coincidan con la capacidad
        elif peso and peso.isdigit() and int(peso) > 0:
            hdds = hdds.filter(peso=peso)  # Filtra los discos que coincidan con el peso
        elif tiempomediofallos and tiempomediofallos.isdigit() and int(tiempomediofallos) > 0:
            hdds = hdds.filter(tiempomediofallos=tiempomediofallos)  # Filtra los discos que coincidan con el tiempo medio entre fallos
        elif pulgadas and pulgadas.replace('.', '', 1).isdigit() and float(pulgadas) > 0 and float(pulgadas) <= 35000:
            hdds = hdds.filter(pulgadas=pulgadas)  # Filtra los discos que tengan un tamaño de pulgadas válido

    return render(request, 'discoshdd/read_hdd.html', {'form': form, 'hdds': hdds})

def editar_hdd(request, id_hdd):
    # Recupera el objeto RAM específico
    hdd = get_object_or_404(DiscoDuroHdd, id_hdd=id_hdd)
    
    # Si el método de la solicitud es POST, procesamos el formulario con los datos del usuario
    if request.method == 'POST':
        form = HDDForm(request.POST, instance=hdd)
        if form.is_valid():
            form.save()
            return redirect('inicio') 
    else:
        form = HDDForm(instance=hdd)  # Cargar el formulario con los datos actuales de la RAM

    # Siempre devolver una respuesta (renderiza el formulario de edición)
    return render(request, 'discoshdd/editar_hdd.html', {'form': form, 'hdd': hdd})

def eliminar_hdd(request, id_hdd):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    hdd = get_object_or_404(DiscoDuroHdd, id_hdd=id_hdd)
    
    if request.method == 'POST':
        try:
            hdd.delete()  
            return redirect('inicio')  # Redirigir a la lista de graficas
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar el HDD: {e}")
            return render(request, 'eliminar_hdd.html', {'hdd': hdd, 'error': 'Hubo un error al eliminar el HDD.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'discoshdd/eliminar_hdd.html', {'hdd': hdd})

#====================================================================================================================================
def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if (rol == Usuario.CLIENTE):
                cliente = Cliente.objects.create ( usuario = user)
                cliente.save()
            elif (rol == Usuario.TECNICOINFORMATICO):
                tecnicoinformatico = TecnicoInformatico.objects.create ( tecnicoinformatico = user)
                tecnicoinformatico.save()
            elif (rol == Usuario.VENDEDOR):
                vendedor = Vendedor.objects.create ( vendedor = user)
                vendedor.save()
    else: 
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario })