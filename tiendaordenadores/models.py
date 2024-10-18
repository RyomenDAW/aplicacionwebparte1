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
# en todo, como primary key
#====================================================================================


#Choices el segundo valor es el que se muestra
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
    ("DDR3", "DDR3"),
    ("DDR4", "DDR4"),
    ("DDR5"),("DDR5"),
)

class Procesador (models.Model):
    id_procesador = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    nombre = models.TextField(max_length=100)
    familiaprocesador = models.TextField(max_length=6, choices=FAMILIA_PROCESADOR)
    potenciacalculo = models.CharField(max_length=30)
    nucleos = models.IntegerField(max_length=3)
    hilos = models.IntegerField(max_length=4)

class Grafica (models.Model):
    id_grafica = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    nombre = models.TextField(max_length=100)
    familiagrafica = models.TextField(max_length=6, choices=FAMILIA_GRAFICA)
    potenciacalculo = models.CharField(max_length=30)
    memoriavram = models.CharField(max_length=10)
    fecha_salida = models.DateTimeField(default=timezone.now)
    trazadorayos = models.BooleanField(default=False)

class FuenteAlimentacion(models.Model):
    id_fuente = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    vatios = models.TextField(max_length=4)
    amperaje = models.FloatField(max_length=20)
    fuentealimentacion = models.TextField(max_length=100)
    calidadfuente = models.TextField(max_length=20, choices=SELLO_CALIDAD_FUENTE)

class PlacaBase(models.Model):
    id_placabase = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    nombre = models.TextField(max_length=100)
    familiaplacabase = models.TextField(max_length=10, choices=FAMILIA_GRAFICA)
    vrm_placa = models.FloatField(max_length=10)

class Monitor (models.Model):
    id_monitor = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    hz = models.TextField(max_length=4)
    calidad_respuesta = models.DecimalField(max_length=10) #Milisegundos puede ser un valor real
    curvo = models.BooleanField(default=False)

class Ram (models.Model):
      id_ram = models.AutoField(primary_key=True)
      fecha_fabricacion = models.DateField(default=timezone.now)
      mhz = models.CharField(max_length=10)
      familiaram = models.TextField(choices=FAMILIA_RAM)
      rgb = models.BooleanField(default = True)
      
    
# placabase
# monitor
# ram
# discodurohdd
# discodurossd
# discoduronvme
# disipador

# (Al menos una de ella debe tener una tabla intermedia con atributos extras)
# Cada modelo debe tener al menos 4 campos.  Y debe existir en total 10 atributos 
# de distinto tipo.No son válidos los atributos de relaciones.

