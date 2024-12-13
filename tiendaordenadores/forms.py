from django import forms
from .models import Procesador, Grafica, Monitor, FuenteAlimentacion, Ram, DiscoDuroHdd
#================================================================================================================================

class ProcesadorForm(forms.ModelForm): #MODEL FORM
    class Meta:
        model = Procesador
        fields = 'nombre', 'urlcompra', 'familiaprocesador', 'potenciacalculo', 'nucleos', 'hilos', 'placabase'  # Incluir todos los campos del modelo

        # Configuración opcional para personalizar etiquetas o mensajes de ayuda
        labels = {
            'nombre': 'Nombre del Procesador',
            'urlcompra': 'URL de compra',
            'familiaprocesador': 'Familia del Procesador',
            'potenciacalculo': 'Potencia de Cálculo',
            'nucleos': 'Número de Núcleos',
            'hilos': 'Número de Hilos',
            'placabase': 'Placa Base',
        }
        help_texts = {
            'familiaprocesador': 'Selecciona la familia a la que pertenece el procesador, sea Intel o Ryzen',
            'urlcompra': 'Introduce una URL válida donde se pueda comprar este procesador.',
        }
        widgets = {
        'nombre': forms.TextInput(attrs={'class': 'form-control'}),      
}
        
class BusquedaAvanzadaProcesador(forms.Form):
    FAMILIA_PROCESADOR = (
        ("Ryzen", "Ryzen"),
        ("Intel", "Intel"),
    )

    nombreBusqueda = forms.CharField(required=False)
    nucleos = forms.IntegerField(required=False, max_value=1000000000, label="Núcleos") #Esta validacion no cuenta segun profesor
    hilos = forms.IntegerField(required=False, max_value=1000000000, label="Hilos") #Esta validacion no cuenta segun profesor
    familiaprocesador = forms.MultipleChoiceField(
        choices=FAMILIA_PROCESADOR,
        required=False,
        label="Familia de Procesador"
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
        # Comprobamos que no haya valores vacíos en todos los campos
        if not nombre and not nucleos and not hilos and not familiaprocesador:
            # Usamos self.add_error() para agregar un error global (no a un campo específico)
            self.add_error(None, "Por favor, rellene al menos un campo para la búsqueda.")

        return self.cleaned_data



#================================================================================================================================

class GraficaForm(forms.ModelForm): #MODEL FORM
    class Meta:
        model = Grafica
        fields = 'nombre', 'urlcompra', 'familiagrafica', 'potenciacalculo', 'memoriavram', 'fecha_salida', 'trazadorayos', 'grafica_procesadores', 'placabase'  # Incluir todos los campos del modelo

        # Configuración opcional para personalizar etiquetas o mensajes de ayuda
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
            'memoriavram': 'Recuerda que la memoriaVRAM son numeros'
        }
        widgets = {
            "potenciacalculo" : forms.NumberInput(),
        }
        

class BusquedaAvanzadaGrafica(forms.Form):       
        FAMILIA_GRAFICA = (
        ("AMD", "AMD"),
        ("Nvidia", "NVIDIA"),
        ("Intel", "Intel"),
        )
    
        nombreBusqueda = forms.CharField(required=False)
        potenciacalculo = forms.IntegerField(required=False, max_value=1000000000, label="PotenciaCalculo") #Esta validacion no cuenta segun profesor
        memoriavram = forms.IntegerField(required=False, max_value=1000000000, label="MemoriaVRAM") #Esta validacion no cuenta segun profesor
        familiagrafica = forms.MultipleChoiceField(
        choices=FAMILIA_GRAFICA,
        required=False,
        label="Familia de Grafica"
    )

