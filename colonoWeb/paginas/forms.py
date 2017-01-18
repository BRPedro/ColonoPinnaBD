from django import forms

#Formulario usado en el cargado de la imagen.
class UploadFileForm(forms.Form):
   archivo = forms.FileField()

#Formulario usado en la configuracion de los Parametros.
class Parametros(forms.Form):
   altura =forms.DecimalField(label='Altura de vuelo:',min_value=1.0)
   escala = forms.DecimalField(label='Escala pixel x metro:',min_value=0.5)
   ruido = forms.IntegerField(label='Filtro de ruido:',min_value=0)
   proximidad=forms.DecimalField(label='Proximidad:',min_value=0.0)
   circulo= forms.IntegerField(label='Escala circulo',min_value=1)
