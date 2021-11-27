from django import forms
from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _

class FormNroCarton(forms.Form):
    #Definimos el atributo-campo de tipo DateField, campoFechaDeRenovacion:
    campoIdTicket = forms.CharField(label="Nº de cartón:", required=False, max_length=10, widget=forms.TextInput(attrs={'size': '6'})) #Note como configuramos su dimensión cuando lo instanciemos con el widget TextInput.
    #Con required en false, no me pone el aviso con viñetas encima del control.
    def clean_campoIdTicket(self):
        #self.cleaned_data['campoIdTicket'] 
        return self.cleaned_data['campoIdTicket']


class SimpleForm(forms.Form):
    #Declaramos atributos constantes de esta clase (estas puden dejar de ser atributos particulares de una clase, y ser a nivel de módulo para uso común de todas las clases (espacio de nombres a nivel de módulo):      
    BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']

    FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES), required=False)
    
    favorite_colors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES, required=False)  
        
class FormSeleccionBase(forms.Form):
    #Lo usamos para el ejemplo del widget tipo RasioSelect
    CHOICES = [('1', 'First'), ('10000', 'Second')]
    seleccion = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False) 
    
class FormSelectCombo(forms.Form):
    #Recordar que las listas para el parámetro choices deben ser listas o tuplas de tuplas de dos elementos, las cuales el Primer elemento es el módulo, y el segundo, su representación en el listbox.
    textos = [('1', 'texto1'), ('2', 'texto2'), ('3', 'texto3')]
    numeros = [(1, '1'), (2, '2'), (3, '3')]
    
    texto = forms.ChoiceField(choices=textos, required=False)
    numero = forms.ChoiceField(choices = numeros, required=False)  

class OperacionesMatematicas(forms.Form):
    #Recordar que las listas para el parámetro choices deben ser listas o tuplas de tuplas de dos elementos, las cuales el Primer elemento es el módulo, y el segundo, su representación que será el que se muestre en el listbox.
    operaciones = [('+', 'suma'), ('-', 'resta'), ('*', 'multiplicación'), ('/', 'división')]
    
    operacion = forms.ChoiceField(choices=operaciones, required=False)
    #Con forms.ChoiceField y forms.DoubleField podemos ingresar numeros decimales.      
    #formularios de tipo forms.DecimalField o forms.DoubleField, nos obliga a meter sólo números, por lo cual no hace falta validar explicitamente por el usuario. 
    #Note también como se establece el ancho del  widget txtBox, a diferencia del que use arriba para forms.TextField:
    txtBox1 = forms.FloatField(required=False)#, widget=forms.NumberInput(attrs={'style': 'width: 100px'}))
    
    txtBox2 = forms.FloatField()# decimal_places=2 (sólo aplicable en forms.DecimalField). Con el parámetro decimal_places, nos notifica el número de decimales que podemos meter, obligando a introducir la cantidad correcta, más no lo trunca, corrige automáticamente.
    
class FormCostoEnvio(forms.Form):
    
    
    largo = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 100px'}))
    
    ancho = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 100px'}))
    
    alto = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 100px'}))
    
    peso = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 100px'}))
    
#Formulario para el tutoria de Crispy Forms:
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit
 
class ExampleForm(forms.Form):

    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))
    
    