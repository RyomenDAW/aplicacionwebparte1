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
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required


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
    # ==========================
    # Verificación si el usuario NO está autenticado (es anónimo)
    # ==========================
    if not request.user.is_authenticated:
        # Si el usuario no tiene la variable 'fecha_inicio' en la sesión, la creamos
        if "fecha_inicio" not in request.session:
            request.session["fecha_inicio"] = timezone.now().strftime('%d/%m/%Y %H:%M')
    
    # ==========================
    # Si el usuario está autenticado
    # ==========================
    else:
        # ==========================
        # Verificamos si existen las variables de sesión necesarias
        # ==========================
        
        # Establecemos la fecha de inicio de sesión si no está en la sesión
        if "fecha_inicio" not in request.session:
            request.session["fecha_inicio"] = timezone.now().strftime('%d/%m/%Y %H:%M')

        # ==========================
        # Establecemos el nombre completo del usuario en la sesión si no está presente
        # ==========================
        if "usuario_nombre" not in request.session:
            request.session["usuario_nombre"] = request.user.get_full_name()  # Usamos el nombre completo del usuario

        # ==========================
        # Establecemos el primer nombre del usuario en la sesión si no está presente
        # ==========================
        if "usuario_first_name" not in request.session:
            request.session["usuario_first_name"] = request.user.first_name  # Usamos el primer nombre del usuario

        # ==========================
        # Establecemos el rol del usuario en la sesión si no está presente
        # ==========================
        if "rol" not in request.session:
            # Accedemos al campo rol de request.user
            rol = request.user.rol
            print("Rol del usuario:", rol)  # Añade este print para debug

            if rol == 1:
                request.session['rol'] = 'Administrador'
            elif rol == 2:
                request.session['rol'] = 'Cliente'
            elif rol == 3:
                request.session['rol'] = 'Técnico Informático'
            elif rol == 4:
                request.session['rol'] = 'Vendedor'
            else:
                request.session['rol'] = 'Desconocido/No disponible'

        # ==========================
        # Establecemos el correo electrónico del usuario en la sesión si no está presente
        # ==========================
        if "usuario_email" not in request.session:
            request.session["usuario_email"] = request.user.email

    # ==========================
    # Renderizamos la página de inicio con las variables de sesión definidas
    # ==========================
    return render(request, 'home/index.html')



#=================================================================================================================================================================


from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .models import Procesador, Grafica
from django.db.models import Avg
from django.db.models import Q

#=================================================================================================================================================================

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA

@login_required
@permission_required('tiendaordenadores.view_procesador', raise_exception=True)
def lista_procesadores(request):
    procesadores = Procesador.objects.all()  
    return render(request, 'procesadores/lista_procesadores.html', {'procesadores': procesadores})

#=================================================================================================================================================================

# USANDO UN PARAMETRO ENTERO.

#ESTA VISTA DEVOLVERÁ TODOS LOS PROCESADORES QUE TENGAN EL NUMERO DE HILOS EXACTO QUE SE LE PASA, ES UN INTEGER, PUEDE SER NEGATIVO EL VALOR.
#TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA AL PROCESADOR

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA

@login_required
@permission_required('tiendaordenadores.view_procesador', raise_exception=True)
def lista_procesadores_segunhilos(request, numero_hilos):
    procesadores = Procesador.objects.filter(hilos = numero_hilos).all()
    return render (request, 'procesadores/lista_procesadores_segunhilos.html', {'procesadores': procesadores})

#=================================================================================================================================================================

#USANDO UN PARAMETRO TIPO STRING

#ESTA VISTA DEVOLVERÁ TODOS LOS PROCESADORES QUE PERTENEZCAN A LA FAMILIA QUE SE LE INDIQUE COMO PARAMETRO, POR EJEMPLO 'Intel', Y FILTRARÁ LOS PROCESADORES
#EN CONSECUENCIA, TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA AL PROCESADOR.

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA

@login_required
@permission_required('tiendaordenadores.view_procesador', raise_exception=True)
def lista_procesadores_segunfamilia(request, nombre_familia):
    #Aqui es un choices realmente, pero funcionaria de todas maneras ya que el campo es de tipo text (String)
    procesadores = Procesador.objects.filter(familiaprocesador = nombre_familia).all()
    return render (request, 'procesadores/lista_procesadores_segunfamilia.html', {'procesadores': procesadores})

