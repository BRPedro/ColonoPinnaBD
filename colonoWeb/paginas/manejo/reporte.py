import pickle

"""
Clase reporte estructura de datos generales de la imagen.
"""


class Reporte:
    def __init__(self, escala,ruido,proximidad,capacidad, conteo):
        self.escala = escala
        self.ruido = ruido
        self.proximidad = proximidad
        self.capacidad = capacidad
        self.conteo = conteo

    def insertar(self, escala,ruido,proximidad,capacidad, conteo):
        self.escala = escala
        self.ruido = ruido
        self.proximidad = proximidad
        self.capacidad = capacidad
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
        obj = Reporte ( r.escala, r.ruido, r.proximidad, r.capacidad, r.conteo )
        return obj
    except:
        n = Reporte ( 0, 0, 0, 0, 0 )
        guardarReporte ( n )
        return n
