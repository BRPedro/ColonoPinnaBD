import gdal
import osr
"""
Clase con la que se obtiene las coordenadas geograficas de los
pixeles de una imagen o los pixeles que corresponde de una
coordenada geografica.
"""
class CoordenadasGeo:
    def __init__(self,dir):
        self.g = gdal.Open(dir)
        self.proj = osr.SpatialReference()
        self.proj.ImportFromWkt(self.g.GetProjection())
        self.latlong = self.proj.CloneGeogCS()
        self.transform = osr.CoordinateTransformation(self.proj, self.latlong)
        self.geoT = self.g.GetGeoTransform()

    """
    Metodo el cual recibe la posicion de un
    pixel (fila y columna) y retorna las coordenadas geograficas.
    """
    def PixelCoordToGeocoord(self,x,y):
        px = self.geoT[0]
        py = self.geoT[3]
        px += self.geoT[1] * x + self.geoT[2] * y
        py += self.geoT[4] * x + self.geoT[5] * y
        return px, py

    """
    Metodo que revive las coordenadas geograficas
    y retorna la posicion del pixel de la imagen.
    """
    def GeocoordToPixelCoord(self,px,py):
        s = px - self.geoT[0]
        t = py - self.geoT[3]
        det = self.geoT[1] * self.geoT[5] - self.geoT[2] * self.geoT[4]
        x = (s * self.geoT[5] - self.geoT[2] * t) / det
        y = (t * self.geoT[1] - self.geoT[4] * s) / det
        return int(x), int(y)
    """
    Metodo que recibe una lista con las posiciones de pixeles
    y retorna una lista con la posicion geograficas de los pixeles.
    """
    def conversion_Pixel_Coordenadas(self,lista):
        largo =len(lista)
        indice=0
        while indice<largo:
            lista[indice][0],lista[indice][1]=self.PixelCoordToGeocoord(lista[indice][0],lista[indice][1])
            indice+=1
        return lista


