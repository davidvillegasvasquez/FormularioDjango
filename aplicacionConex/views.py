from django.shortcuts import render
import psycopg2
from aplicacionConex.forms import FormNroCarton #Note como se importan los módulos dentro de una aplicación django.
from django.http import HttpResponseRedirect, HttpResponse
from aplicacionConex.config import config #Note como se importan los módulos dentro de una aplicación django.
# Create your views here.

def index(request):

    #paramConex = config()
    formulario = FormNroCarton(request.GET)
    idTicket = formulario['campoIdTicket'].value() #Y así obtemos el valor actual del atributo campoIdTicket de la clase FormNroCarton, que es el que se encuentre actualmente en el widget formulario.
    acum_visitas = request.session.get('num_visits', 0) #Contador de visitas. Sirve para configurar la presentación de la página cuando se accede por primera vez. Considere que num_visits es el nombre arbitrario
    request.session['num_visits'] = acum_visitas + 1 # Recordar que cuando se aplica un contador de visitas, se requiere tener habilitada una base de datos en el proyecto, para guardar los datos de las sesiones que se almacenan en las cookies. De modo que se debe hacer un "python manage.py migrate" para que se haga efectiva esta implementación. Investigar si hay alguna manera de lograr el mismo efecto sin la necesidad de habilitar una base de datos en el proyect, sólo usando la externa.
    
    if idTicket is not None: #Primero evaluamos que haya algo en el control.
        try:
            paramConex = config() #Estudiar dónde es mejor que vaya esta proposición.
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
            
    context = {'widget_formulario' : formulario, 'montoPlantilla': monto, 'cantVisitas': acum_visitas,}
    
    return render(request, "index.html", context)