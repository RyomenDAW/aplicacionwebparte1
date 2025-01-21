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