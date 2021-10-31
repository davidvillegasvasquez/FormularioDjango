from django.shortcuts import render
import psycopg2
from aplicacionConex.forms import FormNroCarton
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

def index(request):
    #codigos="92345a"
   
    try:
        conn = psycopg2.connect(host="localhost", database="controltickets", user="david", password="1234")

    except (Exception, psycopg2.DatabaseError) as error:
        idDelCliente1="sin servicio, intente de nuevo o más tarde"

    else:
        cursor = conn.cursor()
        cursor.execute("select id_cliente from consignación where no_consignación = 2")
        idDelCliente1 = cursor.fetchone()[0]
        conn.close()
        
    return render(request, "index.html", context={"IdClienteConsig1" : idDelCliente1})
    #Coloqué un literal -"92345a"- directamente en el diccionario context.

"""
def ConsulTicketCarton(request):
    return render(request, "consultaCarton.html", context={"montoEnPlantilla" : "8000Bs"})

"""
def ConsulTicketCarton(request):  
    
    formulario = FormNroCarton(request.GET)
    monto = formulario['campoIdTicket'].value()
    if monto == 'papa':
        monto='monto es papa'
    context = {'widget_formulario' : formulario, 'montoPlantilla': monto }
    return render(request, "consultaCarton.html", context)