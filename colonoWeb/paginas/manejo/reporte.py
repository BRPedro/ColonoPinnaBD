import pickle

"""
Clase reporte estructura de datos generales de la imagen.
"""


class Reporte:
    def __init__(self, altura, escala, ruido, proximidad, circulo, conteo):
        self.altura = altura
        self.escala = escala
        self.ruido = ruido
        self.proximidad = proximidad
        self.circulo = circulo
        self.conteo = conteo

    def insertar(self, altura, escala, ruido, proximidad, circulo, conteo):
        self.altura = altura
        self.escala = escala
        self.ruido = ruido
        self.proximidad = proximidad
        self.circulo = circulo
        self.conteo = conteo


def guardarReporte(reporte):
    fichero = file ( "paginas/static/paginaP/img/reporte.txt", "w" )
    nl = reporte
    pickle.dump ( nl, fichero )
    return nl


def cargarReporte():
    try:
        fichero = file ( "paginas/static/paginaP/img/reporte.txt" )
        r = pickle.load ( fichero )
        obj = Reporte ( r.altura, r.escala, r.ruido, r.proximidad, r.circulo, r.conteo )
        return obj
    except:
        n = Reporte ( 0, 0, 0, 0, 0, 0 )
        guardarReporte ( n )
        return n
