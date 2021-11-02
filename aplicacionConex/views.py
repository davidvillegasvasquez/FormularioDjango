from django.shortcuts import render
import psycopg2
from aplicacionConex.forms import FormNroCarton
from django.http import HttpResponseRedirect, HttpResponse
from config import config
# Create your views here.

def index(request):
    paramConex = config()
    try:
        conn = psycopg2.connect(**paramConex)

    except (Exception, psycopg2.DatabaseError) as error:
        idDelCliente1="sin servicio, intente de nuevo o más tarde"

    else:
        cursor = conn.cursor()
        cursor.execute("select id_cliente from consignación where no_consignación = 2")
        idDelCliente1 = cursor.fetchone()[0]
        conn.close()
        
    return render(request, "index.html", context={"IdClienteConsig1" : idDelCliente1})

def ConsulTicketCarton(request):  
    
    formulario = FormNroCarton(request.GET)
    idTicket = formulario['campoIdTicket'].value()
    if idTicket is not None: #Primero evaluamos que haya algo en el control.
        try: #Luego evaluamos que haya conexión.
            paramConex = config()
            conn = psycopg2.connect(**paramConex)

        except (Exception, psycopg2.DatabaseError) as error:
            monto = "sin servicio, intente de nuevo o más tarde"

        else:
            cursor = conn.cursor()
            cursor.execute("select monto from ticket_cartón_recibidos where id_cartón = %s limit 1",(idTicket,))
            monto = cursor.fetchone()
            if monto is not None:
                monto = monto[0]
            else: 
                monto = ""
            conn.close()
    else:
        monto = ""

    context = {'widget_formulario' : formulario, 'montoPlantilla': monto }
    return render(request, "consultaCarton.html", context)