from django.shortcuts import render
import psycopg2
from aplicacionConex.forms import FormNroCarton, SimpleForm #Note como se importan los formularios definidos por el usuario de una aplicación django, en este caso específico, el módulo forms.py, más específicamente las clases definidas por el usuario, FormNroCarton y SimpleForm contenidas en dicho modulo forms.
from django.http import HttpResponseRedirect, HttpResponse
from aplicacionConex.config import config #Note como se importan los módulos dentro de una aplicación django.


# Create your views here.


def index(request):
    
    context = Formulario(request) 
     
    return render(request, "index.html", context)
    
  
def EjemSelectDateWidget(request):
    """  
    context = Formulario(request)
    formularioSimpleForm = SimpleForm(request.GET)
    
    contexSelectDateWidget = {'formuSimpEnPlantilla' : formularioSimpleForm,}
    
    #contexSelectDateWidget.update(context) #con el atributo-metodo update() para los diccionarios, concatenamos el diccionario apuntado por el identificador context a la función Formulario, que retorna dicho formulario. Así podremos mandar todas las variables de contexto de ambos formularios a la plantilla común, en este caso plantillaSelectDateWidget.html.
    """
    
    #Racionalizamos el código para hacerlo más corto:
    contexSelectDateWidget = {'formularioEnPlantilla' : SimpleForm(request.GET),}
    contexSelectDateWidget.update(Formulario(request))
    
    return render(request, "plantillaSelectDateWidget.html", contexSelectDateWidget) 
    
    
def Formulario(requestParam):
    """Recordar que esta función no es una vista, pues no renderiza para plantilla alguna, sin empargo todas las vistas la invocan puesto que todos los documentos del sitio se verá el formulario."""
    #paramConex = config()
    formulario = FormNroCarton(requestParam.GET)
    idTicket = formulario['campoIdTicket'].value() #Y así obtemos el valor actual del atributo campoIdTicket de la clase FormNroCarton, que es el que se encuentre actualmente en el widget formulario.
    acum_visitas = requestParam.session.get('num_visits', 0) #Contador de visitas. Sirve para configurar la presentación de la página cuando se accede por primera vez. Considere que num_visits es el nombre arbitrario. Requiere base de datos interna.
    requestParam.session['num_visits'] = acum_visitas + 1 # Recordar que cuando se aplica un contador de visitas, se requiere tener habilitada una base de datos en el proyecto, para guardar los datos de las sesiones que se almacenan en las cookies. De modo que se debe hacer un "python manage.py migrate" para que se haga efectiva esta implementación. Investigar si hay alguna manera de lograr el mismo efecto sin la necesidad de habilitar una base de datos en el proyecto, sólo usando la externa dónde se almacenaran dicha cantidad.
    
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
            else: 
                monto = ""
                
            conn2.close() #Cerramos conexión independientemente del resultado, pues teníamos esta conexión abierta.
                
    else:
        monto = "" #Esto evita que aparezca None, o el error de "UnboundLocalError: local variable 'monto' referenced before assignment" cuando se abre la página por primera vez.
            
    context = {'formularioEnPlantillaBase' : formulario, 'montoPlantilla': monto, 'cantVisitas': acum_visitas,}
    
    return context
    
    
def EjemGrillaAnidada(request):
      
    context = Formulario(request)
    
    return render(request, "grillaAnidada.html", context)
    
from aplicacionConex.forms import FormSeleccionBase  

def SelectWidgetHerencia(request):
    
    contexto = {'formularioEnPlantilla' : FormSeleccionBase(request.GET),} 
    contexto.update(Formulario(request)) #Si agrego el formulario cosuta de ticket, no me aparece el selec con radiobutton. Averiguar esto. Resp: era porque el nombre concordaba con el de la plantilla base (formularioEnPlantilla). Procedí a cambiar el nombre de formulario en plantilla base por formularioEnPlantillaBase, para que no se confundieran las dos variables de contexto en la misma plantilla html dónde actuan.
    
    return render(request, "plantillaSelectWidgetHeredado.html", contexto)
    
    
from aplicacionConex.forms import FormAplicEstilos

def AplicEstilos(request):
    
    contexto = {'formularioEnPlantilla' : FormAplicEstilos(request.GET),}
    #contexto.update(Formulario(request)) #Claro, si no concateno con el diccionario que retorna Formulario(request), no tendré el formulario de consuta de ticket (tampoco visitas).
    
    return render(request, "plantillaAplicandoEstilos.html", contexto)
    