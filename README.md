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
# Esto significa que la combinación de grafica y procesador debe ser única, evitando así que se creen registros 
# duplicados para la misma tarjeta gráfica y procesador en la relación GraficaProcesador.
# Esto asegura la integridad de los datos  y mejora la consistencia en las relaciones entre modelos.

  
# Relación ManyToMany: Grafica - Procesador                                   

Un procesador o varios, pueden dar soporte funcional a uno o mas graficas
                                                                            
Esto se llama SLI, aunque no se usa mucho hoy en dia, Nvlink es ejemplo, la placa
base tiene que ser tambien de muy alta calidad, añado atributo cuellodebotella a la tabla intermedia



class GraficaProcesador(models.Model):
    grafica = models.ForeignKey(Grafica, on_delete=models.CASCADE)
    procesador = models.ForeignKey(Procesador, on_delete=models.CASCADE)
    cuellodebotella = models.BooleanField(default=False)  # Atributo extra

    class Meta:
        unique_together = ('grafica', 'procesador')  # Evitar duplicados

# Relación ManyToMany: Monitor - Grafica              

Varios monitores pueden estar conectados a 1 o mas graficas tecnicamente



class MonitorGrafica(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    grafica = models.ForeignKey(Grafica, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('monitor', 'grafica')  # Evitar duplicados

# Relación ManyToMany: PlacaBase - Disipador          
Una placa base de muy alta calidad puede tener uno o mas disipadores



class PlacaBaseDisipador(models.Model): 
    placabase = models.ForeignKey(PlacaBase, on_delete=models.CASCADE)
    disipador = models.ForeignKey(Disipador, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('placabase', 'disipador')  # Evitar duplicados


===========================================================================================================================================================================================================

Hasta aqui todo PARTE 1.



Resurgimos de las cenizas como Soul of Cinder y explicamos brevemente la parte 2, pero es basicamente lo mismo que el views.py comentado.


===========================================================================================================================================================================================================

PARTE 2:

## Resumen de Vistas y Comentarios

### 1. Inicio:
**Función**: `inicio`  
**Descripción**: Esta es la página index, donde irán todas las URLs, en total 10.  

```python
def inicio(request):
    return render(request, 'home/index.html')
```

### 2. Lista de Procesadores:
**Función**: `lista_procesadores`  
**Descripción**: Esta vista devolverá todos los procesadores con sus características (atributos). También incluirá dentro del HTML el atributo de la placa base que va asociada al procesador.  

```python
def lista_procesadores(request):
    procesadores = Procesador.objects.all()
    return render(request, 'procesadores/lista_procesadores.html', {'procesadores': procesadores})
```

### 3. Filtrar por Hilos:
**Función**: `lista_procesadores_segunhilos`  
**Descripción**: Esta vista devolverá todos los procesadores que tengan el número de hilos exacto que se le pasa como parámetro, es un integer, puede ser negativo el valor. También incluirá el atributo de la placa base asociada al procesador.  

```python
def lista_procesadores_segunhilos(request, numero_hilos):
    procesadores = Procesador.objects.filter(hilos=numero_hilos).all()
    return render(request, 'procesadores/lista_procesadores_segunhilos.html', {'procesadores': procesadores})
```

### 4. Filtrar por Familia:
**Función**: `lista_procesadores_segunfamilia`  
**Descripción**: Esta vista devolverá todos los procesadores que pertenezcan a la familia que se le indique como parámetro. También incluirá el atributo de la placa base asociada al procesador.  

```python
def lista_procesadores_segunfamilia(request, nombre_familia):
    procesadores = Procesador.objects.filter(familiaprocesador=nombre_familia).all()
    return render(request, 'procesadores/lista_procesadores_segunfamilia.html', {'procesadores': procesadores})
```

### 5. Filtrar Gráficas por Familia y VRAM:
**Función**: `lista_graficas_segunfamilia_y_vram`  
**Descripción**: Esta vista devolverá la lista de gráficas que cumplan ambos parámetros, el atributo de su familia y la cantidad de VRAM asignada. También incluirá el atributo de la placa base que va asociada a la gráfica.  

```python
def lista_graficas_segunfamilia_y_vram(request, nombre_familia, cantidad_vram):
    graficas = Grafica.objects.filter(familiagrafica=nombre_familia, memoriavram=cantidad_vram).all()
    return render(request, 'graficas/lista_graficas_segunfamilia_y_vram.html', {'graficas': graficas})
```

### 6. Promedio de Núcleos:
**Función**: `promedio_nucleos`  
**Descripción**:  
```python
# SE UTILIZA LA PARTE DE AGGREGATE QUE SE TENIA QUE INVESTIGAR, SE UTILIZA PARA PODER HACER AGREGACIONES SIN CARGAR EN LA MEMORIA TODOS LOS VALORES Y DEVOLVER EL
# RESULTADO DE LAS OPERACIONES REALIZADAS CON ESOS VALORES, AHORRANDO RECURSO Y OPTIMIZANDO.

# La vista nos obtiene la media (avg) del campo nucleos de todos los objetos en el modelo Procesador, tener en cuenta que es negativo algunos valores.
def promedio_nucleos(request):
    promedio_nucleos = Procesador.objects.aggregate(promedio_nucleos=Avg('nucleos'))
    return render(request, 'procesadores/promedio_nucleos.html', {'promedio_nucleos': promedio_nucleos})
```

### 7. Filtrar Procesadores (OR y AND):
**Función**: `filtrar8nucleos_OR_intel_AND_12hilos`  
**Descripción**: Esta vista obtendrá procesadores que tengan más de 8 núcleos o que pertenezcan a la familia 'Intel', pero que además tengan más de 12 hilos.  

```python
def filtrar8nucleos_OR_intel_AND_12hilos(request):
    procesadores = Procesador.objects.filter((Q(nucleos__gt=8) | Q(familiaprocesador='Intel')) & Q(hilos__gt=12)).all()
    return render(request, 'procesadores/filtrar8nucleos_OR_intel_AND_12hilos.html', {'procesadores': procesadores})
```

### 8. Filtrar Gráficas por Fecha:
**Función**: `filtrargraficas_segunfecha`  
**Descripción**: Esta vista devolverá todas las gráficas ordenadas de forma descendente por fecha.  

```python
def filtrargraficas_segunfecha(request):
    graficas = Grafica.objects.order_by('-fecha_salida')
    return render(request, 'graficas/filtrargraficas_segunfecha.html', {'graficas': graficas})
```

### 9. Procesadores Según Gráfica:
**Función**: `procesadores_segun_grafica`  
**Descripción**: Esta vista obtiene una gráfica específica según su ID y devuelve los procesadores asociados a esa gráfica. Si no existe la gráfica, generará un error.  

```python
def procesadores_segun_grafica(request, grafica_id):
    grafica_especifica = Grafica.objects.get(id_grafica=grafica_id)
    procesadores_conectados = Procesador.objects.filter(procesadores_reverse=grafica_especifica)
    return render(request, 'reverse/procesadores_segun_grafica.html', {
        'grafica': grafica_especifica,
        'procesadores': procesadores_conectados,
    })
```

### 10. Primeros 5 SSD:
**Función**: `primeros_5_ssd`  
**Descripción**: Esta vista obtiene las primeras 5 instancias de `DiscoDuroSsd` y las muestra en la plantilla. No se aplica ningún filtro especial, solo se limita a 5 resultados.  

```python
def primeros_5_ssd(request):
    ssds = DiscoDuroSsd.objects.all()[:5]
    return render(request, 'ssd/primeros_5_ssd.html', {
        'ssds': ssds,
    })
```

### 11. Gráficas Sin Cuello de Botella:
**Función**: `graficas_sin_cuello_de_botella`  
**Descripción**: Esta vista devolverá todas las gráficas sin cuello de botella, es decir, aquellas gráficas que tienen en la relación `ManyToMany` el atributo `cuellodebotella` en 0 (False). También incluirá el procesador asociado.  

```python
def graficas_sin_cuello_de_botella(request):
    graficas_sin_cuello = GraficaProcesador.objects.filter(cuellodebotella=False)  # O None si lo defines como Nullable
    return render(request, 'intermedia/graficas_sin_cuello_de_botella.html', {
        'graficas_sin_cuello': graficas_sin_cuello,
    })
```

### 12. Lista de Gráficas:
**Función**: `lista_graficas`  
**Descripción**: Esta vista devolverá todas las gráficas con sus características (atributos). También incluirá dentro del HTML el atributo de la placa base que va asociada a la tarjeta gráfica.  

```python
def lista_graficas(request):
    graficas = Grafica.objects.all()
    return render(request, 'graficas/lista_graficas.html', {'graficas': graficas})
```

---

===========================================================================================================================================================================================================

TEMPLATES TAGS UTILIZADOS:


1: IF-ELSE 

{% comment %} AQUI VA EL PRIMER TEMPLATE TAG, UN IF ELSE {% endcomment %}

{% extends "../estructura/templatefinal.html" %}
{% block cabecera %}
{% endblock %}

{% block contenido %}

<h1>Promedio de Núcleos</h1>

{% if promedio_nucleos.promedio_nucleos %}
    <p>El promedio de núcleos en los procesadores es: {{ promedio_nucleos.promedio_nucleos }}</p>
{% else %}
    <p>No se pudo calcular el promedio de núcleos en este momento.</p>
{% endif %}

{% endblock %}

En promedio_nucleos.html


2: FOR-EMPTY


{% comment %} ESTE ES EL SEGUNDO TEMPLATE TAG, FOR EMPTY {% endcomment %}

{% extends "../estructura/templatefinal.html" %}
{% block cabecera %}
{% endblock %}

{% block contenido %}
    {% for ssd in ssds %}
        {% include "../estructura/ssd_for.html" %}
    {% empty %}
        <p>No se encontraron SSDs disponibles.</p>
    {% endfor %}
{% endblock %}

{% comment %} FIN DEL SEGUNDO TEMPLATE TAG {% endcomment %}

En primeros_5_ssd.html

3: INCLUDE

{% comment %} TERCER TEMPLATE TAG, INCLUDE {% endcomment %}

{% include './footer.html' %}

{% comment %} FIN DEL TERCER TEMPLATE TAG {% endcomment %}

En estructura/templatefinal.html

4: BLOCK Y ENDBLOCK

{% comment %} CUARTO TEMPLATE TAG: BLOCK Y ENDBLOCK {% endcomment %}

{% block contenido %}
{% endblock %}

{% comment %} FIN DEL CUARTO TEMPLATE TAG {% endcomment %}

En estructura/templatefinal.html

5: FOR & ENDFOR

{% comment %} QUINTO TEMPLATE TAG, FOR, ENDFOR {% endcomment %}

    {% for grafica in graficas %}
    {% include "../estructura/graficas_for.html" %}

    {% endfor %}
{% comment %} FIN DEL QUINTO TEMPLATE TAG {% endcomment %}

En estructura/graficas_for.html


===========================================================================================================================================================================================================

OPERADORES USADOS:

{% comment %} PRIMER OPERADOR, IGUALDAD == {% endcomment %}  en listaprocesadores_segunfamilia.html
{% comment %} SEGUNDO Y TERCER OPERADOR, ARITMÉTICOS > Y <= {% endcomment %} en promedio_nucleos.html
{% comment %} CUARTO OPERADOR, `if not` {% endcomment %} en primeros_5_ssd.httml
{% comment %} QUINTO OPERADOR, ES UN `AND` {% endcomment %} en lista_procesadores.html

===========================================================================================================================================================================================================

TEMPLATE FILTERS USADOS:
---------------------------------------------------------------------------------------------------

Todos en procesadores_for.html

1. upper
Convierte todo el texto a mayúsculas.           

2. slice
Extrae una porción de una cadena de texto o lista. Se puede utilizar para tomar un número específico de caracteres o elementos.

3. default_if_none
Proporciona un valor por defecto solo si el valor original es None.
---------------------------------------------------------------------------------------------------

Todos en graficas_for.html
4. lower
Convierte todo el texto a minúsculas.

5. truncatewords
Trunca el texto a un número específico de palabras. Es útil cuando se necesita limitar la longitud del texto mostrado.

6. date
Formatea un objeto datetime en una cadena de texto con un formato específico. Permite mostrar fechas de forma legible.

7. length
Devuelve la longitud de una lista, cadena o iterable. Es útil para mostrar el tamaño de una colección o cadena.

---------------------------------------------------------------------------------------------------

Todos en graficas_sin_cuello.html

8. title
Convierte la primera letra de cada palabra en mayúscula. Ideal para títulos o nombres de campos.

9. default
Proporciona un valor por defecto si la variable es vacía o None. Se usa para asegurar que siempre haya un valor visible en caso de que no exista uno.

10. add
Suma un valor al original. Puede utilizarse para realizar cálculos dentro de las plantillas.

---------------------------------------------------------------------------------------------------

Cómo usar los filtros
Estos filtros pueden ser aplicados a cualquier variable dentro de las plantillas de Django para modificar su formato, mostrar valores predeterminados, o realizar operaciones como sumar valores. Solo es necesario usar el operador de filtro |, seguido del nombre del filtro y sus parámetros si los hubiera (como en el caso de truncatewords:10 o date:"d M Y").







WIDGETS:

PROCESADOR:
Para el ProcesadorForm, utilicé widgets como TextInput para el nombre del procesador, URLInput para la URL de compra, y Select para las familias de procesadores.


En el BusquedaAvanzadaProcesador, utilicé TextInput para la búsqueda de nombre, NumberInput para los valores numéricos de núcleos y hilos, y CheckboxSelectMultiple para seleccionar las familias de procesadores.



GRAFICA:
En este formulario, vamos a usar widgets como NumberInput (que ya hemos utilizado), Select y TextInput para los campos de texto, y también un CheckboxInput para la opción de trazado de rayos.


Usaremos TextInput para nombreBusqueda, NumberInput para los campos numéricos de potencia de cálculo y memoria VRAM, y CheckboxSelectMultiple para las familias de gráficas.

Hasta ahora llevamos estos:

Resumen de Widgets Usados:
TextInput: Para nombre y nombreBusqueda en ambos formularios.
URLInput: Para urlcompra en GraficaForm.
Select: Para la familia de la gráfica en GraficaForm.
NumberInput: Para campos numéricos como potenciacalculo y memoriavram en ambos formularios.
CheckboxInput: Para el campo de trazado de rayos en GraficaForm.
CheckboxSelectMultiple: Para las familias de gráfica en BusquedaAvanzadaGrafica.


Y añadimos uno mas para monitor:

El nuevo widget que hemos añadido en el formulario MonitorForm y en el formulario BusquedaAvanzadaMonitor es el RadioSelect. Este widget se utiliza para los campos booleanos curvo y pantallafiltroplasma, donde el usuario puede seleccionar entre las opciones "Sí" o "No".

No hace falta que te diga donde mas he utilizado widgets, ya que simplemente se iran repitiendo, puedes verlo aun asi en el programa.

Aun asi son estos:

Widgets Usados:
1. forms.TextInput
Propósito: Campo de texto simple.
Ejemplos:
Usado en campos como mhz en RamForm, capacidad en HDDForm, rpm en HDDForm.
Widget con attrs={'placeholder': 'Ej. 7200'} y similar para otros campos.
2. forms.NumberInput
Propósito: Campo de entrada numérica.
Ejemplos:
Usado en campos como tiempomediofallos en HDDForm para aceptar números con decimales (step='0.01').
Usado en campos como pulgadas en HDDForm para valores numéricos con límites (min='1', max='10').
3. forms.DateInput
Propósito: Campo de entrada para fechas.
Ejemplos:
Usado en el campo fecha_fabricacion en RamForm, donde se establece el tipo de entrada a date.
4. forms.CheckboxInput
Propósito: Campo de entrada tipo checkbox (booleano).
Ejemplos:
Usado en el campo rgb en RamForm y en HDDForm para indicar si tiene o no luces RGB.
5. forms.ClearableFileInput
Propósito: Campo para subir archivos (como imágenes).
Ejemplos:
Usado en el campo imagen en ProcesadorForm para cargar imágenes (usado con multiple=True para permitir múltiples archivos si es necesario).
6. forms.URLInput
Propósito: Campo de entrada para URLs.
Ejemplos:
Usado en urlcompra en FuenteForm, para especificar la URL de compra de un procesador o fuente.
7. forms.Select
Propósito: Campo de selección desplegable.
Ejemplos:
Usado en campos como calidadfuente en FuenteForm, familiaram en RamForm, y en BuscadorAvanzado para seleccionar una opción entre varias.

Todas las validaciones estan comentadas en el forms debidamente, ya que estan ordenadas con comentarios 

===========================================================================================================================================================================================================

MODIFACIONES PARTE V: 14 DE ENERO --> ENTREGA 20 ENERO

En nuestra aplicación debemos incluir al menos dos tipos de usuarios claramente diferenciados(No cuenta el usuario administrador) (1 puntos)

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    TECNICOINFORMATICO = 3
    VENDEDOR = 4
    
    ROLES=(
        (ADMINISTRADOR, 'administrador'),
        (CLIENTE, 'cliente'),
        (TECNICOINFORMATICO, 'tecnicoinformatico'),
        (VENDEDOR, 'vendedor'),
    )
    
    rol = models.PositiveSmallIntegerField(
        choices=ROLES, default=1
    )

Funcionalidad de Cliente --> No puede crear nada, ni borrar, ni editar, si puede buscar.

Funcionalidad de Tecnico Informatico --> No puede crear nada, si puede editar, si puede buscar.

Funcionalidad de Vendedor --> Si puede crear, si puede borrar, si puede editar, si puede buscar. (No es asi supersuser, es decir, administrador)

Se entiende vendedor aquellas marcas como ASUS, ROG, MSI, entre otras, no a un vendedor físico como puede ser Mark Johnson, nos referimos a la figura judicial que representa.

===========================================================================================================================================================================================================

En cada vista controlarse los permisos y si el usuario esta logueado o no (1 punto)

En todas las vistas se requiere el comando del crud necesario para esa vista en especifico, lo he dividido muy bien y esta comentado
de manera que se vea claro.


# VISTA PARA ELIMINAR UN DISCO DURO HDD
# REQUIERE LOGIN Y PERMISO PARA ELIMINAR HDD
@login_required
@permission_required('discoshdd.delete_discodurohdd', raise_exception=True)
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


Por ejemplo eso va en esta vista, ya que se requiere el permiso delete_discodurohdd.


¿Por qué se utiliza raise_exception=True?

Cuando se usa @permission_required en una vista, el decorador revisa si el usuario tiene el permiso específico (como discoshdd.delete_discodurohdd en tu caso). Si el usuario tiene ese permiso, la vista se ejecuta normalmente. Si el usuario no tiene ese permiso, el decorador puede hacer varias cosas, dependiendo de la configuración:

Si raise_exception=False (valor por defecto): El decorador redirige al usuario a una página de inicio de sesión si no está autenticado. Si está autenticado pero no tiene el permiso requerido, se le redirige a una página de error o a una página configurada para manejar este tipo de situación, en nuestro caso.

Si raise_exception=True: En lugar de redirigir al usuario a una página de error o inicio de sesión, se lanza una excepción (PermissionDenied). Esta opción es más explícita en cuanto a la seguridad, ya que detiene la ejecución de la vista inmediatamente y proporciona una respuesta clara de que el usuario no tiene permisos para acceder a esa acción, la pagina de error 403.

La ventaja de usar raise_exception=True es que te permite manejar mejor los casos de acceso no autorizado y tener un flujo de control más claro sobre cómo se debe manejar la seguridad de la vista, por eso lo he elegido, aunque esta a tu disposicion.

===========================================================================================================================================================================================================

En cada template de vista y formulario controlarse los permisos y si el usuario esta logueado o no (1 punto)

Los permisos estan asignados de manera que:

Todos los usuarios pueden ver las listas (Incluye cliente) y se requiere login mediante un if

{% if request.user.is_authenticated %}


Cliente no tiene acceso al CRUD.
Solo vendedor puede hacer en el CRUD: Crear y Eliminar
Solo tecnicoinformatico puede hacer en el CRUD: Editar y Buscar (Avanzado)

Solo administrador puede hacer en el CRUD: Crear, Buscar (Avanzado), Editar y Eliminar

Todas las condiciones del crud se hacen tambien mediante if

{% if request.session.rol == 'Administrador' or request.session.rol == 'Vendedor' %}


===========================================================================================================================================================================================================


Incluir al menos 4 variables que se guarden en la sesión y que aparezcan siempre en la cabacera de la página. Y se eliminen cuando se desloguea el usuario. (1 punto)


Variables incluidas en la sesión
Se incluyen las siguientes variables en la sesión cuando el usuario está autenticado:

fecha_inicio: Fecha y hora de inicio de sesión.
usuario_nombre: Nombre completo del usuario.
usuario_first_name: Primer nombre del usuario.
rol: Rol del usuario basado en un campo específico (request.user.rol).
usuario_email: Correo electrónico del usuario.
Estas variables se almacenan en la sesión y estarán disponibles para ser mostradas en la cabecera de la página.

Se puede ver en la view de inicio, se incluyen en nav.html que forma parte de la estrucutra.


Para asegurar que las variables se eliminen al cerrar sesión, el método de cierre de sesión debe estar configurado para limpiar la sesión, en mi caso, en logout.

def logout_view(request):
    logout(request)  # Desloguear al usuario
    request.session.flush()  # Eliminar todas las variables de la sesión

    return redirect('login')  # Redirigir al login después de logout




===========================================================================================================================================================================================================


Debemos hacer un registro de los distintos tipos de usuario, salvo el administrador, con sus validaciones correspondiente, y controlar que dependiendo del tipo de usuario tendrá unos valores u otros (1 punto)

En vendedor, tenemos el valor marca

    marca = models.CharField(max_length=100, null=True, blank=True, db_column="marca_tiendaordenadores")

El valor solo aparece si se elige vendedor como rol, se guarda en la BBDD como una columna ya que es de models.py



===========================================================================================================================================================================================================

Debemos hacer un login y logout del usuario (1 punto)

LOGIN:

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
                tecnicoinformatico = TecnicoInformatico.objects.create(usuario=user)  # Asociar el usuario como técnico informático
                tecnicoinformatico.save()
            elif rol == Usuario.VENDEDOR:
                vendedor = Vendedor.objects.create(usuario=user)  # Asociar el usuario como vendedor
                vendedor.save()
                
            
            # Redirigir al usuario a la página principal despues del form, ya que no tiene sentido quedarse en el formulario

        
            login(request, user) #Aqui se hace con la propia variable, al registrase, se conectara de forma automatica
            
            
            if request.user.is_authenticated:
                print("Usuario autenticado:", request.user.username)
            else:
                print("Error: Usuario no autenticado")


            return redirect('index')


LOGOUT:

    def logout_view(request):
        logout(request)  # Desloguear al usuario
        request.session.flush()  # Eliminar todas las variables de la sesión

        return redirect('login')  # Redirigir al login después de logout

Las URLS son estas:

  path('registrar',views.registrar_usuario, name='registrar_usuario'),
  path('logout/', LogoutView.as_view(), name='logout'),  # Ruta para el logout

===========================================================================================================================================================================================================


Debe crearse una funcionalidad en algún formulario , que el contenido de algún select ManyToMany o ManyToOne varie dependiendo del usuario que está logueado. (1 punto)

En crear grafica, se puede asignar como tal a que procesador va enlazada esa grafica (manytoone)
        form = GraficaForm(user=request.user) #Se le pasa el usuario

Si es administrador, podra elegir a que procesador podra ir enlazado, si es vendedor, no podra, aparecera en gris. (Ya que es el unico
aparte del administrador que puede hacer la parte de crear)

Logeate con HajimeKashimo para verlo, te pongo en el classroom la password de el.



===========================================================================================================================================================================================================

En los formularios de crear debe incluirse siempre el usuario que crea dicho registro por la sesión del usuario. (1 punto)

Se hace por ejemplo asi en crear_procesador, 

class Procesador (models.Model):
    id_procesador = models.AutoField(primary_key=True)
    urlcompra = models.URLField(max_length=100)
    nombre = models.TextField(max_length=100)
    familiaprocesador = models.TextField(max_length=6, choices=FAMILIA_PROCESADOR)
    potenciacalculo = models.PositiveBigIntegerField()
    nucleos = models.PositiveSmallIntegerField()
    hilos = models.PositiveIntegerField(validators=[MinValueValidator(35000)])  # Este validator luego se suprime por el form y view xd
    imagen = models.ImageField(upload_to='procesadores/', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Aquí usamos CustomUser en lugar de User


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

    Esto sirve para en vez de ponerlo en el .html mas separado, se ponga en el form y ya, mas util.

            exclude = ['user']  # Excluimos el campo 'user' para que no aparezca en el formulario


===========================================================================================================================================================================================================

Debe crearse una funcionalidad en algún formulario de búsqueda , que el contenido se filtre por el suario que está logueado. (1 punto)

Dentro del formulario de busqueda ReadProcesador, solo saldran los procesadores relacionados del usuario logeado, sin importar el rol.


    # Inicializamos la consulta base para filtrar por el usuario autenticado
    procesadores = Procesador.objects.filter(user=request.user)  # Solo los procesadores del usuario logueado

Al inicio de la vista, antes de aplicar cualquier otro filtro, se aplica un filtro inicial para obtener solo los procesadores que pertenecen al usuario logueado: Procesador.objects.filter(user=request.user), es lo que pide el apartado literalmente.

Filtros adicionales:
Después, si se envían otros parámetros en el formulario (como nombre, nucleos, hilos, o familiaprocesador), esos se aplican sobre la consulta filtrada por usuario.

===========================================================================================================================================================================================================

Implementar funcionalidad de reinicio de contraseña.  Ten en cuenta que tu aplicación en local no permite el envó de email, pero hay una forma en Django para obtener dicho enlace de recuperación de contraseña. Investiga! (1 punto)

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Esto permite que cualquier correo de recuperación de contraseña se redirija a la consola de mi servidor local (terminal), lo cual es útil.


En urls creamos 4 vistas.


Aquí está lo que hace cada vista:

password_reset/: Vista donde el usuario ingresa su correo electrónico para recibir un enlace de restablecimiento de contraseña.

password_reset_done/: Mensaje de confirmación que aparece después de que el usuario envía su correo para el restablecimiento de contraseña.

reset/<uidb64>/<token>/: Página donde el usuario puede ingresar una nueva contraseña, accesible solo a través de un enlace seguro con un token válido.

reset/done/: Mensaje de éxito que aparece después de que el usuario ha restablecido su contraseña correctamente.


En tu plantilla de login (login.html),  incluyo un enlace para que los usuarios puedan acceder fácilmente a la página de recuperación de contraseña.

En la terminal sale un mensaje muy similar a este:

Ha recibido este correo electrónico porque ha solicitado restablecer la contraseña para su cuenta en 127.0.0.1:8000.

Por favor, vaya a la página siguiente y escoja una nueva contraseña.

http://127.0.0.1:8000/accounts/reset/MTEw/aquivaelenlacedeltoken/

Lo he quitado ya que no le veo sentido ponerlo en el readme.md por motivos de seguridad

Su nombre de usuario, en caso de que lo haya olvidado: Mahoraga

¡Gracias por usar nuestro sitio!

El equipo de 127.0.0.1:8000 (Mi preciosa pagina web)

===========================================================================================================================================================================================================