#=================================================================================================================================================================

#USANDO DOS PARAMETROS
#ESTA VISTA DEVOLVERÁ LA LISTA DE GRAFICAS QUE CUMPLAN AMBOS PARAMETROS, EL ATRIBUTO DE SU FAMILIA (Ejemplo: 'Nvidia') y LA CANTIDAD DE VRAM ASIGNADA, 
#EN CONSECUENCIA, TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA A LA GRAFICA.

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA

@login_required
@permission_required('tiendaordenadores.view_procesador', raise_exception=True)
def lista_graficas_segunfamilia_y_vram(request, nombre_familia, cantidad_vram):
    graficas = Grafica.objects.filter(familiagrafica = nombre_familia, memoriavram = cantidad_vram ).all()
    return render (request, 'graficas/lista_graficas_segunfamilia_y_vram.html', {'graficas': graficas})

#=================================================================================================================================================================

#SE UTILIZA LA PARTE DE AGGREGATE QUE SE TENIA QUE INVESTIGAR, SE UTILIZA PARA PODER HACER AGREGACIONES SIN CARGAR EN LA MEMORIA TODOS LOS VALORES Y DEVOLVER EL
#RESULTADO DE LAS OPERACIONES REALIZADAS CON ESOS VALORES, AHORRANDO RECURSO Y OPTIMIZANDO.

#La vista nos obtiene la media (avg) del campo nucleos de todos los objetos en el modelo Procesador, tener en cuenta que es negativo algunos valores.

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA

@login_required
@permission_required('tiendaordenadores.view_procesador', raise_exception=True)
def promedio_nucleos(request):
    promedio_nucleos = Procesador.objects.aggregate(promedio_nucleos=Avg('nucleos'))
    return render(request, 'procesadores/promedio_nucleos.html', {'promedio_nucleos': promedio_nucleos})

#=================================================================================================================================================================

#ESTA VISTA NOS DEVUELVE A TRAVES DE UN FILTER CON UN AND OBLIGATORIO Y DENTRO DE 2 OR, QUE POR LO MENOS SE CUMPLA UNO

#En este caso: procesadores que tengan más de 8 núcleos o que pertenezcan a la familia 'Intel', pero que además tengan más de 12 hilos (greaterthan)

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA

@login_required
@permission_required('tiendaordenadores.view_procesador', raise_exception=True)
def filtrar8nucleos_OR_intel_AND_12hilos(request):
    procesadores = Procesador.objects.filter(  (Q(nucleos__gt=8) | Q(familiaprocesador='Intel')) & Q(hilos__gt=12) ).all()
    return render( request,  'procesadores/filtrar8nucleos_OR_intel_AND_12hilos.html', {'procesadores': procesadores} )



#=================================================================================================================================================================


#=================================================================================================================================================================

#ESTA VISTA NOS DEVUELVE A TRAVES DE UN FILTER CON UN AND OBLIGATORIO Y DENTRO DE 2 OR, QUE POR LO MENOS SE CUMPLA UNO

#En este caso: procesadores que tengan más de 8 núcleos o que pertenezcan a la familia 'Intel', pero que además tengan más de 12 hilos (greaterthan)
# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA
@login_required
@permission_required('tiendaordenadores.view_procesador', raise_exception=True)
def filtrar8nucleos_OR_intel_AND_12hilos(request):
    procesadores = Procesador.objects.filter(  (Q(nucleos__gt=8) | Q(familiaprocesador='Intel')) & Q(hilos__gt=12) ).all()
    return render( request,  'procesadores/filtrar8nucleos_OR_intel_AND_12hilos.html', {'procesadores': procesadores} )

#=================================================================================================================================================================

#ESTA VISTA DEVUELVE CON UN FILTRO DE ORDER BY QUE SERIA DE FORMA DESCEDENTE, LA FECHA, TODAS LAS GRAFICAS AL SER CON SEEDERS SALEN CON LA MISMA FECHA.

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA
@login_required
@permission_required('tiendaordenadores.view_grafica', raise_exception=True)
def filtrargraficas_segunfecha(request):
    graficas = Grafica.objects.order_by('-fecha_salida')
    return render ( request, 'graficas/filtrargraficas_segunfecha.html', {'graficas': graficas })

