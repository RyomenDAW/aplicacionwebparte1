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