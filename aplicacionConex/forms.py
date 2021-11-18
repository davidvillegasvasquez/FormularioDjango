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
    #Recordar que las listas para el parámetro choices deben ser listas o tuplas de tuplas, las cuales el Primer elemento es el módulo, y el segundo, su representación en el listbox.
    textos = [('1', 'texto1'), ('2', 'texto2'), ('3', 'texto3')]
    numeros = [(1, '1'), (2, '2'), (3, '3')]
    
    texto = forms.ChoiceField(choices=textos, required=False)
    numero = forms.ChoiceField(choices = numeros, required=False)  

class OperacionesMatematicas(forms.Form):
    #Recordar que las listas para el parámetro choices deben ser listas o tuplas de tuplas, las cuales el Primer elemento es el módulo, y el segundo, su representación en el listbox.
    operaciones = [('+', 'suma'), ('-', 'resta'), ('*', 'multiplicación'), ('/', 'multiplicación')]
    
    operacion = forms.ChoiceField(choices=operaciones, required=False)
    
    txtBox1 = forms.CharField(required=False, max_length=10, widget=forms.NumberInput(attrs={'size': '6'}))
    txtBox2 = forms.CharField(required=False, max_length=10, widget=forms.NumberInput(attrs={'size': '6'}))
    