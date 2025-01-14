from django import forms
from .models import Procesador, Grafica, Monitor, FuenteAlimentacion, Ram, DiscoDuroHdd
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from .models import *
#================================================================================================================================

class ProcesadorForm(forms.ModelForm):  # MODEL FORM
    class Meta:
        model = Procesador
        fields = ['nombre', 'urlcompra', 'familiaprocesador', 'potenciacalculo', 'nucleos', 'hilos', 'placabase', 'imagen']

        # Configuración opcional para personalizar etiquetas o mensajes de ayuda
        labels = {
            'nombre': 'Nombre del Procesador',
            'urlcompra': 'URL de compra',
            'familiaprocesador': 'Familia del Procesador',
            'potenciacalculo': 'Potencia de Cálculo',
            'nucleos': 'Número de Núcleos',
            'hilos': 'Número de Hilos',
            'placabase': 'Placa Base',
            'imagen': 'Imagen del Procesador',
        }
        help_texts = {
            'familiaprocesador': 'Selecciona la familia a la que pertenece el procesador, sea Intel o Ryzen',
            'urlcompra': 'Introduce una URL válida donde se pueda comprar este procesador.',
        }

        # Personalización de widgets
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),  # Campo de texto para el nombre
            'urlcompra': forms.URLInput(attrs={'class': 'form-control'}),  # Campo para la URL de compra
            'familiaprocesador': forms.Select(choices=[('Intel', 'Intel'), ('Ryzen', 'Ryzen')], attrs={'class': 'form-control'}),  # Dropdown para familia
            'nucleos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 1000000}),  # Campo numérico para núcleos
            'hilos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100000000}),  # Campo numérico para hilos
            'imagen': forms.ClearableFileInput(),  # Sin el atributo multiple
        }


        
class BusquedaAvanzadaProcesador(forms.Form):
    FAMILIA_PROCESADOR = (
        ("Ryzen", "Ryzen"),
        ("Intel", "Intel"),
    )

    nombreBusqueda = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar procesador por nombre'}))
    nucleos = forms.IntegerField(required=False, max_value=1000000000, label="Núcleos", widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}))
    hilos = forms.IntegerField(required=False, max_value=1000000000, label="Hilos", widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}))
    familiaprocesador = forms.MultipleChoiceField(
        choices=FAMILIA_PROCESADOR,
        required=False,
        label="Familia de Procesador",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'})
    )

    def clean(self):  # 3 VALIDACIONES
        """
        Validaciones adicionales para los campos del formulario.
        """
        cleaned_data = super().clean()
        nucleos = cleaned_data.get('nucleos')
        hilos = cleaned_data.get('hilos')
        nombre = cleaned_data.get('nombreBusqueda')
        familiaprocesador = cleaned_data.get('familiaprocesador')

        # Validación 1: Si los hilos no pueden ser menores que los núcleos
        if nucleos and hilos:
            if hilos < nucleos:
                # Usamos self.add_error() para agregar el error al campo 'hilos'
                self.add_error('hilos', 'El número de hilos no puede ser menor que el número de núcleos.')

        # Validación 2: Si el nombre tiene menos de 3 caracteres
        if nombre and len(nombre) < 3:
            # Usamos self.add_error() para agregar el error al campo 'nombreBusqueda'
            self.add_error('nombreBusqueda', 'El nombre debe tener al menos 3 caracteres.')
        
        # Validación adicional: Si todos los campos están vacíos
        if not nombre and not nucleos and not hilos and not familiaprocesador:
            self.add_error(None, "Por favor, rellene al menos un campo para la búsqueda.")

        return self.cleaned_data




#================================================================================================================================

