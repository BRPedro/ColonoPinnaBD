import pickle
class Configuracion:
    def __init__(self,escala,ruido,proximidad,capacidad):
        self.escala=escala
        self.ruido=ruido
        self.proximidad=proximidad
        self.capacidad=capacidad

def cargar():
    try:
        fichero=file('paginas\static\paginaP\conf\configuracion.txt')
        r=pickle.load(fichero)
        obj=Configuracion(r.escala, r.ruido, r.proximidad,r.capacidad)
        return obj
    except:
        guardar(0.3,6,54.5,50000000)
        return Configuracion(0.3,6,54.5,50000000)

def guardar(escala,ruido,proximidad,capacidad):
    fichero=file('paginas\static\paginaP\conf\configuracion.txt','w')
    nl=Configuracion(escala,ruido,proximidad,capacidad)
    pickle.dump(nl,fichero)
    return nl

def predeterminado():
    return guardar(0.3,6,54.5,50000000)
