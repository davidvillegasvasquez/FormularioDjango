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
    CHOICES = [('1', 'First'), ('10000', 'Second')]
    seleccion = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False) 
    
class FormAplicEstilos(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}), required=False)
    url = forms.URLField(required=False)
    comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}), required=False)  

    