from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *


@api_view(['GET'])
def procesador_list(request):

    procesadores = Procesador.objects.all()
    serializer = ProcesadorSerializer(procesadores, many=True)
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