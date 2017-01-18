#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from osgeo import gdal

import tiempo as tie
import conexion as bd
import geoReferencia as Ref
import crearShapefile as shp

__author__ = "Pedro Barrantes R"
__date__ = "$11/10/2016 09:44:07 AM$"
"""
Clase encargada del conteo de imagines tiff.
"""


class ConteoGeo:
    """
    Constructor recibe el URL de la imegen.
    """

    def __init__(self, direccion, capacidad):
        self.dir = direccion  # Direccion de la fisica de la imagen.
        self.imagen = gdal.Open ( direccion )  # Se carga la imagen que se encuentra en la direccion dir.

        self.yTamanno = self.imagen.RasterYSize  # Dimensiones de la imagen.
        self.xTamanno = self.imagen.RasterXSize  # Dimensiones de la imagen.
        self.tamannoImagen = self.xTamanno * self.yTamanno  # Dimencion total de la imagen.
        self.yActual = 0  # Posicion de la fila por la que se esta analizando la imagen.
        self.xActual = 0  # Posicion de la columna por la que se esta analizando la imagen.

        self.centroides = []  # Lista de coordenadas de los centros de los patrones.
        self.contadorGeneral = 0  # Contador para verificar cantidad de pixel procesados por ciclos.
        self.contadorTotal = 0  # Contador para verificar cantidad de pixel en total.
        self.limitePixeles = capacidad  # Limite que puede soportar sin que de error de memoria.

        self.listapuntos = []

        self.fin = True

    # ****************************************************************************************************************************************************************************

    """
    Metodo con el cual se obtiene el valor del limitePixeles que es utilizado para
    corregir el desborde de memoria.
    Retrna:
        limitePixeles (float)
    """

    def getLimitePixeles(self):
        return self.limitePixeles

    """
    Metodo con el cual se actualisa el valor del limitePixeles que es utilizado para
    corregir el desborde de memoria.
    Parametros:
	    limitePixeles = Limite Pixeles(float)
    """

    def setLimitePixeles(self, limitePixeles):
        self.limitePixeles = limitePixeles

    """
    Metodo que busca los 8 vecinos mas cercanos de una coordenada (f,c)
    Recibe de parametros:
        f =  fila (int)
        c = columna (int)
        lista = lista de coordenadas ejemplo: [[2,3],[1,2], ...,[2,4]]
    Retorna True si tiene un vecino en la lista o Falso si no tiene vecino.
    """

    def busqueda(self, x, y, lista):
        if lista.count ( [x - 1, y - 1] ) > 0:
            return True
        if lista.count ( [x - 1, y] ) > 0:
            return True
        if lista.count ( [x - 1, y + 1] ) > 0:
            return True
        if lista.count ( [x, y + 1] ) > 0:
            return True
        if lista.count ( [x + 1, y + 1] ) > 0:
            return True
        if lista.count ( [x + 1, y] ) > 0:
            return True
        if lista.count ( [x + 1, y - 1] ) > 0:
            return True
        if lista.count ( [x, y - 1] ) > 0:
            return True
        return False

    # ****************************************************************************************************************************************************************************

    """
    Metodo para calcular la distancia de dos puntos (F, C)
    Parametros:
            coordenada1: lista de int ejemplo: [0, 0]
            coordenada2: lista de int ejemplo: [0, 1]
    Retorna:
            Resultado: float
    """

    def distaciaEntrePuntos(self, coordenada1, coordenada2):
        return abs ( (((coordenada2[0] - coordenada1[0]) ** 2) + ((coordenada2[1] - coordenada1[01]) ** 2)) ** 0.5 )

    # ****************************************************************************************************************************************************************************

    # ****************************************************************************************************************************************************************************

    """
    Método encargado de agrupar los pixeles verdes de una imagen en listas de patrones.
    Parametros:
        listapuntos: [[],[],..] lista con listas de las coordenadas de un pixel verde.
    Retorna:
        listapuntos con patrones agrupados.
    """

    def agrupamientoXvecinos(self, listapuntos):
        while True:
            inicio, siguiente = 0, 1
            bandera = True
            while siguiente < len ( listapuntos ):
                bandera2 = True
                for lis in listapuntos[inicio]:
                    if self.busqueda ( lis[0], lis[1], listapuntos[siguiente] ):
                        bandera2 = False
                        bandera = False
                        listapuntos[inicio] = listapuntos[inicio] + listapuntos[siguiente]
                        listapuntos.pop ( siguiente )
                        break
                if bandera2:
                    inicio += 1
                    siguiente += 1
            if bandera:
                break
        return listapuntos

    # ****************************************************************************************************************************************************************************

    """
    Método encargado de agrupar los pixeles verdes de una imagen en listas de patrones.
    Parametros:
        listapuntos: [[],[],..] lista con listas de las coordenadas de un pixel verde
        estado: int para controlar los hilos
    """

    def agrupamientoXvecinosFinal(self, listapuntos):
        while True:
            inicio, siguiente = 0, 1
            bandera = True
            while siguiente < len ( listapuntos ):
                bandera2 = True
                for lis in listapuntos[inicio]:
                    if self.busqueda ( lis[0], lis[1], listapuntos[siguiente] ):
                        bandera2 = False
                        bandera = False
                        listapuntos[inicio] = listapuntos[inicio] + listapuntos[siguiente]
                        listapuntos.pop ( siguiente )
                        break
                if bandera2:
                    inicio += 1
                    siguiente += 1
            if bandera:
                break
        return listapuntos

    # ****************************************************************************************************************************************************************************

    """
    Metodo secundario sin hilos que calcula las coordenadas centrales de un patrón.
    Parametros:
        listapuntos: [[[], []], [[]], ..] lista que contiene listas con las coordenadas de los parámetros.
        estado: int que cambia el estado de de la lista listaEstado, para identificar en que estado esta el hilo.
        limite: int límite mínimo aceptable de cantidad de pixeles de un patrón.
    """

    def centroidesBuscar(self, listapuntos):
        centroides = []
        for indice1 in listapuntos:
            minF, minC = self.yTamanno - 1, self.xTamanno - 1
            maxF, maxC = 0, 0
            for indice2 in indice1:
                if indice2[0] < minF:
                    minF = indice2[0]
                if indice2[0] > maxF:
                    maxF = indice2[0]
                if indice2[1] < minC:
                    minC = indice2[1]
                if indice2[1] > maxC:
                    maxC = indice2[1]
            centroides.append ( [((maxC - minC) / 2) + minC, ((maxF - minF) / 2) + minF, len ( indice1 )] )
        return centroides

    # ****************************************************************************************************************************************************************************

    """
    Método que inicia el conteo sobre la imagen.
    Parámetros:
        limitePatron: int valor mínimo que se acepta en cantidad de pixeles de un patrón.
        limiteCercania: float valor mínimo que se acepta de cercanía entre los parones.
        circulo: int tamaño de las marcas circulares.
    Retorno:
        [(int resultado conteo),(float tiempo de análisis)]
    """

    def inicioConteo(self, limitePatron, limiteCercania):
        return self.contadorAgrupado ( limitePatron, limiteCercania )

    # ****************************************************************************************************************************************************************************

    """
    Método que inicia el conteo sobre la imagen el cual se realiza ejecutando varios hilos.
    Parámetros:
        limitePatron: int valor mínimo que se acepta en cantidad de pixeles de un patrón.
        limiteCercania: float valor mínimo que se acepta de cercanía entre los parones.
        circulo: int tamaño de las marcas circulares.
    Retorno:
        [(int resultado conteo),(float tiempo de análisis)]
    """

    def contadorAgrupado(self, limitePatron, limiteCercania, nombreShp):
        baseD = bd.BDConexion ( 'BDAPTECH2', 'colono14', '1234' )
        baseD.reinicioBDs ( )
        baseD.desconectar ( )

        print "\t" + tie.hora ( )
        tiempo_inicial = time ( )
        print "\t" + str ( tiempo_inicial )
        ciclos = 1
        print "\t" + "Inicio de ciclos de particion de imagen"
        print "\tx:", self.xTamanno, "y:", self.yTamanno
        pinnas = 0
        while self.fin:
            print "\n\t\t", "*" * 30
            x, y = self.coordenadasFinales ( self.limitePixeles )
            self.listapuntos = []
            self.centroides = []
            print "\t\t" + "Inicio Ciclo: " + str ( ciclos ), "Tiempo: " + tie.hora ( )
            print "\t\t\tPaso 1 de 6"
            self.listapuntos = self.filtroVerde ( x, y )

            print "\t\t\tPaso 2 de 6", "Tiempo: " + tie.hora ( )
            self.listapuntos = self.agrupamientoXvecinos ( self.listapuntos )

            print "\t\t\tPaso 3 de 6", "Tiempo: " + tie.hora ( )
            self.listapuntos = self.centroidesBuscar ( self.listapuntos )

            print "\t\t\tPaso 4 de 6", "Tiempo: " + tie.hora ( )
            self.listapuntos = self.agrupamientoXproximidad ( self.listapuntos, limiteCercania )

            print "\t\t\tPaso 5 de 6", "Tiempo: " + tie.hora ( )
            print "\t\t\tPaso 5 de 6 insertando en BD", "Tiempo: " + tie.hora ( )
            baseD = bd.BDConexion ( 'BDAPTECH2', 'colono14', '1234' )
            baseD.insercionPatronSimpre ( self.listapuntos )
            baseD.desconectar ( )
            print "\t\t\tPaso 5 de 6 filtro ruido", "Tiempo: " + tie.hora ( )
            self.listapuntos = self.filtroRuido ( self.listapuntos, limitePatron )

            print "\t\t\tPaso 6 de 6", "Tiempo: " + tie.hora ( )
            print "\t\t\t" + str ( len ( self.listapuntos ) )
            self.listapuntos = Ref.CoordenadasGeo ( self.dir ).conversion_Pixel_Coordenadas ( self.listapuntos )
            pinnas += len ( self.listapuntos )
            shp.CrearShapefile ( "ciclo" + str ( ciclos ) + "_" + nombreShp, "archivoshp" ).crearmultipuntos (
                self.listapuntos )

            print "\t\t\tFIN...", "Tiempo: " + tie.hora ( )
            tiempo_final = time ( )
            print "\t\t\t" + str ( tiempo_final )
            tiempo_total = tiempo_final - tiempo_inicial
            tiempo_total /= 60.0
            print "\t\t\t" + str ( tiempo_total )

            print "\t\t" + "Fin Ciclo: " + str ( ciclos ), "Tiempo: " + tie.hora ( )

            self.xActual, self.yActual = x, y
            ciclos += 1

        baseD = bd.BDConexion ( 'BDAPTECH2', 'colono14', '1234' )
        baseD.filtrarPatrones ( limiteCercania )
        baseD.desconectar ( )

        baseD = bd.BDConexion ( 'BDAPTECH2', 'colono14', '1234' )
        baseD.filtrarRuido ( limitePatron )
        baseD.desconectar ( )

        baseD = bd.BDConexion ( 'BDAPTECH2', 'colono14', '1234' )
        self.listapuntos = baseD.listaCoordenadas ( )
        baseD.desconectar ( )

        self.listapuntos = Ref.CoordenadasGeo ( self.dir ).conversion_Pixel_Coordenadas ( self.listapuntos )
        shp.CrearShapefile ( "Total", "archivoshp" ).crearmultipuntos ( self.listapuntos )
        total = len ( self.listapuntos )

        baseD = bd.BDConexion ( 'BDAPTECH2', 'colono14', '1234' )
        baseD.reinicioBDs ( )
        baseD.desconectar ( )

        tiempo_final = time ( )

        tiempo_total = tiempo_final - tiempo_inicial
        tiempo_total /= 60.0
        print pinnas
        print  tie.hora ( )
        return ["Por ciclos: " + str ( pinnas ) + " Por BD: " + str ( total ), "{0:.2f}".format ( tiempo_total )]

    def filtroRuido(self, lista, limite):
        listaTem = []
        for indice in lista:
            if indice[2] > limite:
                listaTem.append ( indice )
        return listaTem

    # ****************************************************************************************************************************************************************************

    """
    Metodo que verifica los vecinos de los patrones y si existen patrones mas cercanos al limite minimo borra el patron con menor cantidad de coordenadas
    Parametros:
        listaGrupos: lista [][][]
        limite: int, limite de cercania
      Retorna:
        Int[][][]
    """

    def agrupamientoXproximidad(self, listaGrupos,
                                limiteD):  # Analizar si es mas exacto colocar la coordenada intermedia entre los 2 patrones.
        listaGrupos = sorted ( listaGrupos, key=lambda x: x[2], reverse=True )
        largo = len ( listaGrupos ) - 1
        indice = 0
        while indice < largo:
            indice2 = indice + 1
            while indice2 < largo + 1:
                resultado = self.distaciaEntrePuntos ( listaGrupos[indice], listaGrupos[indice2] )
                if resultado <= float ( limiteD ):
                    listaGrupos.pop ( indice2 )
                    largo -= 1
                else:
                    indice2 += 1
            indice += 1
        return listaGrupos

    # ****************************************************************************************************************************************************************************

    """"
    Metodo que filtra la imagen y crea una lista con todas las coordenadas que corresponde a una intensidad de verde mayor.
    Retorna:
        Lista con sublistas que contienen las coordenadas de los pixeles verdes.
    """

    def filtroVerde(self, x, y):
        self.contadorGeneral = 0  # Inicializa el contadorGeneral en 0 para no sobrepasar el limite de memoria.
        listapuntos = []  # Inicializa la listapuntos vacía para cargarla con las coordenadas que correspondas a pixeles verdes los elementos insertados en ella tendran la estructura [coordenada x, coordenada y]
        bandera = False # Bandera para salir de los ciclos internos.
        while self.yActual < self.yTamanno:  # Ciclo para recorrer las coordenadas y de la imagin no se debe reiniciar.
            while self.xActual < self.xTamanno:  # Ciclo para recorrer las coordenadas x de la imagen, se debe reiniciar al llegar al limite de largo de las coordenadas x de la imagen en caso de llegar al limite de memoria se debe quedar en la posición en la que va.
                rojo, verde, azul, infrarrojo = self.getPixelPosicion ( self.xActual, self.yActual )  # obtiene los valores del pixel por el cual se encuentra la posición del ciclo.
                if (rojo < verde) and (azul < verde):  # Evalua que el pixel corresponda a una intensidad de verde predominante en las bandas.
                    listapuntos.append ( [[self.yActual, self.xActual]] )  # Inserta la coordenada el pixel que cumplio la condicion en la estructura [x,y].
                self.xActual += 1  # Aumenta la posicion de x.
                if self.xActual >= x + 1 and self.yActual >= y + 1: # Verifica que no esté en la posición de la coordenada final permitida para el ciclo.
                    if self.xActual >= self.xTamanno and self.yActual >= self.yTamanno: # Verifica que el ciclo este en el final de la imagen.
                        self.fin = False # Si está en el final cambia la bandera global a False para terminar el ciclo principal de análisis.
                    bandera = True # Si está en el límite permitido por el ciclo actual cambia la bandera local por True.
                    break # Se sale del ciclo actual.
            if bandera:
                break
            self.yActual += 1 # Aumenta en 1 la posición actual de y.
            if self.xActual >= self.xTamanno and self.yActual >= self.yTamanno:  # Verifica que el ciclo este en el final de la imagen.
                self.fin = False # Si está en el final cambia la bandera global a False para terminar el ciclo principal de análisis.
            self.xActual = 0 # # Reinicia la posición del x actual en 0.
        return listapuntos # Retorna la lista con las coordenadas de los pixeles con intensidad de verde mayor a las otras bandas.

    # ****************************************************************************************************************************************************************************


    """
    Método que para obtener el los valores rojo, verde, azul e infrarrojo de un pixel con las coordenadas pasadas por parámetros.
    Parámetros:
        fila: int posición de la fila del pixel a buscar.
        columna: int posición de la fila del pixel a buscar.
    Retorna:
        int valor rojo, int valor verde, int azul
    """

    def getPixelPosicion(self, x, y):
        try:
            pixel = self.imagen.ReadAsArray ( x, y, 1,
                                              1 )  # Obtención de la información de pixel en la ubicación (x, y).
            r = pixel[0][0][0]  # Valor rojo.
            g = pixel[1][0][0]  # Valor verde.
            b = pixel[2][0][0]  # Valor azul.
            i = 0  # pixel[3][0][0]# Valor infrarrojo.
        except:
            return 0, 0, 0, 0  # En caso de error retorna valores en 0.
        return r, g, b, i  # retorno de los valores numericos de las bandas.

    # ****************************************************************************************************************************************************************************

    """
    Método que calcula el punto máximo en coordenadas x, y que se puede procesar en el barrido.
    Parámetros:
         Distancia: int que representa la cantidad de pixeles que se pueden analizar.
    Retorna x,y que son el int del pinto máximo a recorrer.
    """

    def coordenadasFinales(self, distancia, xInicial, yInicial):
        x = xInicial  # Posición actual de x para el recorrido en la imagen.
        y =  yInicial  # Posición actual de y para el recorrido en la imagen.
        distancia//=4
        lista=[]
        if distancia <= 0: # Verifica que la distancio no esté en 0.
            return [[[x, y],[x, y]]] # En caso de estar en 0 retorna en punto máximo (coordenadas finales de la imagen) de la imagen.
        for i in range(4):
            contador = 0 # Contador con para verificar cuanto a que avanzar en las coordenadas.
            bandera=False
            while y < self.yTamanno: # Para avanzar en el eje y de la imagen sin sobrepasar el final.
                while x < self.xTamanno: # Para avanzar en el eje y de la imagen sin sobrepasar el final.
                    if contador >= distancia: # Verifica que el contador sea mayor o igual a la distancia.
                        lista.append([[xInicial, yInicial],[x, y ]])# En caso de ser el contador sea mayor o igual a la distancia retorna la posición por la que los ciclos estén.
                        bandera=True
                        break
                    contador += 1 # Aumenta el contador más 1
                    x += 1 # Aumenta x más 1
                if bandera:
                    break
                x = 0 # Reinicia x en 0.
                y += 1 # Aumenta y más 1
            return self.xTamanno - 1, self.yTamanno - 1 # En caso de llegar al final de la imagen se retorna la coordenada del ultimo pixel.


# ______________________________________________________________________________________________________________________________________________________________________________

prue = ConteoGeo ( 'C:\\Users\\aariasr\\Pictures\\tif_redu\\exom- seccion 2 completa_transparent_mosaic_group1.tif', 50000000 )
print prue.xTamanno, prue.yTamanno

print prue.contadorAgrupado ( 6, 55.5, "prue" )
