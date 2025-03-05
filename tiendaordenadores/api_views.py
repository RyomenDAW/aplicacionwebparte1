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


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Procesador
from .serializers import CrearProcesadorSerializer, ProcesadorSerializer, ProcesadorActualizarNombreSerializer
#=============================================================================================================================
# 🔹 Crear un procesador (Solo Vendedor y Administrador)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_procesador(request):
    if request.user.rol not in [1, 4]:  # Solo Administrador (1) y Vendedor (4)
        return Response({"error": "No tienes permisos para crear procesadores."}, status=status.HTTP_403_FORBIDDEN)

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

# 🔹 Obtener y actualizar procesador (Solo Técnico Informático y Administrador)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def obtener_y_actualizar_procesador(request, procesador_id):
    procesador = get_object_or_404(Procesador, id_procesador=procesador_id)

    if request.method == 'GET':
        serializer = ProcesadorSerializer(procesador)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        if request.user.rol not in [1, 3]:  # Solo Administrador (1) y Técnico Informático (3)
            return Response({"error": "No tienes permisos para actualizar procesadores."}, status=status.HTTP_403_FORBIDDEN)

        procesador_serializer = CrearProcesadorSerializer(instance=procesador, data=request.data)

        if procesador_serializer.is_valid():
            procesador_serializer.save()
            return Response({"mensaje": "Procesador actualizado correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response(procesador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Actualizar solo el nombre del procesador (Solo Técnico Informático y Administrador)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_nombre_procesador(request, procesador_id):
    if request.user.rol not in [1, 3]:  # Solo Administrador (1) y Técnico Informático (3)
        return Response({"error": "No tienes permisos para actualizar nombres de procesadores."}, status=status.HTTP_403_FORBIDDEN)

    procesador = get_object_or_404(Procesador, id_procesador=procesador_id)
    serializer = ProcesadorActualizarNombreSerializer(procesador, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Nombre actualizado correctamente"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Eliminar un procesador (Solo Vendedor y Administrador)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_procesador(request, procesador_id):
    if request.user.rol not in [1, 4]:  # Solo Administrador (1) y Vendedor (4)
        return Response({"error": "No tienes permisos para eliminar procesadores."}, status=status.HTTP_403_FORBIDDEN)

    procesador = get_object_or_404(Procesador, id_procesador=procesador_id)

    try:
        procesador.delete()
        return Response({"mensaje": "✅ Procesador eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#=============================================================================================================================


# 🔹 Crear una gráfica (Solo Vendedor y Administrador)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_grafica(request):
    """ API para crear una nueva gráfica """

    if request.user.rol not in [1, 4]:  # Solo Administrador (1) y Vendedor (4)
        return Response({"error": "No tienes permisos para crear gráficas."}, status=status.HTTP_403_FORBIDDEN)

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

# 🔹 Obtener y actualizar una gráfica (Solo Técnico Informático y Administrador)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def obtener_y_actualizar_grafica(request, grafica_id):
    """ OBTIENE O ACTUALIZA UNA GRÁFICA SEGÚN EL MÉTODO HTTP """

    grafica = get_object_or_404(Grafica, id_grafica=grafica_id)

    if request.method == 'GET':
        serializer = CrearGraficaSerializer(grafica)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if request.user.rol not in [1, 3]:  # Solo Administrador (1) y Técnico Informático (3)
            return Response({"error": "No tienes permisos para actualizar gráficas."}, status=status.HTTP_403_FORBIDDEN)

        datos = request.data.copy()

        # Asegurar que el usuario autenticado es el que edita la gráfica
        if "user" not in datos or datos["user"] is None:
            if request.user.is_authenticated:
                datos["user"] = request.user.id  # Asignar usuario autenticado
            else:
                return Response({"error": "❌ Debes estar autenticado para actualizar una gráfica"}, status=status.HTTP_403_FORBIDDEN)

        grafica_serializer = CrearGraficaSerializer(instance=grafica, data=datos)

        if grafica_serializer.is_valid():
            grafica_serializer.save()
            return Response({"mensaje": "✅ Gráfica actualizada correctamente!"}, status=status.HTTP_200_OK)
        else:
            return Response(grafica_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Actualizar solo el nombre de la gráfica (Solo Técnico Informático y Administrador)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_nombre_grafica(request, grafica_id):
    """ Actualiza solo el nombre de la gráfica con PATCH. """

    if request.user.rol not in [1, 3]:  # Solo Administrador (1) y Técnico Informático (3)
        return Response({"error": "No tienes permisos para actualizar nombres de gráficas."}, status=status.HTTP_403_FORBIDDEN)

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

# 🔹 Eliminar una gráfica (Solo Vendedor y Administrador)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def eliminar_grafica(request, grafica_id):
    """ Elimina una gráfica de la base de datos """

    if request.user.rol not in [1, 4]:  # Solo Administrador (1) y Vendedor (4)
        return Response({"error": "No tienes permisos para eliminar gráficas."}, status=status.HTTP_403_FORBIDDEN)

    grafica = get_object_or_404(Grafica, id_grafica=grafica_id)
    
    try:
        grafica.delete()
        return Response({"mensaje": "✅ Gráfica eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#=====================================================================================================================================

# 🔹 Crear relación Monitor-Grafica (Solo Vendedor y Administrador)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_monitor_grafica(request):
    """ Crea una relación entre Monitor y Gráfica con validaciones """

    if request.user.rol not in [1, 4]:  # Solo Administrador (1) y Vendedor (4)
        return Response({"error": "No tienes permisos para crear relaciones Monitor-Grafica."}, status=status.HTTP_403_FORBIDDEN)

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


### 🔹 Obtener y actualizar relación Monitor-Grafica (Solo Técnico Informático y Administrador)
@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated])
def actualizar_monitor_grafica(request, relacion_id):
    """ Obtiene o actualiza toda la relación entre Monitor y Gráfica """

    relacion = get_object_or_404(MonitorGrafica, id=relacion_id)

    # 📌 GET: Obtener la relación actual (Cualquiera autenticado puede verla)
    if request.method == "GET":
        serializer = MonitorGraficaSerializer(relacion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 📌 PUT: Actualizar la relación
    elif request.method == "PUT":
        if request.user.rol not in [1, 3]:  # Solo Administrador (1) y Técnico Informático (3)
            return Response({"error": "No tienes permisos para actualizar relaciones Monitor-Grafica."}, status=status.HTTP_403_FORBIDDEN)

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


# 🔹 Actualizar solo la gráfica en la relación (Solo Técnico Informático y Administrador)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_grafica_en_relacion(request, relacion_id):
    """ Actualiza solo la tarjeta gráfica en una relación Monitor-Grafica """

    if request.user.rol not in [1, 3]:  # Solo Administrador (1) y Técnico Informático (3)
        return Response({"error": "No tienes permisos para actualizar gráficas en relaciones Monitor-Grafica."}, status=status.HTTP_403_FORBIDDEN)

    nueva_grafica_id = request.data.get("grafica")

    if not nueva_grafica_id:
        return Response({"error": "Se requiere el ID de la nueva gráfica"}, status=status.HTTP_400_BAD_REQUEST)

    relacion = get_object_or_404(MonitorGrafica, id=relacion_id)
    relacion.grafica = get_object_or_404(Grafica, id_grafica=nueva_grafica_id)

    relacion.save()
    return Response({"mensaje": "Gráfica actualizada correctamente"}, status=status.HTTP_200_OK)


# 🔹 Eliminar relación Monitor-Grafica (Solo Vendedor y Administrador)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_monitor_grafica(request, relacion_id):
    """ Elimina una relación Monitor-Grafica """

    if request.user.rol not in [1, 4]:  # Solo Administrador (1) y Vendedor (4)
        return Response({"error": "No tienes permisos para eliminar relaciones Monitor-Grafica."}, status=status.HTTP_403_FORBIDDEN)

    relacion = get_object_or_404(MonitorGrafica, id=relacion_id)
    
    try:
        relacion.delete()
        return Response({"mensaje": "✅ Relación eliminada correctamente"}, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#=====================================================================================================================================
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UsuarioSerializerRegistro

class RegistrarUsuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.models import AccessToken


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_usuario_token(request):
    """ Devuelve los datos del usuario autenticado usando su token """
    usuario = request.user
    return Response({
        "id": usuario.id,
        "username": usuario.username,
        "email": usuario.email,
        "rol": usuario.rol
    })
    
#==============================================================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_usuario_autenticado(request):
    """ Devuelve la información del usuario autenticado """
    usuario = request.user
    return Response({
        "id": usuario.id,
        "username": usuario.username,
        "email": usuario.email,
        "rol": usuario.get_rol_display(),  # Si rol es un número,  se convertira a texto
    })
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_procesadores_usuario(request):
    """ Devuelve solo los productos creados por el usuario autenticado """
    procesador = Procesador.objects.filter(usuario=request.user)  # Filtrar por usuario autenticado
    serializer = ProcesadorSerializer(procesador, many=True)
    return Response(serializer.data)
