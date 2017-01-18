#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

"""
Función encargada encargada de dimensionar la imagen para presentarla en la interfaz web.
Parámetros:
	imagen: imagen a la que se quiere cambiar el tamaño.
	nombre: nombre con el que se guardara la imagen redimensionada.
Nota: la dirección de guardado esta empotrada en el código.
"""
def cambio(imagen,nombre):
    f,c,t=imagen.shape
    if f>400:
        porcen=(400.0*100.0/f)/100.0
        imagen=cv2.resize(imagen,(int(c*porcen),int(f*porcen)),interpolation=cv2.INTER_CUBIC)
    f,c,t=imagen.shape
    if c>400:
        porcen=(400.0*100.0/c)/100.0
        imagen=cv2.resize(imagen,(int(c*porcen),int(f*porcen)),interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("paginas\\static\\paginaP\\img\\"+nombre, imagen)
#***************************************************************************************************

"""
Función encargada encargada de cambiar formato de imagen.
Parámetros:
	imagen: imagen a la que se quiere cambiar el tamaño.
	nombre: nombre con el que se guardara la imagen redimensionada.
"""
def formato(imagen,nombre):
    imagen=cv2.resize(imagen,(1,1),interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("paginas\\static\\paginaP\\img\\"+nombre, imagen)
#***************************************************************************************************