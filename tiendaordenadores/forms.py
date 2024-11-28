from django import forms
from .models import Procesador
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
        
        
    
#================================================================================================================================
from django import forms

class BusquedaAvanzadaProcesador(forms.Form):
    FAMILIA_PROCESADOR = (
        ("Ryzen", "Ryzen"),
        ("Intel", "Intel"),
    )

    nombreBusqueda = forms.CharField(required=False)
    nucleos = forms.IntegerField(required=False, max_value=1000000000, label="Núcleos")
    hilos = forms.IntegerField(required=False, max_value=1000000000, label="Hilos")
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

        return cleaned_data
