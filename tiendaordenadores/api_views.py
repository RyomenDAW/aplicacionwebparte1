from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from rest_framework import status
from django.shortcuts import get_object_or_404



@api_view(['GET'])
def placabases_list(request):
    placasbase = PlacaBase.objects.all()
    serializer = PlacaBaseSerializer(placasbase, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def procesador_list(request):
    procesadores = Procesador.objects.all()
    serializer = ProcesadorSerializer(procesadores, many=True)
    
    print(serializer.data)  # Verifica en la consola de Django
    
    return Response(serializer.data)



@api_view(['GET'])
def procesadores_mejorados(request):
    # Consulta optimizada con relaciones (ejemplo: incluir la marca del procesador)
    
    #optimizacion
    procesadores = Procesador.objects.select_related('placabase')  # Optimización de relaciones, retrieve de placabase
    
    serializer = ProcesadorMejoradoSerializer(procesadores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def grafica_list(request):
    graficas = Grafica.objects.all()  
    serializer = GraficaMejoradaSerializer(graficas, many=True)  # Serializamos los datos
    return Response(serializer.data)

# Vista para listar fuentes de alimentación
@api_view(['GET'])
def fuente_list(request): #Aqui la mejora es que pone el user
    fuentes = FuenteAlimentacion.objects.all()  
    serializer = FuenteAlimentacionMejoradaSerializer(fuentes, many=True)  
    return Response(serializer.data)

@api_view(['GET'])
def ram_list(request):  
    rams = Ram.objects.all()     
    serializer = RamMejoradaSerializer(rams, many=True)  
    return Response(serializer.data)


@api_view(['GET']) #Busqueda SIMPLE

def procesador_busqueda(request):
    # Obtener el texto de búsqueda desde el parámetro GET
    texto_busqueda = request.GET.get('textoBusqueda', '')
    print("Texto de búsqueda ACTUALL:", texto_busqueda)  # Agregar esta línea para depurar

    if texto_busqueda:
        # Filtrar procesadores por el nombre que contenga el texto de búsqueda
        procesadores = Procesador.objects.filter(nombre__icontains=texto_busqueda).all()
    else:
        # Si no hay texto de búsqueda, devolver todos los procesadores
        procesadores = Procesador.objects.all()
    # Serializar los procesadores
    serializer = ProcesadorSerializer(procesadores, many=True)
    
    # Devolver la respuesta con los datos serializados
    return Response(serializer.data)



@api_view(['GET']) #Busqueda AVANZADA
def procesador_busqueda_avanzada(request):

    # Filtros de búsqueda 
    nombre = request.GET.get('nombre', '')
    familia = request.GET.get('familiaprocesador', '')
    nucleos = request.GET.get('nucleos', None)
    hilos = request.GET.get('hilos', None)
    potencia_calculo = request.GET.get('potenciacalculo', None)
    
    procesadores = Procesador.objects.all()

    # Aplicamos los filtros si han sido proporcionados
    if nombre:
        procesadores = procesadores.filter(nombre__icontains=nombre)
    if familia:
        procesadores = procesadores.filter(familiaprocesador__icontains=familia)
    if nucleos:
        try:
            nucleos = int(nucleos)
            procesadores = procesadores.filter(nucleos=nucleos)
        except ValueError:
            pass  # Si no se puede convertir a entero, no filtramos por núcleos
    if hilos:
        try:
            hilos = int(hilos)
            procesadores = procesadores.filter(hilos=hilos)
        except ValueError:
            pass  # Si no se puede convertir a entero, no filtramos por hilos
    if potencia_calculo:
        try:
            potencia_calculo = float(potencia_calculo)
            procesadores = procesadores.filter(potenciacalculo=potencia_calculo)
        except ValueError:
            pass  # Si no se puede convertir a flotante, no filtramos por potencia de cálculo

    # Serializamos los resultados
    serializer = ProcesadorMejoradoSerializer(procesadores, many=True)
    
    return Response(serializer.data)



#=====================================================================================================
@api_view(['GET'])
def grafica_busqueda_avanzada_api(request):
    nombre = request.GET.get('nombre', '')
    familiagrafica = request.GET.get('familiagrafica', '')
    potencia = request.GET.get('potenciacalculo', None)
    graficas = Grafica.objects.all()

    if nombre:
        graficas = graficas.filter(nombre__icontains=nombre)
    if familiagrafica:
        graficas = graficas.filter(familiagrafica__icontains=familiagrafica)
    if potencia:
        potencia = int(potencia)  # Asegurarse de que el valor sea un número
        graficas = graficas.filter(potenciacalculo=potencia) #Este de aqui no funciona bien

    serializer = GraficaMejoradaSerializer(graficas, many=True)
    return Response(serializer.data)

# Vista para búsqueda avanzada de fuentes
@api_view(['GET'])
def fuente_busqueda_avanzada_api(request):
    vatios = request.GET.get('vatios', None)
    calidadfuente = request.GET.get('calidadfuente', '')
    amperaje = request.GET.get('amperaje', None)
    fuentes = FuenteAlimentacion.objects.all()

    if vatios:
        fuentes = fuentes.filter(vatios__icontains=vatios)
    if calidadfuente:
        fuentes = fuentes.filter(calidadfuente__icontains=calidadfuente)
    if amperaje:
        fuentes = fuentes.filter(amperaje=amperaje)

    serializer = FuenteAlimentacionMejoradaSerializer(fuentes, many=True)
    return Response(serializer.data)

# Vista para búsqueda avanzada de RAMS
@api_view(['GET'])
def ram_busqueda_avanzada_api(request):
    mhz = request.GET.get('mhz', None)
    familiaram = request.GET.get('familiaram', '')
    rgb = request.GET.get('rgb', None)
    rams = Ram.objects.all()

    if mhz:
        rams = rams.filter(mhz__icontains=mhz)
    if familiaram:
        rams = rams.filter(familiaram__icontains=familiaram)
    if rgb is not None:
        rams = rams.filter(rgb=rgb)

    serializer = RamMejoradaSerializer(rams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_procesador(request):
    
    print("📌 RECIBIDA PETICIÓN POST EN /template-api/procesadores/")  # DEBUG
    print("📌 DATOS RECIBIDOS:", request.data)  # DEBUG

    procesador_serializer = CrearProcesadorSerializer(data=request.data, context={'request': request})  

    if procesador_serializer.is_valid():
        try:
            procesador_serializer.save()
            return Response({"mensaje": "PROCESADOR CREADO CON ÉXITO"}, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(procesador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def obtener_y_actualizar_procesador(request, procesador_id):
    """ OBTIENE O ACTUALIZA UN PROCESADOR SEGÚN EL MÉTODO HTTP """

    # OBTENER PROCESADOR O DEVOLVER ERROR 404 SI NO EXISTE
    procesador = get_object_or_404(Procesador, id_procesador=procesador_id)

    if request.method == 'GET':
        serializer = ProcesadorSerializer(procesador)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        procesador_serializer = CrearProcesadorSerializer(instance=procesador, data=request.data)

        if procesador_serializer.is_valid():
            procesador_serializer.save()
            return Response({"mensaje": "Procesador actualizado correctamente SERVIDOR!"}, status=status.HTTP_200_OK)
        else:
            return Response(procesador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def actualizar_nombre_procesador(request, procesador_id):
    """ Vista para actualizar solo el nombre de un procesador con PATCH """
    procesador = get_object_or_404(Procesador, id_procesador=procesador_id)
    serializer = ProcesadorActualizarNombreSerializer(procesador, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Nombre actualizado correctamente"}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_procesador(request, procesador_id):
    """ Elimina un procesador por su ID """
    procesador = get_object_or_404(Procesador, id_procesador=procesador_id)
    
    try:
        procesador.delete()
        return Response({"mensaje": "✅ Procesador eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
def crear_grafica(request):
        """ API para crear una nueva gráfica """
        print("📌 RECIBIDA PETICIÓN POST EN /template-api/graficas/")  # DEBUG
        print("📌 DATOS RECIBIDOS:", request.data)  # DEBUG

        grafica_serializer = CrearGraficaSerializer(data=request.data, context={'request': request})

        if grafica_serializer.is_valid():
            try:
                grafica_serializer.save(user=request.user)
                return Response({"mensaje": "GRÁFICA CREADA CON ÉXITO"}, status=status.HTTP_201_CREATED)

            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(grafica_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT'])
def obtener_y_actualizar_grafica(request, grafica_id):
    """ OBTIENE O ACTUALIZA UNA GRÁFICA SEGÚN EL MÉTODO HTTP """

    # Obtener la gráfica o devolver error 404 si no existe
    grafica = get_object_or_404(Grafica, id_grafica=grafica_id)

    if request.method == 'GET':
        serializer = CrearGraficaSerializer(grafica)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        datos = request.data.copy()

        # Asegurar que el usuario autenticado sea el que está editando la gráfica
        if "user" not in datos or datos["user"] is None:
            if request.user.is_authenticated:
                datos["user"] = request.user.id  # Asignar usuario autenticado
            else:
                return Response({"error": "❌ Debes estar autenticado para actualizar una gráfica"}, status=status.HTTP_403_FORBIDDEN)

        # Validamos los datos con el serializador
        grafica_serializer = CrearGraficaSerializer(instance=grafica, data=datos)

        if grafica_serializer.is_valid():
            grafica_serializer.save()
            return Response({"mensaje": "✅ Gráfica actualizada correctamente!"}, status=status.HTTP_200_OK)
        else:
            return Response(grafica_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
def actualizar_nombre_grafica(request, grafica_id):
    """
    Actualiza solo el nombre de la gráfica con PATCH.
    """
    grafica = get_object_or_404(Grafica, id_grafica=grafica_id)
    
    nuevo_nombre = request.data.get("nombre", None)
    if not nuevo_nombre:
        return Response({"error": "El campo 'nombre' es obligatorio para esta actualización."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Validación: No permitir nombres repetidos
    if Grafica.objects.filter(nombre=nuevo_nombre).exclude(id_grafica=grafica_id).exists():
        return Response({"error": "Ya existe una gráfica con ese nombre."}, status=status.HTTP_400_BAD_REQUEST)

    grafica.nombre = nuevo_nombre
    grafica.save()

    return Response({"mensaje": "Nombre de la gráfica actualizado con éxito"}, status=status.HTTP_200_OK)



@api_view(["DELETE"])
def eliminar_grafica(request, grafica_id):
    """ Elimina una gráfica de la base de datos """
    grafica = get_object_or_404(Grafica, id_grafica=grafica_id)
    grafica.delete()
    return Response({"mensaje": "✅ Gráfica eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def crear_monitor_grafica(request):
    """ Crea una relación entre Monitor y Gráfica con validaciones """
    monitor_id = request.data.get("monitor")
    grafica_id = request.data.get("grafica")
    modo_conexion = request.data.get("modo_conexion")
    es_monitor_gaming = request.data.get("es_monitor_gaming", False)
    resolucion_maxima = request.data.get("resolucion_maxima", 1080)

    # ✅ Validaciones necesarias
    if not monitor_id or not grafica_id or not modo_conexion:
        return Response({"error": "Se requieren 'monitor', 'grafica' y 'modo_conexion'"}, status=status.HTTP_400_BAD_REQUEST)

    if modo_conexion not in ["HDMI", "DisplayPort", "VGA", "DVI"]:
        return Response({"error": "Modo de conexión inválido"}, status=status.HTTP_400_BAD_REQUEST)

    if int(resolucion_maxima) < 720 or int(resolucion_maxima) > 4320:
        return Response({"error": "Resolución no válida (debe estar entre 720p y 8K)"}, status=status.HTTP_400_BAD_REQUEST)

    monitor = get_object_or_404(Monitor, id_monitor=monitor_id)
    grafica = get_object_or_404(Grafica, id_grafica=grafica_id)

    relacion, created = MonitorGrafica.objects.get_or_create(
        monitor=monitor, 
        grafica=grafica, 
        modo_conexion=modo_conexion,
        es_monitor_gaming=es_monitor_gaming,
        resolucion_maxima=resolucion_maxima
    )

    if created:
        return Response({"mensaje": "Relación creada exitosamente"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"mensaje": "La relación ya existe"}, status=status.HTTP_200_OK)


### 🛠 **PUT - Actualizar Toda la Relación**

@api_view(['PUT', 'GET'])
def actualizar_monitor_grafica(request, relacion_id):
    """ Obtiene o actualiza toda la relación entre Monitor y Gráfica """

    # 📌 GET: Obtener la relación actual
    if request.method == "GET":
        relacion = get_object_or_404(MonitorGrafica, id=relacion_id)
        serializer = MonitorGraficaSerializer(relacion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 📌 PUT: Actualizar la relación
    elif request.method == "PUT":
        relacion = get_object_or_404(MonitorGrafica, id=relacion_id)

        monitor_id = request.data.get("monitor")
        grafica_id = request.data.get("grafica")
        modo_conexion = request.data.get("modo_conexion")
        es_monitor_gaming = request.data.get("es_monitor_gaming", False)
        resolucion_maxima = request.data.get("resolucion_maxima", 1080)

        if monitor_id:
            relacion.monitor = get_object_or_404(Monitor, id_monitor=monitor_id)
        if grafica_id:
            relacion.grafica = get_object_or_404(Grafica, id_grafica=grafica_id)
        if modo_conexion:
            if modo_conexion not in ["HDMI", "DisplayPort", "VGA", "DVI"]:
                return Response({"error": "Modo de conexión inválido"}, status=status.HTTP_400_BAD_REQUEST)
            relacion.modo_conexion = modo_conexion

        if int(resolucion_maxima) < 720 or int(resolucion_maxima) > 4320:
            return Response({"error": "Resolución no válida (debe estar entre 720p y 8K)"}, status=status.HTTP_400_BAD_REQUEST)

        relacion.resolucion_maxima = resolucion_maxima
        relacion.es_monitor_gaming = es_monitor_gaming
        relacion.save()

        return Response({"mensaje": "✅ Relación actualizada correctamente"}, status=status.HTTP_200_OK)



@api_view(['PATCH'])
def actualizar_grafica_en_relacion(request, relacion_id):
    """ Actualiza solo la tarjeta gráfica en una relación Monitor-Grafica """
    nueva_grafica_id = request.data.get("grafica")

    if not nueva_grafica_id:
        return Response({"error": "Se requiere el ID de la nueva gráfica"}, status=status.HTTP_400_BAD_REQUEST)

    relacion = get_object_or_404(MonitorGrafica, id=relacion_id)
    relacion.grafica = get_object_or_404(Grafica, id_grafica=nueva_grafica_id)

    relacion.save()
    return Response({"mensaje": "Gráfica actualizada correctamente"}, status=status.HTTP_200_OK)



### 🛠 **DELETE - Eliminar Relación**
@api_view(['DELETE'])
def eliminar_monitor_grafica(request, relacion_id):
    """ Elimina una relación Monitor-Grafica """
    relacion = get_object_or_404(MonitorGrafica, id=relacion_id)
    relacion.delete()
    return Response({"mensaje": "Relación eliminada correctamente"}, status=status.HTTP_200_OK)