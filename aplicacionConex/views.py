from django.shortcuts import render
import psycopg2
from aplicacionConex.forms import FormNroCarton #Note como se importan los módulos dentro de una aplicación django.
from django.http import HttpResponseRedirect, HttpResponse
from aplicacionConex.config import config #Note como se importan los módulos dentro de una aplicación django.
# Create your views here.

def index(request):

    paramConex = config()
    formulario = FormNroCarton(request.GET)
    idTicket = formulario['campoIdTicket'].value()
    
    if idTicket is not None: #Primero evaluamos que haya algo en el control.
        try:
            conn2 = psycopg2.connect(**paramConex) 
        except (Exception, psycopg2.DatabaseError) as error:
            idDelCliente1="Sin conexión en este momento, intente de nuevo o más tarde"
        else:
            cursor2 = conn2.cursor()
            cursor2.execute("select monto from ticket_cartón_recibidos where id_cartón = %s limit 1",(idTicket,))
            monto = cursor2.fetchone() #Recordar que los fetch siempre se deben hacer antes de cerrar conexión.
            
            if monto is not None:
                monto = monto[0]
                conn2.close()
            else: 
                monto = ""
                conn2.close()
    else:
        monto = "" #Esto evita que aparezca None, o el error de "UnboundLocalError: local variable 'monto' referenced before assignment" cuando se abre la página por primera vez.
            
    context = {'widget_formulario' : formulario, 'montoPlantilla': monto,}
    
    return render(request, "index.html", context)