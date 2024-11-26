from django.conf import settings
from django.db import models
from django.utils import timezone

# Definir 10 modelos de mi página Web que cumpla los siguientes requisitos.
# Al menos 3 relaciones OneToOne, 3 relaciones ManytoOne, 3 relaciones ManyToMany


#====================================================================================

# Estos son mis 10 atributos de distinto tipo, se utilizaran en funcion.

# models.TextField -
# models.CharField -
# models.IntegerField -
# models.FloatField -
# models.BooleanField -
# models.DateTimeField -
# models.DateField -
# models.URLField -
# models.DecimalField -
# models.EmailField -

#El campo models.AutoField no lo contare, aun asi si lo menciono, ya que lo pondre
# en todo, como primary key, SIEMPRE SERA ID_nombre.

#Date no me ha dado bugs pero verifica en la BBDD si quieres vaya
#====================================================================================


#Choices el segundo valor es el que se muestra es humano, pero vaya, que es lo mismo.
FAMILIA_PROCESADOR = (
    ("Ryzen", "Ryzen"),
    ("Intel", "Intel"),
)

FAMILIA_GRAFICA = (
    ("AMD", "AMD"),
    ("Nvidia", "NVIDIA"),
    ("Intel", "Intel")
)

SELLO_CALIDAD_FUENTE = (
    ("80Bronce", "80Bronce"),
    ("80Silver", "80Silver"),
    ("80Gold", "80Gold"),
    ("80Plat", "80Plat"),
    ("80Titanium", "80Titanium"),
)

FAMILIA_RAM = (
    ("DDR3", "Formato DDR3"),
    ("DDR4", "Formato DDR4"),
    ("DDR5","FOrmato DDR5"),
)

class Procesador (models.Model):
    id_procesador = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    nombre = models.TextField(max_length=100)
    familiaprocesador = models.TextField(max_length=6, choices=FAMILIA_PROCESADOR)
    potenciacalculo = models.CharField(max_length=30)
    nucleos = models.IntegerField()
    hilos = models.IntegerField()

    
    # Relación OneToOne con PlacaBase
    placabase = models.OneToOneField('PlacaBase', on_delete=models.CASCADE, null=True, blank=True)


class Grafica (models.Model):
    id_grafica = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    nombre = models.TextField(max_length=100)
    familiagrafica = models.TextField(max_length=6, choices=FAMILIA_GRAFICA)
    potenciacalculo = models.CharField(max_length=30)
    memoriavram = models.CharField(max_length=10)
    fecha_salida = models.DateTimeField(default=timezone.now)
    trazadorayos = models.BooleanField(default=False)

   #AÑADIDO EN ESTA TAREA PARA QUE FUNCIONE LA URL REVERSA
    grafica_procesadores = models.ForeignKey(Procesador, related_name='procesadores_reverse', on_delete=models.CASCADE)


# Relación OneToOne con PlacaBase
placabase = models.OneToOneField('PlacaBase', on_delete=models.CASCADE, null=True, blank=True)
    
    
class FuenteAlimentacion(models.Model):
    id_fuente = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    vatios = models.TextField(max_length=4)
    amperaje = models.FloatField(max_length=20)
    conectoresdisponibles = models.TextField(max_length=100)
    calidadfuente = models.TextField(max_length=20, choices=SELLO_CALIDAD_FUENTE)

class PlacaBase(models.Model):
    id_placabase = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    nombre = models.TextField(max_length=100)
    familiaplacabase = models.TextField(max_length=10, choices=FAMILIA_PROCESADOR)
    vrm_placa = models.FloatField(max_length=10)
    rgb = models.BooleanField(default=False)
    
    # Relación OneToMany con DiscoDuroHdd
    hdds = models.ManyToManyField('DiscoDuroHdd', related_name='placabas_hdds')

    # Relación OneToMany con Monitor
    monitores = models.ManyToManyField('Monitor', related_name='placabas_monitores')

    # Relación OneToMany con Ram
    rams = models.ManyToManyField('Ram', related_name='placabas_rams')
    

class Monitor (models.Model):
    id_monitor = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    hz = models.TextField(max_length=4)
    calidad_respuesta = models.DecimalField(max_digits=10, decimal_places=5)  # 5 decimales, el valor real de ms puede ser 1, monitores competetivos sobre todo
    curvo = models.BooleanField(default=False)
    pantallafiltroplasma = models.BooleanField(default=False)
class Ram (models.Model):
    id_ram = models.AutoField(primary_key=True)
    fecha_fabricacion = models.DateField(default=timezone.now)
    mhz = models.CharField(max_length=10)
    familiaram = models.TextField(choices=FAMILIA_RAM)
    rgb = models.BooleanField(default = True)
    factormemoria = models.IntegerField()
      
class DiscoDuroHdd(models.Model):
    id_hdd = models.AutoField(primary_key=True)
    rpm = models.TextField(max_length=20)
    capacidad = models.CharField(max_length=20)
    peso = models.CharField(max_length=10)
    tiempomediofallos = models.DecimalField(max_digits=10, decimal_places=2)  # HASTA 2 DECIMALES
    pulgadas = models.IntegerField()

