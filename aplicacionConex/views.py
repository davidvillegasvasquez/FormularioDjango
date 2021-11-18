from django.shortcuts import render
import psycopg2
from aplicacionConex.forms import FormNroCarton, SimpleForm #Note como se importan los formularios definidos por el usuario de una aplicación django, en este caso específico, el módulo forms.py, más específicamente las clases definidas por el usuario, FormNroCarton y SimpleForm contenidas en dicho modulo forms.
from django.http import HttpResponseRedirect, HttpResponse
from aplicacionConex.config import config #Note como se importan los módulos dentro de una aplicación django.


# Create your views here.


def index(request):

    acum_visitas = request.session.get('num_visits', 0) #Contador de visitas. Sirve para configurar la presentación de la página cuando se accede por primera vez. Considere que num_visits es el nombre arbitrario. Requiere base de datos interna.
    
    request.session['num_visits'] = acum_visitas + 1 # Recordar que cuando se aplica un contador de visitas, se requiere tener habilitada una base de datos en el proyecto, para guardar los datos de las sesiones que se almacenan en las cookies. De modo que se debe hacer un "python manage.py migrate" para que se haga efectiva esta implementación. Investigar si hay alguna manera de lograr el mismo efecto sin la necesidad de habilitar una base de datos en el proyecto, sólo usando la externa dónde se almacenaran dicha cantidad.
    
    context = {'cantVisitas': acum_visitas,}
    context.update(Formulario(request))
     
    return render(request, "index.html", context)
    
  
def EjemSelectDateWidget(request):
    """  
    context = Formulario(request)
    formularioSimpleForm = SimpleForm(request.GET)
    
    contexSelectDateWidget = {'formuSimpEnPlantilla' : formularioSimpleForm,}
    
    #contexSelectDateWidget.update(context) #con el atributo-metodo update() para los diccionarios, concatenamos el diccionario apuntado por el identificador context a la función Formulario, que retorna dicho formulario. Así podremos mandar todas las variables de contexto de ambos formularios a la plantilla común, en este caso plantillaSelectDateWidget.html.
    
    
    #Racionalizamos el código para hacerlo más corto:
    contexSelectDateWidget = {'formularioEnPlantilla' : SimpleForm(request.GET),}
    """
    
    #Pero como necesitamos acceder a los valores de todos los campos atributos del objeto de clase SimpleForm, tenemos que usar necesariamente un identificador apuntador, en este caso formularioSimpleForm:
    
    formularioSimpleForm = SimpleForm(request.GET)
    
    #Extraemos los valores de sus atributos recogidos en las solicitudes:
    atrib_birth_year = formularioSimpleForm['birth_year'].value()
    atrib_favorite_colors = formularioSimpleForm['favorite_colors'].value()
    
    #Preparamos el diccionario principal con las variables de contexto para la plantilla:
    contexSelectDateWidget = {'formularioEnPlantilla' : formularioSimpleForm, 'atrib_birth_year_EnPlantilla' : atrib_birth_year, 'atrib_favorite_colors_EnPlantilla' : atrib_favorite_colors,}
    
    #Concatenamos con el diccionario que retorna el formulario de consulta de tickets:
    contexSelectDateWidget.update(Formulario(request))
    
    #Finalmente renderizamos en la plantilla asociada a la vista, plantillaSelectDataWidget.html:
    return render(request, "plantillaSelectDateWidget.html", contexSelectDateWidget) 
    
    
def Formulario(requestParam):
    """Recordar que esta función no es una vista, pues no renderiza para plantilla alguna, sin embargo todas las vistas la invocan puesto que en todos los documentos del sitio estará disponible este formulario de consult de idticket cartón."""
    #paramConex = config()
    formulario = FormNroCarton(requestParam.GET)
    idTicket = formulario['campoIdTicket'].value() #Y así obtemos el valor actual del atributo campoIdTicket de la clase FormNroCarton, que es el que se encuentre actualmente en el widget formulario.
    
    if idTicket is not None: #Primero evaluamos que haya algo que recoger en el control al darle al botón enviar (submmit), que es el que desencadena la solicitud (request).
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
            
    context = {'formularioEnPlantillaBase' : formulario, 'montoPlantilla': monto,}
    
    return context
    
    