class GraficaForm(forms.ModelForm):  # MODEL FORM
    class Meta:
        model = Grafica
        fields = 'nombre', 'urlcompra', 'familiagrafica', 'potenciacalculo', 'memoriavram', 'fecha_salida', 'trazadorayos', 'grafica_procesadores', 'placabase'  # Incluir todos los campos del modelo

        labels = {
            'nombre': 'Nombre de la grafica',
            'urlcompra': 'URL de compra',
            'familiagrafica': 'Familia de la grafica',
            'potenciacalculo': 'Potencia de Cálculo',
            'memoriavram': 'Cantidad de VRAM disponible',
            'fecha_salida': 'Fecha de salida:',
            'trazadorayos': 'Tiene trazado de rayos?',
            'grafica_procesadores': 'A que procesador esta enlazada?',
            'placabase': 'A que placabase va enlazada?'
        }
        help_texts = {
            'familiagrafica': 'Selecciona la familia a la que pertenece el procesador, sea AMD, Nvidia o Intel',
            'urlcompra': 'Introduce una URL válida donde se pueda comprar este procesador.',
            'memoriavram': 'Recuerda que la memoria VRAM son números'
        }
        widgets = {
            "nombre": forms.TextInput(attrs={'class': 'form-control'}),  # Widget de texto para el nombre
            "urlcompra": forms.URLInput(attrs={'class': 'form-control'}),  # Widget para la URL de compra
            "familiagrafica": forms.Select(attrs={'class': 'form-control'}),  # Dropdown para la familia de la gráfica
            "potenciacalculo": forms.NumberInput(attrs={'class': 'form-control'}),  # Campo numérico para la potencia de cálculo
            "memoriavram": forms.NumberInput(attrs={'class': 'form-control'}),  # Campo numérico para la memoria VRAM
            "trazadorayos": forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Checkbox para trazado de rayos
        }