class DiscoDuroSsd(models.Model):
    id_ssd = models.AutoField(primary_key=True)
    amperaje = models.TextField(max_length=20)
    capacidad = models.CharField(max_length=20)
    peso = models.CharField(max_length=10)
    tiempomediofallos = models.DecimalField(max_digits=10, decimal_places=2)  # HASTA 2 DECIMALES

class DiscoDuroNvme(models.Model):
    id_nvme = models.AutoField(primary_key=True)
    amperaje = models.TextField(max_length=20)
    capacidad = models.CharField(max_length=20)
    peso = models.CharField(max_length=10)
    tiempomediofallos = models.DecimalField(max_digits=10, decimal_places=2)  # HASTA 2 DECIMALES

class Disipador(models.Model):
    id_disipador = models.AutoField(primary_key=True)    
    vidautil = models.CharField(max_length=20)
    socket = models.TextField(max_length=20, choices=FAMILIA_PROCESADOR)
    voltaje = models.CharField(max_length=10)
    dimensiones = models.CharField(max_length=10)
    fechacreacion = models.DateTimeField(default=timezone.now)
    
# Relación OneToOne con PlacaBase
placabase = models.OneToOneField('PlacaBase', on_delete=models.CASCADE, null=True, blank=True)


#EXPLICACION DEL META, YA QUE LO HE SACADO DE INTERNET, Y SE DEBE DE EXPLICAR:

# La clase Meta en un modelo de Django se utiliza para proporcionar opciones adicionales sobre el comportamiento del modelo. 
# En este caso, estamos utilizando el atributo unique_together para definir una restricción de unicidad en la tabla intermedia 
# que relaciona los modelos. 
# 
# Esto significa que la combinación de grafica y procesador debe ser única, evitando así que se creen registros 
# duplicados para la misma tarjeta gráfica y procesador en la relación GraficaProcesador.
# 
# Esto asegura la integridad de los datos  y mejora la consistencia en las relaciones entre modelos.

  
# Relación ManyToMany: Grafica - Procesador                                    //Un procesador o varios, pueden dar soporte funcional a uno o mas graficas
                                                                               #Esto se llama SLI, aunque no se usa mucho hoy en dia, Nvlink es ejemplo, la placa
                                                                               #base tiene que ser tambien de muy alta calidad, añado atributo cuellodebotella a la tabla intermedia
class GraficaProcesador(models.Model):
    grafica = models.ForeignKey(Grafica, on_delete=models.CASCADE)
    procesador = models.ForeignKey(Procesador, on_delete=models.CASCADE)
    cuellodebotella = models.BooleanField(default=False)  # Atributo extra

    class Meta:
        unique_together = ('grafica', 'procesador')  # Evitar duplicados

# Relación ManyToMany: Monitor - Grafica               //Varios monitores pueden estar conectados a 1 o mas graficas tecnicamente
class MonitorGrafica(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    grafica = models.ForeignKey(Grafica, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('monitor', 'grafica')  # Evitar duplicados

# Relación ManyToMany: PlacaBase - Disipador          //Una placa base de muy alta calidad puede tener uno o mas disipadores
class PlacaBaseDisipador(models.Model): 
    placabase = models.ForeignKey(PlacaBase, on_delete=models.CASCADE)
    disipador = models.ForeignKey(Disipador, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('placabase', 'disipador')  # Evitar duplicados
    
    
    
# de distinto tipo.No son válidos los atributos de relaciones.

    # Relaciones ManyToMany
    # Grafica_Procesador

# Descripción: Esta relación representa una conexión entre la Tarjeta Gráfica (Grafica) y el Procesador (Procesador). Una tarjeta gráfica puede ser utilizada con varios procesadores, dependiendo de la compatibilidad del socket y otros factores. Al mismo tiempo, un procesador puede funcionar con múltiples tarjetas gráficas.
# Atributo extra: cuellodebotella (boolean, default=False) se utiliza para indicar si la combinación de este procesador y tarjeta gráfica específica presenta un cuello de botella. Un cuello de botella ocurre cuando un componente limita el rendimiento del sistema debido a su incapacidad para manejar la carga de trabajo, lo que significa que el rendimiento de la tarjeta gráfica podría verse afectado por las limitaciones del procesador.
# Monitor_Grafica

# Descripción: Esta relación muestra la conexión entre un Monitor y una Tarjeta Gráfica. Un monitor puede ser utilizado con múltiples tarjetas gráficas, y cada tarjeta gráfica puede soportar varios monitores. Esto permite a los usuarios elegir diferentes configuraciones de monitores según sus necesidades, como configuraciones de múltiples pantallas para tareas de diseño gráfico o gaming.
# Atributo extra: En este caso, no se mencionó un atributo extra, pero podrías considerar añadir algo como resolucion_soportada para especificar las resoluciones que puede manejar cada combinación de monitor y tarjeta gráfica.
# PlacaBase_Disipador

# Descripción: Esta relación representa la conexión entre una Placa Base y un Disipador. Cada placa base puede ser compatible con diferentes modelos de disipadores, y un disipador específico puede ser utilizado en varias placas base. Esta flexibilidad es crucial para garantizar que el sistema se mantenga refrigerado, especialmente en configuraciones de alto rendimiento.
# Atributo extra: Al igual que en el caso anterior, puedes considerar agregar un atributo extra como tipo_refrigeracion (por ejemplo, aire o líquida) para detallar el tipo de refrigeración que proporciona el disipador.