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
        
BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']

FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]

class SimpleForm(forms.Form):
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES), required=False)
    favorite_colors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES, required=False)     

    