from osgeo import gdal
from osgeo import ogr
class CrearShapefile:
    def __init__(self,nombre,dir):
        driverName = "ESRI Shapefile"
        drv = gdal.GetDriverByName(driverName)
        self.ds = drv.Create(dir+"\\"+nombre+".shp", 0, 0, 0, gdal.GDT_Unknown)
        self.lyr = self.ds.CreateLayer(nombre, None, ogr.wkbPoint)
        field_defn = ogr.FieldDefn("Name", ogr.OFTString)
        field_defn.SetWidth(32)
        self.lyr.CreateField(field_defn)

    def crearmultipuntos(self,lista):
        feat = ogr.Feature(self.lyr.GetLayerDefn())
        name = "planta"
        feat.SetField("Name", name)
        for indice in lista:
            wkt = "POINT(%f %f)" % (indice[0], indice[1])
            point = ogr.CreateGeometryFromWkt(wkt)
            feat.SetGeometry(point)
            self.lyr.CreateFeature(feat)

        feat.Destroy()

        self.ds = None