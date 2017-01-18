import pickle
class Configuracion:
    def __init__(self,altura,escala,ruido,proximidad,circulo):
        self.altura=altura
        self.escala=escala
        self.ruido=ruido
        self.proximidad=proximidad
        self.circulo=circulo

    def imp(self):
        print self.ruido,self.proximidad,self.altura,self.altura,self.circulo,self.escala


def cargar():
    try:
        fichero=file('paginas\static\paginaP\conf\configuracion.txt')
        r=pickle.load(fichero)
        obj=Configuracion(r.altura,r.escala,r.ruido,r.proximidad,r.circulo)
        return obj
    except:
        guardar(15,0.5,2,20,10)
        return Configuracion(15,0.5,2,20,10)

def guardar(altura,escala,ruido,proximidad,circulo):
    fichero=file('paginas\static\paginaP\conf\configuracion.txt','w')
    nl=Configuracion(altura,escala,ruido,proximidad,circulo)
    pickle.dump(nl,fichero)
    return nl

def predeterminado():
    return guardar(15,0.5,2,20,10)