class BusquedaAvanzadaGrafica(forms.Form):
    FAMILIA_GRAFICA = (
        ("AMD", "AMD"),
        ("Nvidia", "NVIDIA"),
        ("Intel", "Intel"),
    )

    nombreBusqueda = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar gráfica por nombre'}))
    potenciacalculo = forms.IntegerField(required=False, max_value=1000000000, label="Potencia Calculo", widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10000}))
    memoriavram = forms.IntegerField(required=False, max_value=1000000000, label="Memoria VRAM", widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10000}))
    familiagrafica = forms.MultipleChoiceField(
        choices=FAMILIA_GRAFICA,
        required=False,
        label="Familia de Gráfica",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    def clean(self):  # 3 VALIDACIONES
        """
        Validaciones adicionales para los campos del formulario.
        """
        cleaned_data = super().clean()
        potenciacalculo = cleaned_data.get('potenciacalculo')
        memoriavram = cleaned_data.get('memoriavram')
        nombre = cleaned_data.get('nombreBusqueda')
        familiagrafica = cleaned_data.get('familiagrafica')

        # Validación 1: La potencia de cálculo tiene que ser mayor que 500
        if potenciacalculo:
            if potenciacalculo < 500:
                self.add_error('potenciacalculo', 'La potencia de cálculo debe ser mayor que 500.')

        # Validación 2: Si el nombre tiene menos de 3 caracteres
        if nombre and len(nombre) < 6:
            self.add_error('nombreBusqueda', 'El nombre debe tener al menos 6 caracteres.')

        # Validación adicional: Si todos los campos están vacíos
        if not potenciacalculo and not memoriavram and not nombre and not familiagrafica:
            self.add_error(None, "Por favor, rellene al menos un campo para la búsqueda.")

        return self.cleaned_data


#================================================================================================================================


class MonitorForm(forms.ModelForm):  # MODEL FORM
    class Meta:
        model = Monitor
        fields = 'hz', 'urlcompra', 'calidad_respuesta', 'curvo', 'pantallafiltroplasma'  # Incluir todos los campos del modelo

        labels = {
            'hz': 'Tasa de refresco',
            'urlcompra': 'URL de compra',
            'calidad_respuesta': 'Calidad de respuesta (1ms?)',
            'curvo': 'Es curvo?',
            'pantallafiltroplasma': 'Tiene filtro plasma HDR?',
        }
        help_texts = {
            'hz': 'Selecciona los hercios del monitor',
            'urlcompra': 'Introduce una URL válida donde se pueda comprar este procesador.',
            'pantallafiltroplasma': 'Indique si tiene mediante booleano, no hace falta versión.'
        }
        widgets = {
            "hz": forms.NumberInput(attrs={'class': 'form-control'}),  # Campo numérico para la tasa de refresco
            "urlcompra": forms.URLInput(attrs={'class': 'form-control'}),  # URL para la compra
            "calidad_respuesta": forms.NumberInput(attrs={'class': 'form-control'}),  # Campo numérico para la calidad de respuesta
            "curvo": forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Checkbox para curvatura
            "pantallafiltroplasma": forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Checkbox para filtro plasma HDR
        }

        
    def clean_hz(self): 
        hz = self.cleaned_data.get("hz")
        if hz is not None:  
            try:
                hz = int(hz)  # Convertir a entero, da error en form si se pasa como string.
            except ValueError:
                raise forms.ValidationError("La tasa de refresco debe ser un número entero válido.")
            if hz <= 0:
                raise forms.ValidationError("La tasa de refresco debe ser un valor mayor que 0.")
        return hz

    
    def clean_calidad_respuesta(self):  
        calidad_respuesta = self.cleaned_data.get("calidad_respuesta")  
        if calidad_respuesta is not None:  # Asegurarnos de que el campo no esté vacío  
            if calidad_respuesta <= 0:  
                raise forms.ValidationError("La calidad de respuesta debe ser un valor mayor que 0.")  
        return calidad_respuesta  
    

class BusquedaAvanzadaMonitor(forms.Form):
    hz_min = forms.IntegerField(
        required=False,
        label="Tasa de refresco mínima (Hz)",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Ej. 60", 'class': 'form-control'})
    )
    hz_max = forms.IntegerField(
        required=False,
        label="Tasa de refresco máxima (Hz)",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Ej. 320", 'class': 'form-control'})
    )
    calidad_respuesta = forms.IntegerField(
        required=False,
        label="Calidad de respuesta máxima (ms)",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Ej. 1", 'class': 'form-control'})
    )
    curvo = forms.ChoiceField(
        required=False,
        label="¿Es curvo?",
        choices=[('1', 'Sí'), ('0', 'No')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    pantallafiltroplasma = forms.ChoiceField(
        required=False,
        label="¿Tiene filtro plasma HDR?",
        choices=[('1', 'Sí'), ('0', 'No')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    # Validaciones adicionales
    def clean(self):
        cleaned_data = super().clean()
        hz_min = cleaned_data.get("hz_min")
        hz_max = cleaned_data.get("hz_max")
        calidad_respuesta = cleaned_data.get("calidad_respuesta")
        curvo = cleaned_data.get("curvo")
        pantallafiltroplasma = cleaned_data.get("pantallafiltroplasma")

        # Validación 1: hz_min no debe ser mayor que hz_max
        if hz_min and hz_max and hz_min > hz_max:
            self.add_error("hz_max", "La tasa de refresco máxima debe ser mayor o igual a la mínima.")

        # Validación 2: calidad_respuesta no debe ser negativa
        if calidad_respuesta and calidad_respuesta <= 0:
            self.add_error("calidad_respuesta", "La calidad de respuesta debe ser mayor que 0.")

        # Validación adicional: Asegurar que al menos un campo esté lleno
        if not (hz_min or hz_max or calidad_respuesta or curvo or pantallafiltroplasma):
            self.add_error(None, "Por favor, rellene al menos un campo para realizar la búsqueda.")
        
        return cleaned_data


#================================================================================================================================

class FuenteForm(forms.ModelForm):
    class Meta:
        model = FuenteAlimentacion
        fields = 'vatios', 'urlcompra', 'amperaje', 'conectoresdisponibles', 'calidadfuente'  # Incluir todos los campos del modelo

        # Configuración opcional para personalizar etiquetas o mensajes de ayuda
        labels = {
            'vatios': 'Vatios de la fuente',
            'urlcompra': 'URL de compra',
            'amperaje': 'Amperaje de la fuente',
            'conectoresdisponibles': 'Conectores disponibles',
            'calidadfuente': 'Calidad de la fuente',
        }
        help_texts = {
            'vatios': 'Cuantos vatios tiene la fuente',
            'urlcompra': 'Introduce una URL válida donde se pueda comprar este procesador.',
            'calidadfuente': 'Recuerda que hay varias clasificaciones',
        }
        widgets = {
            'urlcompra': forms.URLInput(attrs={'class': 'form-control'}),
            'vatios': forms.NumberInput(attrs={'class': 'form-control'}),
            'amperaje': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # Validación simplificada para el campo 'vatios' (Debe ser mayor que 0)
    def clean_vatios(self):
        vatios = self.cleaned_data.get('vatios')
        if vatios is None or vatios <= 0:
            raise forms.ValidationError("El valor de vatios debe ser mayor que 0.")
        return vatios

    # Validación simplificada para el campo 'urlcompra' (Debe ser una URL válida)
    def clean_urlcompra(self):
        urlcompra = self.cleaned_data.get('urlcompra')
        if not urlcompra or not urlcompra.startswith(('http://', 'https://')):
            raise forms.ValidationError("La URL debe ser válida y comenzar con 'http://' o 'https://'.")
        return urlcompra


# Formulario de búsqueda avanzada
SELLO_CALIDAD_FUENTE = (
    ("80Bronce", "80Bronce"),
    ("80Silver", "80Silver"),
    ("80Gold", "80Gold"),
    ("80Plat", "80Plat"),
    ("80Titanium", "80Titanium"),
)

class BusquedaAvanzadaFuente(forms.Form):
    # Campos de búsqueda avanzada
    vatios = forms.IntegerField(
        required=False,
        label="Vatios",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Ej. Deep."})
    )
    amperaje = forms.IntegerField(
        required=False,
        label="Amperaje (A)",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Ej. 20"})
    )
    conectoresdisponibles = forms.CharField(  # Cambié a CharField para poder verificar la longitud
        required=False,
        label="Conectores disponibles",
        widget=forms.TextInput(attrs={"placeholder": "Ej. This one"})
    )
    calidadfuente = forms.ChoiceField(
        required=False,
        label="Calidad de la fuente",
        choices=SELLO_CALIDAD_FUENTE,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Validaciones adicionales
    def clean(self):
        cleaned_data = super().clean()
        vatios = cleaned_data.get("vatios")
        amperaje = cleaned_data.get("amperaje")
        conectoresdisponibles = cleaned_data.get("conectoresdisponibles")
        calidadfuente = cleaned_data.get("calidadfuente")

        # Validación adicional 1: Asegurarse de que al menos esta todo relleno (esta no cuenta como validacion)
        if not (vatios or amperaje or conectoresdisponibles or calidadfuente):
            self.add_error(None, "Por favor, rellene campos para realizar la búsqueda.")

        # Validación adicional 2: El amperaje debe ser mayor que 0 si está presente
        if amperaje is not None and amperaje <= 0:
            self.add_error('amperaje', "El amperaje debe ser mayor que 0.")
        
        # Validación adicional 3: La longitud de 'conectoresdisponibles' debe ser mayor que 1
        if conectoresdisponibles and len(conectoresdisponibles) <= 1:
            self.add_error('conectoresdisponibles', "El campo de conectores disponibles debe tener una longitud mayor que 1.")

        return cleaned_data


#================================================================================================================================

FAMILIA_RAM = (
    ("DDR3", "Formato DDR3"),
    ("DDR4", "Formato DDR4"),
    ("DDR5","FOrmato DDR5"),
)

class RamForm(forms.ModelForm):
    class Meta:
        model = Ram
        fields = 'fecha_fabricacion', 'mhz', 'familiaram', 'rgb', 'factormemoria'  # Incluir todos los campos del modelo

        # Configuración opcional para personalizar etiquetas o mensajes de ayuda
        labels = {
            'fecha_fabricacion': 'Fecha de fabricación del producto',
            'mhz': 'Megahercios del módulo de memoria',
            'familiaram': 'Familia de la RAM (DDR3, DDR4, DDR5)',
            'rgb': '¿Tiene luces RGB?',
            'factormemoria': 'Factor de memoria',
        }
        help_texts = {
            'fecha_fabricacion': 'Indica la fecha de fabricación del producto.',
            'familiaram': 'Selecciona el tipo de memoria (DDR3, DDR4 o DDR5).',
            'rgb': 'Indica si tiene luces RGB.',
        }
        widgets = {
            'fecha_fabricacion': forms.DateInput(attrs={'type': 'date'}),
            'mhz': forms.NumberInput(attrs={'placeholder': 'Ej. 2400 MHz', 'class': 'form-control'}),
            'rgb': forms.CheckboxInput(),
        }

    # Validación para asegurarse que MHz esté lleno (1)
    def clean_mhz(self):
        mhz = self.cleaned_data.get('mhz')
        if len(mhz) <= 0:
            raise forms.ValidationError('El valor de MHz debe estar lleno.')
        return mhz

    # Validación para la fecha de fabricación (no puede ser futura)
    def clean_fecha_fabricacion(self):
        fecha_fabricacion = self.cleaned_data.get('fecha_fabricacion')
        hoy = date.today() #Esto lo importamos de antes
        if fecha_fabricacion > hoy:
            raise forms.ValidationError('La fecha de fabricación no puede ser en el futuro.')
        return fecha_fabricacion

from django import forms
from .models import Ram

FAMILIA_RAM = (
    ("DDR3", "Formato DDR3"),
    ("DDR4", "Formato DDR4"),
    ("DDR5", "Formato DDR5"),
)
class RamAvanzadaForm(forms.Form):
    # Campos de búsqueda avanzada
    mhz = forms.CharField(
        required=False,
        label="Megahercios (MHz)",
        widget=forms.TextInput(attrs={"placeholder": "Ej. 2400", 'class': 'form-control'})
    )
    familiaram = forms.ChoiceField(
        required=False,
        label="Familia de la RAM",
        choices=FAMILIA_RAM,
        widget=forms.Select(attrs={"placeholder": "Selecciona una opción", 'class': 'form-control'})
    )
    fecha_fabricacion = forms.DateField(
        required=False,
        label="Fecha de fabricación",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    rgb = forms.BooleanField(
        required=False,
        label="¿Tiene luces RGB?",
        widget=forms.CheckboxInput()
    )
    factormemoria = forms.CharField(
        required=False,
        label="Factor de memoria",
        widget=forms.TextInput(attrs={"placeholder": "Ej. DIMM, SO-DIMM", 'class': 'form-control'})
    )

    # Validaciones adicionales
    def clean(self):
        cleaned_data = super().clean()
        mhz = cleaned_data.get("mhz")
        familiaram = cleaned_data.get("familiaram")
        fecha_fabricacion = cleaned_data.get("fecha_fabricacion")
        rgb = cleaned_data.get("rgb")
        factormemoria = cleaned_data.get("factormemoria")

        # Validación 1: Asegurarse de que al menos un campo esté relleno
        if not any([mhz, familiaram, fecha_fabricacion, rgb, factormemoria]):
            self.add_error(None, "Por favor, rellene al menos un campo para realizar la búsqueda.")

        # Validación 2: El valor de MHz debe ser mayor que 3 caracteres si se ingresa como texto
        if mhz and len(mhz) <= 3:
            self.add_error('mhz', "El valor de MHz debe ser mayor que 3 caracteres.")

        # Validación 3: Si se ha seleccionado una familia RAM, debe ser una opción válida
        if familiaram and familiaram not in dict(FAMILIA_RAM).keys():
            self.add_error('familiaram', "La familia de RAM seleccionada no es válida.")

        return cleaned_data
#================================================================================================================================

# Formulario de creación
class HDDForm(forms.ModelForm):  # MODEL FORM
    class Meta:
        model = DiscoDuroHdd
        fields = ['rpm', 'capacidad', 'peso', 'tiempomediofallos', 'pulgadas']  # Incluir todos los campos del modelo

        # Configuración opcional para personalizar etiquetas o mensajes de ayuda
        labels = {
            'rpm': 'Revoluciones por minuto',
            'capacidad': 'Capacidad disponible, normalmente en GB',
            'peso': 'Cuantos gramos pesa el disco duro',
            'tiempomediofallos': 'Tiempo medio entre fallos',
            'pulgadas': 'Longitud del disco duro (pulgadas)',
        }
        help_texts = {
            'rpm': 'Cuantos revoluciones por minuto tiene el disco duro.',
            'capacidad': 'Indique la capacidad en GB.',
            'tiempomediofallos': 'Es un valor que admite decimales.',
        }
        widgets = {
            'rpm': forms.NumberInput(attrs={'placeholder': 'Ej. 7200'}),
            'capacidad': forms.NumberInput(attrs={'placeholder': 'Ej. 500'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Ej. 700'}),
            'tiempomediofallos': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Ej. 15000'}),
            'pulgadas': forms.NumberInput(attrs={'min': '1', 'max': '100000', 'placeholder': 'Ej. 2.5'}),
        }

    def clean_peso(self):
        """Validación para asegurar que el peso sea un número positivo."""
        peso = self.cleaned_data.get('peso')
        try:
            if len(peso) <= 0:
                raise forms.ValidationError('El peso debe ser un valor positivo en cuanto a caracteres')
        except ValueError:
            raise forms.ValidationError('El peso debe ser un valor numérico.')
        return peso

    def clean_tiempomediofallos(self):
        """Validación para asegurar que el tiempo medio entre fallos sea un valor positivo y decimal."""
        tiempomediofallos = self.cleaned_data.get('tiempomediofallos')
        if tiempomediofallos <= 0:
            raise forms.ValidationError('El tiempo medio entre fallos debe ser un valor positivo.')
        return tiempomediofallos


# Formulario de búsqueda avanzada
class HDDBusquedaAvanzadaForm(forms.Form):
    rpm = forms.CharField(required=False, label="Revoluciones por minuto", widget=forms.TextInput(attrs={"placeholder": "Ej. 7200"}))
    capacidad = forms.CharField(required=False, label="Capacidad disponible (GB)", widget=forms.TextInput(attrs={"placeholder": "Ej. 500"}))
    peso = forms.CharField(required=False, label="Peso del disco duro (gramos)", widget=forms.TextInput(attrs={"placeholder": "Ej. 700"}))
    tiempomediofallos = forms.CharField(required=False, label="Tiempo medio entre fallos (horas)", widget=forms.TextInput(attrs={"placeholder": "Ej. 10000"}))
    pulgadas = forms.CharField(required=False, label="Tamaño en pulgadas", widget=forms.TextInput(attrs={"placeholder": "Ej. 2.5"}))

    def clean_rpm(self):
        rpm = self.cleaned_data.get('rpm')
        if rpm and len(rpm) <= 0:
            raise forms.ValidationError("Las revoluciones por minuto no pueden estar vacías.")
        return rpm

    def clean_pulgadas(self):
        pulgadas = self.cleaned_data.get('pulgadas')
        if pulgadas and (not pulgadas.replace('.', '', 1).isdigit() or float(pulgadas) <= 0 or float(pulgadas) > 35000):
            raise forms.ValidationError("El tamaño en pulgadas debe ser un número válido y mayor que 0 y menor o igual a 35000.")
        return pulgadas
    
#Retorna en 2 diferentes porque si no me daba un error raro.


#======================================================================================================================================================


class RegistroForm(UserCreationForm):
    roles = (
        (Usuario.CLIENTE, 'cliente'),
        (Usuario.TECNICOINFORMATICO, 'tecnicoinformatico'),
        (Usuario.VENDEDOR, 'vendedor'),
    )
    rol = forms.ChoiceField(choices = roles)
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rol')
        
        