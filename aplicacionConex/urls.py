from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [url(r'^$', views.index, name='index'), path('selectdate_widgetEjemplo', views.EjemSelectDateWidget, name='selectdatewidget'), path('grillanidadaEjemplo', views.EjemGrillaAnidada, name='grillanidada'), path('heredados_selecwidget', views.SelectWidgetHerencia, name='selecwidgetheritage'),]