def EjemGrillaAnidada(request):
      
    context = Formulario(request)
    
    return render(request, "grillaAnidada.html", context)
    
from aplicacionConex.forms import FormSeleccionBase  

def SelectWidgetRadioButton(request):
    formularioSelect = FormSeleccionBase(request.GET)
    #Para obtener los valores de la selección, aplicamos el método atributo value() a su campo selección:
    valores_formulario = formularioSelect['seleccion'].value() #seleccion es el único atributo de la clase FormSeleccionBase, instanciada y apuntada con el identificador formularioSelect.
    print("type(valores_formulario):", type(valores_formulario)) #Vemos que retorna un <class 'str'>. 
    
    #Nota: Recuerde que para poder tomar los valores de la selección, se debe configurar el formulario en la plantilla, dotándolo de un elemento input (en nuestro caso <input type="submit" value="selección"> dentro de una elemento form <form action="" method="GET">), que es el que enviará la solicitud (request).
    contexto = {'formularioEnPlantilla' : formularioSelect, 'valSelecEnPlanti': valores_formulario,} 
    contexto.update(Formulario(request)) #Si agrego el formulario cosulta de ticket, no me aparece el selec con radiobutton. Averiguar esto. Resp: era porque el nombre colicionaba con el de la plantilla base (formularioEnPlantilla). Procedí a cambiar el nombre de formulario en plantilla base por formularioEnPlantillaBase, para que no se confundieran las dos variables de contexto en la misma plantilla html dónde actúan.
    
    return render(request, "plantillaSelectRadioButton.html", contexto)
    
    
from aplicacionConex.forms import FormSelectCombo

def FormComboBox(request):
    
    #contexto = {'formularioEnPlantilla' : 'Una cadena de caracteres es lo que mando.',} Fijese como puedo mandar un literal como variable de contexto para la plantilla.
    formulario = FormSelectCombo(request.GET)
    valtextoSelec = formulario['texto'].value()
    print('formulario[\'texto\'].value()=', valtextoSelec)
    valnumSelec = formulario['numero'].value()
    
    contexto = {'formularioEnPlantilla' : formulario, 'valtextoSelecEnPlanti': valtextoSelec, 'valnumSelecEnPlanti': valnumSelec,} 
    #contexto.update(Formulario(request)) #Claro, si no concateno con el diccionario que retorna Formulario(request), no tendré el formulario de consuta de ticket.
    return render(request, "plantillaSelectCombobox.html", contexto)
    
    
from aplicacionConex.forms import OperacionesMatematicas

def Operacion(request):
    
    formOperacMat = OperacionesMatematicas(request.GET)#, initial=[{'operacion': '+', 'txtBox1': 0, 'txtBox2': 0,}])
    
    operacionSelec = formOperacMat['operacion'].value()
    numeroTxtBox1 = formOperacMat['txtBox1'].value()
    #Imprimimos en la terminal a ver que valor arroja ormOperacMat['txtBox1'].value():
    print("formOperacMat['txtBox1'].value()=", numeroTxtBox1)
    numeroTxtBox2 = formOperacMat['txtBox2'].value()
    
    #Validación rudimentario por no saber usar bien el framework:
    resultado = 0
    if operacionSelec is not None: #Los tipo forms.ChoiceField retornan None si no se coloca nada en el widget de dicho forms.
    
        if numeroTxtBox1 != '': #Comienza con cadena de longitud 0, no None type, puesto que los forms.CharField retorna dicha cadena vacía si no se coloca nada en el widget que se le asigne a dicho tipo de forms.
            if numeroTxtBox2 != '': 
                resultado = int(numeroTxtBox1) + int(numeroTxtBox2)
            else: 
                resultado = '0'
        else: 
            resultado = '0'
    else: 
        resultado = '0'
    
    #resultado = int(numeroTxtBox1) + int(numeroTxtBox2)
    
    #Procedemos a renderizar:
    contexto = {'formularioEnPlantilla' : formOperacMat, 'resultadoEnPlantilla': resultado,} 
    #contexto.update(Formulario(request)) #Claro, si no concateno con el diccionario que retorna Formulario(request), no tendré el formulario de consuta de ticket.
    return render(request, "plantillaOperacionMat.html", contexto)
    