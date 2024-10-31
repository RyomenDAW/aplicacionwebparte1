# Crea una URL que muestre una lista de todos los proyectos 
# de la aplicación con sus datos correspondientes.

from django.db.models import Q, Count, Avg  # Para filtros OR, agregaciones, y operaciones con modelos

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
    Disipador
)


# def lista_proyectos(request):
#     context = {
#         'procesadores': Procesador.objects.all(),
#         'graficas': Grafica.objects.all(),
#         'fuentes_alimentacion': FuenteAlimentacion.objects.all(),
#         'placas_base': PlacaBase.objects.all(),
#         'monitores': Monitor.objects.all(),
#         'rams': Ram.objects.all(),
#         'discos_hdd': DiscoDuroHdd.objects.all(),
#         'discos_ssd': DiscoDuroSsd.objects.all(),
#         'discos_nvme': DiscoDuroNvme.objects.all(),
#         'disipadores': Disipador.objects.all(),
#     }
#     return render(request, 'proyectos/lista_proyectos.html', context)

def inicio(request):
    return render(request, 'home/index.html')

def lista_procesadores(request):
    procesadores = Procesador.objects.all()
    return render (request, 'procesadores/lista_procesadores.html', {'procesadores': procesadores})

def lista_procesadores_segunhilos(request, numero_hilos):
    procesadores = Procesador.objects.all().filter(hilos = numero_hilos)
    return render (request, 'procesadores/lista_procesadores_segunhilos.html', {'procesadores': procesadores})

def lista_procesadores_segunfamilia(request, nombre_familia):
    #Aqui es un choices realmente, pero funcionaria de todas maneras ya que el campo es de tipo text (String)
    procesadores = Procesador.objects.all().filter(familiaprocesador = nombre_familia)
    return render (request, 'procesadores/lista_procesadores_segunfamilia.html', {'procesadores': procesadores})


def lista_graficas_segunfamilia_y_vram(request, nombre_familia, cantidad_vram):
    graficas = Grafica.objects.filter(familiagrafica = nombre_familia, memoriavram = cantidad_vram ).all()
    return render (request, 'graficas/lista_graficas_segunfamilia_y_vram.html', {'graficas': graficas})