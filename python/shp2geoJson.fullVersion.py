import shapefile
import os
import json
from json import dumps
import datetime
import utm


filename = os.getcwd() + "/data/Circuit/E501_Basemap.shp"


shp = gdp.read_file(filename)
shp = shp.to_crs(epsg=4326)
shp.head()
fig, ax = plt.subplots()
shp.plot(ax = ax)
fig.show()
flat1 = flatten_gdf_geometry (borough, 'LineString')
flat1.to_file("circPandas.geojson", driver="GeoJSON")
borough.to_file("circPandas.geojson", driver="GeoJSON")

filename2 = '/Users/habib13inch/Documents/13/code/python/Exelon/circPandas.geojson/circPandas.shp'
re = gdp.read_file(filename2)
re.to_file("re.geojson", driver="GeoJSON")









def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

filename = os.getcwd() + "/data/Circuit/E501_Basemap.shp"
# read the shapefile
reader = shapefile.Reader(filename)
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
#reader.encoding = "latin1"
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    for i in range(len (geom['coordinates'])):
            for pair in geom['coordinates'][i]:
                    longLat = 
                    print (pair)
    toto = geom['coordinates']
    print (geom['coordinates'])
    print ("------------------------------------------------------------------------------------------------------------------------------------------- \n\n/n/n")
    buffer.append(dict(type="Feature", geometry=geom, properties=atr)) 

#print ("buffer = ", buffer )

# write the GeoJSON file

geojson = open("circJunk.json", "w")
#dmps = dumps(buffer,sort_keys=True, indent=1, default=default )
geojson.write(dumps({"type": "FeatureCollection", "features": buffer }, sort_keys=True, indent=2, default=default) + "\n")
geojson.close()

import geopandas as gdp 

def flatten_gdf_geometry(gdf, geom_type):
    geometry = gdf.geometry
    flattened_geometry = []
    flattened_gdf = gdp.GeoDataFrame()
    for geom in geometry:
        if geom.type in ['GeometryCollection', 'MultiPoint', 'MultiLineString', 'MultiPolygon']:
            for subgeom in geom:
                print(subgeom.type)
                if subgeom.type==geom_type:
                    flattened_geometry.append(subgeom)
        else:
            if geom.type==geom_type:
                flattened_geometry.append(geom)
    flattened_gdf.geometry=flattened_geometry
    return flattened_gdf