#=================================================================================================================================================================

# ESTA VISTA OBTIENE UNA GRAFICA ESPECIFICA SEGUN SU ID Y DEVUELVE LOS PROCESADORES ASOCIADOS A ESA GRAFICA.
# SI NO EXISTE LA GRAFICA, GENERARA UN ERROR.
# UTILIZA EL NOMBRE RELACIONADO PARA FILTRAR LOS PROCESADORES CONECTADOS, ESTOS DEVUELVEN TAMBIEN TODOS SUS ATRIBUTOS.

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA
@login_required
@permission_required('tiendaordenadores.view_grafica', raise_exception=True)
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

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA
@login_required
@permission_required('tiendaordenadores.view_discodurossd', raise_exception=True)
def primeros_5_ssd(request):
    # Obtener las primeras 5 instancias de DiscoDuroSsd según su ID
    ssds = DiscoDuroSsd.objects.all()[:5]

    return render(request, 'ssd/primeros_5_ssd.html', {
        'ssds': ssds,
    })

#=================================================================================================================================================================

#ESTA VISTA DEVOLVERA TODAS LAS GRAFICAS SIN CUELLO DE BOTELLA, ES DECIR, TODAS AQUELLAS GRAFICAS QUE TENGAN EN LA RELACION MANYTOMANY (GRAFICAPROCESADOR), EL ATRIBUTO
#DE CUELLODEBOTELLA EN 0 (FALSE), ADEMAS TE INCLUIRE A QUE PROCESADOR VA ASOCIADA ESA GRAFICA, Y LOS ATRIBUTOS DE ESTE.

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA
@login_required
@permission_required('tiendaordenadores.view_grafica', raise_exception=True)
def graficas_sin_cuello_de_botella(request):
    # Filtrar las relaciones donde cuellodebotella es None (o False (0), si es un BooleanField)
    graficas_sin_cuello = GraficaProcesador.objects.filter(cuellodebotella=False)  # O None si lo defines como Nullable

    return render(request, 'intermedia/graficas_sin_cuello_de_botella.html', {
        'graficas_sin_cuello': graficas_sin_cuello,
    })

#=================================================================================================================================================================

#ESTA VISTA DEVOLVERÁ TODAS LAS GRAFICAS CON SUS CARACTERÍSTICAS (ATRIBUTOS), TAMBIEN INCLUIRA DENTRO DEL HTML EL ATRIBUTO DE LA PLACA BASE QUE VA ASOCIADA
#A LA TARJETA GRAFICA

# REQUIERE LOGIN Y PERMISO PARA VER LA VISTA
@login_required
@permission_required('tiendaordenadores.view_grafica', raise_exception=True)
def lista_graficas(request):
    graficas = Grafica.objects.all()
    return render (request, 'graficas/lista_graficas.html', {'graficas': graficas})
#=================================================================================================================================================================



#No se si te molestan las lineas pero yo lo veo mejor asi, de aqui en adelante empieza CRUD

#=================================================================================================================================================================


from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Procesador
from .forms import ProcesadorForm, BusquedaAvanzadaProcesador, BusquedaAvanzadaGrafica

#=================================================================================================================================================================

# VISTA PARA CREAR UN NUEVO PROCESADOR
# REQUIERE LOGIN Y PERMISO PARA CREAR PROCESADORES
@permission_required('tiendaordenadores.add_procesador', raise_exception=True)
@login_required  # Asegura que solo los usuarios autenticados puedan crear un procesador
def crear_procesador(request):
    if request.method == 'POST':
        form = ProcesadorForm(request.POST, request.FILES)
        if form.is_valid():
            procesador = form.save(commit=False)
            procesador.user = request.user  # Asigna el usuario autenticado (es una instancia de User)
            procesador.save()  # Guarda el procesador con el usuario asignado
            return redirect('inicio')  # Redirige a la lista de procesadores o cualquier otra vista
    else:
        form = ProcesadorForm()

    return render(request, 'procesadores/crear_procesador.html', {'form': form})

