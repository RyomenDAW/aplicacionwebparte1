from django import forms
from .models import Procesador, Grafica
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

    # Validación 1: 
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
