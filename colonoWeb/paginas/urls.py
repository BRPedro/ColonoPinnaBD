from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^cargadoArchivo/$', views.formularioImagen, name='cargado'),
    url(r'^cargadoI/$', views.cargadoConImagenO,name='cargadoI'),
    url(r'^prosesamiento/$', views.prosesamiento,name='prosesamiento'),
    url(r'^ajusteParametros/$', views.ajusteParametros,name='guardar'),
    url(r'^guardar/$', views.crearPDF,name='guardar'),
    url(r'^imagen/$', views.imagenO,name='imagen'),
    url(r'^animacion/$', views.animacio,name='animacion'),
]