#=================================================================================================================================================================
# VISTA PARA LEER (FILTRAR) LOS PROCESADORES
# REQUIERE LOGIN Y PERMISO PARA VER PROCESADORES
@login_required
@permission_required('tiendaordenadores.view_procesador', raise_exception=True)
def read_procesadores(request):
    form = BusquedaAvanzadaProcesador(request.GET)

    # Inicializamos la consulta base para filtrar por el usuario autenticado
    procesadores = Procesador.objects.filter(user=request.user)  # Solo los procesadores del usuario logueado

    # Verifica que el formulario se está enviando correctamente
    if form.is_valid():
        nombre = form.cleaned_data.get('nombreBusqueda')
        nucleos = form.cleaned_data.get('nucleos')
        hilos = form.cleaned_data.get('hilos')
        familiaprocesador = form.cleaned_data.get('familiaprocesador')

        # Aplica los filtros adicionales si los valores fueron proporcionados en el formulario
        if nombre:
            procesadores = procesadores.filter(nombre__icontains=nombre)
        if nucleos:
            procesadores = procesadores.filter(nucleos=nucleos)
        if hilos:
            procesadores = procesadores.filter(hilos=hilos)
        if familiaprocesador:
            procesadores = procesadores.filter(familiaprocesador__in=familiaprocesador)

    return render(request, 'procesadores/read_procesadores.html', {'form': form, 'procesadores': procesadores})
#=================================================================================================================================================================

