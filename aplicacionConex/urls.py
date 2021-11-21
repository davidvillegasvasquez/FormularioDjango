from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [url(r'^$', views.index, name='index'), path('selectdate_widgetEjemplo', views.EjemSelectDateWidget, name='selectdatewidget'), path('grillanidadaEjemplo', views.EjemGrillaAnidada, name='grillanidada'), path('radiobutton_selecwidget', views.SelectWidgetRadioButton, name='radioButtonSelectEjem'), path('combobox_widgets', views.FormComboBox, name='combobox'), path('operacionesMatemáticas', views.Operacion, name='aritmetica'), path('calculador_costoenvio', views.CostoEnvio, name='costo'), path('ejercicios_crispyforms', views.inbox, name='crispy'),]
