from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [url(r'^$', views.index, name='index'), path('ejemploselectwidget', views.EjemSelectWidget, name='selectwidget'),]