# VISTA PARA EDITAR UN PROCESADOR
# REQUIERE LOGIN Y PERMISO PARA EDITAR PROCESADORES
@login_required
@permission_required('tiendaordenadores.change_procesador', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA ELIMINAR UN PROCESADOR
# REQUIERE LOGIN Y PERMISO PARA ELIMINAR PROCESADORES
@login_required
@permission_required('tiendaordenadores.delete_procesador', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA CREAR UNA NUEVA GRAFICA
# REQUIERE LOGIN Y PERMISO PARA CREAR GRAFICAS
@login_required
@permission_required('tiendaordenadores.add_grafica', raise_exception=True)
def crear_grafica(request):
    if request.method == 'POST':
        form = GraficaForm(request.POST, request.FILES)  # Si estás subiendo un archivo, también usa request.FILES
        if form.is_valid():
            grafica = form.save(commit=False)  # No guarda aún
            grafica.user = request.user  # Asigna el usuario autenticado
            grafica.save()  # Guarda la gráfica con el usuario asignado
            return redirect('lista_graficas')  # Redirige a la lista de gráficas (ajusta el nombre de la URL si es necesario)
    else:
        form = GraficaForm()  # Si no es POST, simplemente crea el formulario vacío

    return render(request, 'graficas/crear_grafica.html', {'form': form})




#=================================================================================================================================================================

# VISTA PARA LEER (FILTRAR) LAS GRAFICAS
# REQUIERE LOGIN Y PERMISO PARA VER GRAFICAS
@login_required
@permission_required('tiendaordenadores.view_grafica', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA EDITAR UNA GRAFICA
# REQUIERE LOGIN Y PERMISO PARA EDITAR GRAFICAS
@login_required
@permission_required('tiendaordenadores.change_grafica', raise_exception=True)
def editar_grafica(request, id_grafica):
    grafica = get_object_or_404(Grafica, id_grafica=id_grafica)  # Recupera la gráfica por id
    if request.method == 'POST':
        form = GraficaForm(request.POST, instance=grafica)
        if form.is_valid():
            form.save()
            return redirect('lista_graficas')
    else:
        form = GraficaForm(instance=grafica)
    
    return render(request, 'graficas/editar_grafica.html', {'form': form, 'grafica': grafica})

#=================================================================================================================================================================

# VISTA PARA ELIMINAR UNA GRAFICA
# REQUIERE LOGIN Y PERMISO PARA ELIMINAR GRAFICAS
@login_required
@permission_required('tiendaordenadores.delete_grafica', raise_exception=True)
def eliminar_grafica(request, id_grafica):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    grafica = get_object_or_404(Grafica, id_grafica=id_grafica)
    
    if request.method == 'POST':
        try:
            grafica.delete()  # Eliminar la gráfica de la base de datos
            return redirect('lista_graficas')  # Redirigir a la lista de gráficas
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar la gráfica: {e}")
            return render(request, 'eliminar_grafica.html', {'grafica': grafica, 'error': 'Hubo un error al eliminar la gráfica.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'graficas/eliminar_grafica.html', {'grafica': grafica})

#=================================================================================================================================================================

# VISTA PARA CREAR UN MONITOR
# REQUIERE LOGIN Y PERMISO PARA CREAR MONITORES
@login_required
@permission_required('tiendaordenadores.add_monitor', raise_exception=True)
def crear_monitor(request):
    if request.method == 'POST':
        form = MonitorForm(request.POST)
        if form.is_valid():
            monitor = form.save(commit=False)  # No guarda aún
            monitor.user = request.user  # Asigna el usuario autenticado
            monitor.save()  # Guarda el monitor con el usuario asignado
            return redirect('inicio')  # Redirige usando el nombre de la vista
    else:
        form = MonitorForm()

    return render(request, 'monitores/crear_monitor.html', {'form': form})

#=================================================================================================================================================================

# VISTA PARA LEER (FILTRAR) MONITORES
# REQUIERE LOGIN Y PERMISO PARA VER MONITORES
@login_required
@permission_required('tiendaordenadores.view_monitor', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA EDITAR UN MONITOR
# REQUIERE LOGIN Y PERMISO PARA EDITAR MONITORES
@login_required
@permission_required('tiendaordenadores.change_monitor', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA ELIMINAR UN MONITOR
# REQUIERE LOGIN Y PERMISO PARA ELIMINAR MONITORES
@login_required
@permission_required('tiendaordenadores.delete_monitor', raise_exception=True)
def eliminar_monitor(request, id_monitor):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    monitor = get_object_or_404(Monitor, id_monitor=id_monitor)
    
    if request.method == 'POST':
        try:
            monitor.delete()  # Eliminar el monitor de la base de datos
            return redirect('inicio')  # Redirigir a la lista de monitores
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar el monitor: {e}")
            return render(request, 'eliminar_monitor.html', {'monitor': monitor, 'error': 'Hubo un error al eliminar el monitor.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'monitores/eliminar_monitor.html', {'monitor': monitor})

#=================================================================================================================================================================


# VISTA PARA CREAR UNA FUENTE DE ALIMENTACIÓN
# REQUIERE LOGIN Y PERMISO PARA CREAR FUENTES
@login_required
@permission_required('tiendaordenadores.add_fuentealimentacion', raise_exception=True)
def crear_fuente(request):
    if request.method == 'POST':
        form = FuenteForm(request.POST)
        if form.is_valid():
            fuente = form.save(commit=False)  # No guarda aún
            fuente.user = request.user  # Asigna el usuario autenticado
            fuente.save()  # Guarda el fuente con el usuario asignado
            return redirect('inicio')  # Redirige usando el nombre de la vista
    else:
        form = FuenteForm()

    return render(request, 'fuentes/crear_fuente.html', {'form': form})

#=================================================================================================================================================================

# VISTA PARA LEER (FILTRAR) FUENTES DE ALIMENTACIÓN
# REQUIERE LOGIN Y PERMISO PARA VER FUENTES
@login_required
@permission_required('tiendaordenadores.view_fuentealimentacion', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA EDITAR UNA FUENTE DE ALIMENTACIÓN
# REQUIERE LOGIN Y PERMISO PARA EDITAR FUENTES
@login_required
@permission_required('tiendaordenadores.change_fuentealimentacion', raise_exception=True)
def editar_fuente(request, id_fuente):
    fuente = get_object_or_404(FuenteAlimentacion, id_fuente=id_fuente) 
    
    if request.method == "POST":
        # Crear el formulario con los datos del POST y la instancia de la fuente
        form = FuenteForm(request.POST, instance=fuente)
        
        if form.is_valid():
            # Si el formulario es válido, guardar los cambios
            form.save()
            return redirect('inicio')

    else:
        # Si no es un POST, simplemente cargar el formulario con los valores actuales de la fuente
        form = FuenteForm(instance=fuente)

    return render(request, 'fuentes/editar_fuente.html', {'form': form, 'fuente': fuente})

#=================================================================================================================================================================

# VISTA PARA ELIMINAR UNA FUENTE DE ALIMENTACIÓN
# REQUIERE LOGIN Y PERMISO PARA ELIMINAR FUENTES
@login_required
@permission_required('tiendaordenadores.delete_fuentealimentacion', raise_exception=True)
def eliminar_fuente(request, id_fuente):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    fuente = get_object_or_404(FuenteAlimentacion, id_fuente=id_fuente)
    
    if request.method == 'POST':
        try:
            fuente.delete()  # Eliminar la fuente de alimentación de la base de datos
            return redirect('inicio')  # Redirigir a la lista de fuentes
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar la fuente: {e}")
            return render(request, 'fuentes/eliminar_fuente.html', {'fuente': fuente, 'error': 'Hubo un error al eliminar la fuente.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'fuentes/eliminar_fuente.html', {'fuente': fuente})

#=================================================================================================================================================================

# VISTA PARA CREAR UNA RAM
# REQUIERE LOGIN Y PERMISO PARA CREAR RAM
@login_required
@permission_required('tiendaordenadores.add_ram', raise_exception=True)
def crear_ram(request):
    if request.method == 'POST':
        form = RamForm(request.POST)
        if form.is_valid():
            ram = form.save(commit=False)  # No guarda aún
            ram.user = request.user  # Asigna el usuario autenticado
            ram.save()  # Guarda la ram con el usuario asignado            
            return redirect('inicio')  # Redirige usando el nombre de la vista
    else:
        form = RamForm()

    return render(request, 'ram/crear_ram.html', {'form': form})

#=================================================================================================================================================================

# VISTA PARA LEER (FILTRAR) RAM
# REQUIERE LOGIN Y PERMISO PARA VER RAM
@login_required
@permission_required('tiendaordenadores.view_ram', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA EDITAR UNA RAM
# REQUIERE LOGIN Y PERMISO PARA EDITAR RAM
@login_required
@permission_required('tiendaordenadores.change_ram', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA ELIMINAR UNA RAM
# REQUIERE LOGIN Y PERMISO PARA ELIMINAR RAM
@login_required
@permission_required('tiendaordenadores.delete_ram', raise_exception=True)
def eliminar_ram(request, id_ram):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    ram = get_object_or_404(Ram, id_ram=id_ram)
    
    if request.method == 'POST':
        try:
            ram.delete()  # Eliminar la RAM de la base de datos
            return redirect('inicio')  # Redirigir a la lista de RAM
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar la RAM: {e}")
            return render(request, 'ram/eliminar_ram.html', {'ram': ram, 'error': 'Hubo un error al eliminar la RAM.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'ram/eliminar_ram.html', {'ram': ram})

#=================================================================================================================================================================
# VISTA PARA CREAR UN DISCO DURO HDD
# REQUIERE LOGIN Y PERMISO PARA CREAR HDD
@login_required
@permission_required('tiendaordenadores.add_discodurohdd', raise_exception=True)
def crear_hdd(request):
    if request.method == 'POST':
        form = HDDForm(request.POST)
        if form.is_valid():
            hdd = form.save(commit=False)  # No guarda aún
            hdd.user = request.user  # Asigna el usuario autenticado
            hdd.save()  # Guarda el hdd con el usuario asignado   
            return redirect('inicio')  # Redirige usando el nombre de la vista
    else:
        form = HDDForm()

    return render(request, 'discoshdd/crear_hdd.html', {'form': form})

#=================================================================================================================================================================

# VISTA PARA LEER (FILTRAR) HDD
# REQUIERE LOGIN Y PERMISO PARA VER HDD
@login_required
@permission_required('tiendaordenadores.view_discodurohdd', raise_exception=True)
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

#=================================================================================================================================================================

# VISTA PARA EDITAR UN DISCO DURO HDD
# REQUIERE LOGIN Y PERMISO PARA EDITAR HDD
@login_required
@permission_required('tiendaordenadores.change_discodurohdd', raise_exception=True)
def editar_hdd(request, id_hdd):
    # Recupera el objeto DiscoDuroHdd específico
    hdd = get_object_or_404(DiscoDuroHdd, id_hdd=id_hdd)
    
    # Si el método de la solicitud es POST, procesamos el formulario con los datos del usuario
    if request.method == 'POST':
        form = HDDForm(request.POST, instance=hdd)
        if form.is_valid():
            form.save()
            return redirect('inicio') 
    else:
        form = HDDForm(instance=hdd)  # Cargar el formulario con los datos actuales del disco duro

    # Siempre devolver una respuesta (renderiza el formulario de edición)
    return render(request, 'discoshdd/editar_hdd.html', {'form': form, 'hdd': hdd})

#=================================================================================================================================================================

# VISTA PARA ELIMINAR UN DISCO DURO HDD
# REQUIERE LOGIN Y PERMISO PARA ELIMINAR HDD
@login_required
@permission_required('tiendaordenadores.delete_discodurohdd', raise_exception=True)
def eliminar_hdd(request, id_hdd):
    # Usamos get_object_or_404 para manejar objetos inexistentes
    hdd = get_object_or_404(DiscoDuroHdd, id_hdd=id_hdd)
    
    if request.method == 'POST':
        try:
            hdd.delete()  # Eliminar el disco duro de la base de datos
            return redirect('inicio')  # Redirigir a la lista de discos duros
        except Exception as e:
            # Manejar cualquier error de eliminación (aunque no es común)
            print(f"Error al eliminar el HDD: {e}")
            return render(request, 'discoshdd/eliminar_hdd.html', {'hdd': hdd, 'error': 'Hubo un error al eliminar el HDD.'})
    
    # Si el método es GET, mostramos la página de confirmación
    return render(request, 'discoshdd/eliminar_hdd.html', {'hdd': hdd})
#====================================================================================================================================
from django.contrib.auth.models import Group

def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()  # Guardar el usuario

            rol = int(formulario.cleaned_data.get('rol'))
            if rol == Usuario.CLIENTE:
                cliente = Cliente.objects.create(usuario=user)  # Asociar el usuario como cliente
                cliente.save()
            elif rol == Usuario.TECNICOINFORMATICO:
                grupo = Group.objects.get(name="TecnicosInformaticos")
                grupo.user_set.add(user)
                tecnicoinformatico = TecnicoInformatico.objects.create(usuario=user)  # Asociar el usuario como técnico informático
                tecnicoinformatico.save()
            elif rol == Usuario.VENDEDOR:
                grupo = Group.objects.get(name="Vendedores")
                grupo.user_set.add(user)
                vendedor = Vendedor.objects.create(usuario=user,marca=formulario.cleaned_data['marca'])  # Asociar el usuario como vendedor
                vendedor.save()
                
            
            # Redirigir al usuario a la página principal despues del form, ya que no tiene sentido quedarse en el formulario

        
            login(request, user)
            
            
            if request.user.is_authenticated:
                print("Usuario autenticado:", request.user.username)
            else:
                print("Error: Usuario no autenticado")


            return redirect('inicio')
        
        


    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

def logout_view(request):
    logout(request)  # Desloguear al usuario
    request.session.flush()  # Eliminar todas las variables de la sesión

    return redirect('login')  # Redirigir al login después de logout


#=======================================================================================================================================0
# class CustomTokenObtainPairView(TokenObtainPairView):
#   serializer_class = CustomTokenObtainPairSerializer
  
  
  #viewset
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Procesador
from .serializers import ProcesadorSerializer


class ProcesadorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar procesadores (CRUD completo)
    """
queryset = Procesador.objects.all()
serializer_class = ProcesadorSerializer
permission_classes = [IsAuthenticated]

def perform_create(self, serializer):
        """
        Asigna automáticamente el usuario autenticado al crear un procesador
        """
        serializer.save(user=self.request.user)
  
  
  
  
  
#========================================================================================================================================

from django.http import HttpResponse
from django.shortcuts import redirect
import requests



# def oidc_callback(request):
#     """Handle the authorization code callback and exchange for tokens"""
#     code = request.GET.get("code")
#     if not code:
#         return HttpResponse("Error: No authorization code found.", status=400)

#     # Exchange code for tokens
#     token_data = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": REDIRECT_URI,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#     }

#     response = requests.post(OIDC_TOKEN_URL, data=token_data)

#     if response.status_code == 200:
#         tokens = response.json()
#         return HttpResponse(f"Access Token: {tokens.get('access_token')}")
#     else:
#         return HttpResponse(f"Token request failed: {response.text}", status=400)
