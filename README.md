# aplicacionwebparte1
Aplicación Web Parte I -Inicio y Modelos   (Para entregar el 20 de octubre)



===========================================================================================================================================================================================================

Primero las relaciones:

![ModeloEntidadRelacion_20OCTUBRE](https://github.com/user-attachments/assets/40253660-ce89-4d58-b0be-31871282047c)


===========================================================================================================================================================================================================

1. Relación OneToOne: Procesador - PlacaBase
Un procesador puede estar asociado a una única placa base, y viceversa. Esto significa que cada modelo de procesador está diseñado para funcionar con una placa base específica. Por ejemplo, si un procesador está instalado en una placa base, no se puede usar otro procesador en la misma placa base.

 

2. Relación OneToOne: Grafica - PlacaBase
Al igual que en la relación anterior, cada tarjeta gráfica se vincula a una sola placa base. Esto implica que la tarjeta gráfica se debe instalar en una placa base compatible. No puede haber más de una tarjeta gráfica en la misma placa base.

 

3. Relación OneToMany: PlacaBase - DiscoDuroHdd
Una placa base puede soportar múltiples discos duros HDD. Esto permite que un sistema tenga varias unidades de almacenamiento, aumentando la capacidad total y ofreciendo opciones para configuraciones RAID, por ejemplo.

 

4. Relación OneToMany: PlacaBase - Monitor
Una placa base puede gestionar varios monitores. Esto es importante para usuarios que requieren múltiples pantallas, como en el caso de configuraciones de trabajo con diseño gráfico UX.

 

5. Relación OneToMany: PlacaBase - Ram
Una placa base puede tener múltiples módulos de RAM instalados. Esto permite aumentar la memoria disponible del sistema, mejorando el rendimiento general, especialmente en tareas que requieren muchos recursos.

 

6. Relación ManyToMany: Grafica - Procesador
Un procesador puede funcionar con varias tarjetas gráficas y una tarjeta gráfica puede ser utilizada con múltiples procesadores. Este vínculo es crucial en configuraciones de alto rendimiento y gaming, donde diferentes combinaciones pueden ofrecer el mejor rendimiento. El atributo adicional cuellodebotella se usa para identificar si hay limitaciones en el rendimiento debido a la combinación de estos componentes.

 

7. Relación ManyToMany: Monitor - Grafica
Varios monitores pueden conectarse a una o varias tarjetas gráficas. Esto es útil para configuraciones que requieren múltiples pantallas, donde una tarjeta gráfica puede gestionar varias salidas de video simultáneamente.

 

8. Relación ManyToMany: PlacaBase - Disipador
Cada placa base puede estar asociada con múltiples modelos de disipadores. Esto permite a los usuarios elegir entre diferentes opciones de refrigeración para mantener el sistema a temperaturas adecuadas. Un disipador específico puede ser compatible con múltiples placas base, lo que ofrece flexibilidad en el diseño del sistema. 

 

9. Relación ManyToMany: Grafica - Monitor (no definido en tu modelo)
Una o mas tarjeta gráfica (SLI --> NVLINK) puede estar conectada a múltiples monitores, lo que es esencial para experiencias de usuario avanzadas. Este vínculo permite que un único sistema de gráficos gestione varios monitores.

===========================================================================================================================================================================================================

¿Cuales son los choices?

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
    ("DDR5","Formato DDR5"),
)

Para la familia de procesador solo tenemos Ryzen e Intel, sencillo.

Para las tarjetas graficas tendremos AMD, Nvidia e Intel, considero esta ultima ya que por ejemplo sacaron la grafica 'Iris' que da un rendimiento aceptable.

El sello de la calidad de la fuente empieza en 80Bronce como el sello mas 'malo' y luego va aumentando de calidad, esto permite que se aproveche mejor la eficiencia energetica de la fuente de alimentacion, sea mas resistente a picos de tension, tenga mas tiempo de vida util, etc.

La familia de la RAM consiste en el 'tipo' de RAM que permiten los slots de nuestra placa base, DDR3 siendo el mas antiguo, DDR4 el mas utilizado, y DDR5 el de mas calidad y caro.

Veo necesario explicar el atributo socket 

    socket = models.TextField(max_length=20, choices=FAMILIA_PROCESADOR)

Eso pasa debido a que cada socket de la placa base, solo admitira cierto tipos de procesadores, no es necesario crear un choices de sockets ya que solo admite procesadores de ADM o Intel, si es verdad que luego en la vida real existe LG1150, LGA1551, y AMD4, AMD5 (entre otros vaya), pero despues de todo la gran diferencia recae en que uno no tiene pines y otro si, lo cual hace imposible insertar un Intel dentro de uno de AMD4 (PGA)

Entonces, ya reutilizamos el choices de procesador porque, no hace falta crear uno nuevo, especificamente para el atributo de socket.

===========================================================================================================================================================================================================

ATRIBUTOS:

RGB es si contiene luces LED que sean agradables a la vista, lo pongo primero ya que no le veo mucho sentido a ponerlo 5 veces ya que lo he reutilizado
class Monitor (models.Model):
    id_monitor = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    hz = models.TextField(max_length=4)         #### Significa herzios, cuantos hz significan la fluidez de la imagen, formatos suelen ser 60 --> 75 --> 120 --> 144 --> 165 --> 180 --> 240 --> 360
    
    calidad_respuesta = models.DecimalField(max_digits=10, decimal_places=5)  # 5 decimales, el valor real de ms puede ser 1, monitores competetivos sobre todo
    curvo = models.BooleanField(default=False)
    pantallafiltroplasma = models.BooleanField(default=False)

    
class Ram (models.Model):
    id_ram = models.AutoField(primary_key=True)
    fecha_fabricacion = models.DateField(default=timezone.now)
    mhz = models.CharField(max_length=10)       #Miliherzios, velocidad de comunicacion con el bus de la RAM
    familiaram = models.TextField(choices=FAMILIA_RAM)
    rgb = models.BooleanField(default = True)
    factormemoria = models.IntegerField()
      
class DiscoDuroHdd(models.Model):
    id_hdd = models.AutoField(primary_key=True)
    rpm = models.TextField(max_length=20)      #Revoluciones por minuto, a mas, los platos giraran mas rapido y por ende mas velocidad de respuesta
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
    socket = models.TextField(max_length=20, choices=FAMILIA_PROCESADOR)                   # DONDE PONEMOS EL PROCESADOR, COMPARTE CHOICES.
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


===========================================================================================================================================================================================================

Hasta aqui todo.