def clean(self):  # 3 VALIDACIONES
    """
    Validaciones adicionales para los campos del formulario.
    """
    cleaned_data = super().clean()
    potenciacalculo = cleaned_data.get('nucleos')
    memoriavram = cleaned_data.get('hilos')
    nombre = cleaned_data.get('nombreBusqueda')
    familiagrafica = cleaned_data.get('familiagrafica')

    # Validación 1: La potencia de calculo tiene que ser MAYOR que 500
    if potenciacalculo:
        if potenciacalculo > 500:
            self.add_error('potenciacalculo', 'El número de potencia de cálculo debe ser mayor que 500.')

    # Validación 2: Si el nombre tiene menos de 3 caracteres
    if nombre and len(nombre) < 6:
        # Usamos self.add_error() para agregar el error al campo 'nombreBusqueda'
        self.add_error('nombreBusqueda', 'El nombre debe tener al menos 3 caracteres.')

    # Validación adicional: Si todos los campos están vacíos
    # Comprobamos que no haya valores vacíos en todos los campos
    if not potenciacalculo and not memoriavram and not nombre and not familiagrafica:
        # Usamos self.add_error() para agregar un error global (no a un campo específico)
        self.add_error(None, "Por favor, rellene al menos un campo para la búsqueda.")

    return self.cleaned_data

#================================================================================================================================


class MonitorForm(forms.ModelForm): #MODEL FORM
    class Meta:
        model = Monitor
        fields = 'hz', 'urlcompra', 'calidad_respuesta', 'curvo', 'pantallafiltroplasma',  # Incluir todos los campos del modelo

        # Configuración opcional para personalizar etiquetas o mensajes de ayuda
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
            'pantallafiltroplasma': 'Indique si tiene mediante booleano, no hace falta version'
        }
        widgets = {
            "hz" : forms.NumberInput(),
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
    # Campos de búsqueda avanzada
    hz_min = forms.IntegerField(
        required=False,
        label="Tasa de refresco mínima (Hz)",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Ej. 60"})
    )
    hz_max = forms.IntegerField(
        required=False,
        label="Tasa de refresco máxima (Hz)",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Ej. 320"})
    )
    calidad_respuesta = forms.IntegerField(
        required=False,
        label="Calidad de respuesta máxima (ms)",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Ej. 1"})
    )
    curvo = forms.CharField(
        required=False,
        label="¿Es curvo?",
        widget=forms.RadioSelect(choices=[('1', 'Sí'), ('0', 'No')])
    )
    pantallafiltroplasma = forms.CharField(
        required=False,
        label="¿Tiene filtro plasma HDR?",
        widget=forms.RadioSelect(choices=[('1', 'Sí'), ('0', 'No')])
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

        # Validación adicional: Asegurar que todos los campos están llenos
        if not (hz_min or hz_max or calidad_respuesta or curvo or pantallafiltroplasma):
            self.add_error(None, "Por favor, rellene al menos un campo para realizar la búsqueda.")
        
        return cleaned_data


#================================================================================================================================

class FuenteForm(forms.ModelForm): #MODEL FORM
    class Meta:
        model = FuenteAlimentacion
        fields = 'vatios', 'urlcompra', 'amperaje', 'conectoresdisponibles', 'calidadfuente',  # Incluir todos los campos del modelo

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
            'calidadfuente': 'Recuerda que hay varias clasificaciones'
        }
        widgets = {
            "urlcompra" : forms.URLInput(),
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
        widget=forms.Select(attrs={"placeholder": "Selecciona una opción"})
    )

    # Validaciones adicionales
    def clean(self):
        cleaned_data = super().clean()
        vatios = cleaned_data.get("vatios")
        amperaje = cleaned_data.get("amperaje")
        conectoresdisponibles = cleaned_data.get("conectoresdisponibles")
        calidadfuente = cleaned_data.get("calidadfuente")

        # Validación adicional 1: Asegurarse de que al menos esta todo relleno (esta no cuenta como validacion)
        if not (vatios and amperaje and conectoresdisponibles and calidadfuente):
            self.add_error(None, "Por favor, rellene campos para realizar la búsqueda.")

        # Validación adicional 2: El amperaje debe ser mayor que 0 si está presente
        if amperaje is not None and amperaje <= 0:
            self.add_error('amperaje', "El amperaje debe ser mayor que 0.")
        
        # Validación adicional 3: La longitud de 'conectoresdisponibles' debe ser mayor que 1
        if conectoresdisponibles and len(conectoresdisponibles) <= 1:
            self.add_error('conectoresdisponibles', "El campo de conectores disponibles debe tener una longitud mayor que 1.")

        return cleaned_data