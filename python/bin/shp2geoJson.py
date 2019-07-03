import shapefile
import os
import json
from json import dumps
import datetime
import utm
import geopandas


inputFilename = os.getcwd() + "/E501_Basemap.shp"
outputGeoJSON = "E501_Basemap.js"

def hasShp( name ):
     if (( name.find(".shp") > -1 )):
        positionShp = name.find(".shp")
        lenShp = len(name)
        if (lenShp == positionShp + 4):
                return name

def flatten_gdf_geometry(gdf, geom_type):
    geometry = gdf.geometry
    flattened_geometry = []
    flattened_gdf = geopandas.GeoDataFrame()
    for geom in geometry:
        print (geom.type)
        if geom.type in ['GeometryCollection', 'MultiPoint', 'MultiLineString', 'MultiPolygon']:
            for subgeom in geom:
                #print(subgeom.type)
                #if subgeom.type==geom_type:
                flattened_geometry.append(subgeom)
        else:
            #if geom.type==geom_type:
            flattened_geometry.append(geom)
    flattened_gdf.geometry=flattened_geometry
    return flattened_gdf

def shp2geoJS(inputFilename, outputGeoJSON):
        shp = geopandas.read_file(inputFilename)
        shp = shp.to_crs(epsg=4326)
        print (shp.head())
        #fig, ax = plt.subplots()
        #shp.plot(ax = ax)
        #fig.show()
        flat1 = flatten_gdf_geometry (shp, 'LineString')
        flat1.to_file(outputGeoJSON, driver="GeoJSON")

# lists the files in current directory and retains the *.shp ones.
shpList = list (map(hasShp, os.listdir()))
while (None in shpList):
        shpList.remove(None)

# goes by all the *.shp files one by one and transforms them into js files so they be consumed by MapBox.
for file in shpList:
        print ("processing the file called " + file )
        shp2geoJS(file, file+'.js')
