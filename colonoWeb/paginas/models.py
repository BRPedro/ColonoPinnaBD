from __future__ import unicode_literals
from django.db import models

"""
Modelo de la tabla en la base de datos.
"""
class TC_PATRON(models.Model):
    idpatron = models.AutoField(primary_key=True)   #Id de la tabla de patrones.
    xp = models.IntegerField(null=True)          #Fila central del patron.
    yp = models.IntegerField(null=True)       #Columna central del patron.
    contadorp = models.IntegerField(default=0)      #Tamanno del patron.
