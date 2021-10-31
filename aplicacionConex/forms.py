from django import forms
from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _

class FormNroCarton(forms.Form):
    #Definimos el atributo-campo de tipo DateField, campoFechaDeRenovacion:
    campoIdTicket = forms.CharField(label="Nº de cartón:", required=False)
    #Con required en false, no me pone el aviso con viñetas encima del control.
    def clean_campoIdTicket(self):
        #self.cleaned_data['campoIdTicket'] 
        return self.cleaned_data['campoIdTicket']

    