import numpy as np
from delaunay2D import Delaunay2D
import os
import math as m 


minLong = -88.3
maxLong = -88.2

minLat = 42.1
maxLat = 42.2

numPts = 3900

# Create a random set of 2D points around longlat -88.3 and 42.1 with random heights for a heat map, with a Delauney triangulation
longitude =    minLong +  ((maxLong - minLong) * np.random.random((numPts)))
latittude =    minLat +  ((maxLat - minLat) * np.random.random((numPts)))
height = [] #2550 * np.random.random(numPts)

for i in range (numPts):
    x = longitude[i]
    y = latittude[i]
    sin = 8* m.sin((x-minLong)*31.4) # values bewteeen 0 and 10 across the longitude
    h =  25500 *  ( ( m.exp  (sin ) - 1 )  / (m.exp(8) - 1) )
    if ((x-minLong) < 0.02):
        sin = m.fabs ( m.sin((y-minLat)*31.4*2) ) # values bewteeen 0 and 10 across the longitude
        h =  25500 *  sin / 20
    height.append(h)


r =   range(255)
g =   []
b = []
for i in range (255):
    g.append(0)
    b.append(254-i)



b =   (255 * np.random.random(numPts))

lo = longitude.tolist()
la =  latittude.tolist()

longLat = []
for i in range (len(lo)):
    longLat.append([ lo[i], la[i] ])

longLat = np.array(longLat)

# Create delaunay Triangulation
dt = Delaunay2D()
for s in longLat:
    dt.addPoint(s)

# indices of triangles 
indices = dt.exportTriangles()



filename = os.getcwd() + "/heatmap.js"
file = open (filename, 'w')

filename0 = os.getcwd() + "/heatmap0.js"
file0 = open (filename0, 'w')

file.write ( 'export const E501_Basemap = { "type": "FeatureCollection", "features": [  \n '   )
file0.write ( 'export const E501_Basemap = { "type": "FeatureCollection", "features": [  \n '   )


for idx in range (len(indices)):
    idx0 = indices[idx][0]  # we do -1 becuase indices are start with 1 for the 0 index
    idx1 = indices[idx][1]  
    idx2 = indices[idx][2] 
    colorIdx = int (height[idx2] / 100)
    print (colorIdx)
    file.write (' { "type": "Feature", "properties": { "level": 1, "height": ' + str (height[idx2])  + ', "base_height":' + str (height[idx2] - 10 ) + ', "color":[' + str(int (r[colorIdx])) + ',' + str(int (g[colorIdx] )) + ',' + str(int (b[colorIdx]) )+ '] }, "geometry": { "type": "Polygon", "coordinates": ' )
    file.write ('[[['+ str (lo[idx0]) + ',' + str(la[idx0]) + '],['+str (lo[idx1]) + ',' + str(la[idx1]) + '],[' + str(lo[idx2]) + ',' + str (la[idx2]) + ']]] } }, \n' )
    file0.write (' { "type": "Feature", "properties": { "level": 1, "height": 0.1, "base_height":0 , "color":[' + str(int (r[colorIdx])) + ',' + str(int (g[colorIdx] )) + ',' + str(int (b[colorIdx]) )+ '] }, "geometry": { "type": "Polygon", "coordinates": ' )
    file0.write ('[[['+ str (lo[idx0]) + ',' + str(la[idx0]) + '],['+str (lo[idx1]) + ',' + str(la[idx1]) + '],[' + str(lo[idx2]) + ',' + str (la[idx2]) + ']]] } }, \n' )


file.write ('\n ]}')
file.close()

file0.write ('\n ]}')
file0.close()





"""
Demostration of how to plot the data.
"""
import matplotlib.pyplot as plt
import matplotlib.tri
import matplotlib.collections



# Create a plot with matplotlib.pyplot
fig, ax = plt.subplots()
ax.margins(0.1)
ax.set_aspect('equal')
plt.axis([minLong, maxLong, minLat, maxLat])

# Plot our Delaunay triangulation (plot in blue)
cx, cy = zip(*longLat)
dt_tris = dt.exportTriangles()
ax.triplot(matplotlib.tri.Triangulation(cx, cy, dt_tris), 'bo--')

# Plot annotated Delaunay vertex (seeds)
"""
for i, v in enumerate(seeds):
    plt.annotate(i, xy=v)
"""
    
# DEBUG: Use matplotlib to create a Delaunay triangulation (plot in green)
# DEBUG: It should be equal to our result in dt_tris (plot in blue)
# DEBUG: If boundary is diferent, try to increase the value of your margin
# ax.triplot(matplotlib.tri.Triangulation(*zip(*seeds)), 'g--')

# DEBUG: plot the extended triangulation (plot in red)
# edt_coords, edt_tris = dt.exportExtendedDT()
# edt_x, edt_y = zip(*edt_coords)
# ax.triplot(matplotlib.tri.Triangulation(edt_x, edt_y, edt_tris), 'ro-.')

# Plot the circumcircles (circles in black)
"""
for c, r in dt.exportCircles():
    ax.add_artist(plt.Circle(c, r, color='k', fill=False, ls='dotted'))
"""

# Build Voronoi diagram as a list of coordinates and regions
vc, vr = dt.exportVoronoiRegions()

# Plot annotated voronoi vertex
"""
plt.scatter([v[0] for v in vc], [v[1] for v in vc], marker='.')
for i, v in enumerate(vc):
    plt.annotate(i, xy=v)
"""

# Plot annotated voronoi regions as filled polygons
"""
for r in vr:
    polygon = [vc[i] for i in vr[r]]     # Build polygon for each region
    plt.fill(*zip(*polygon), alpha=0.2)  # Plot filled polygon
    plt.annotate("r%d" % r, xy=np.average(polygon, axis=0))
"""

# Plot voronoi diagram edges (in red)
for r in vr:
    polygon = [vc[i] for i in vr[r]]       # Build polygon for each region
    plt.plot(*zip(*polygon), color="red")  # Plot polygon edges in red

# Dump plot to file
# plt.savefig('output-delaunay2D.png', dpi=96)
# plt.savefig('output-delaunay2D.svg', dpi=96)

plt.show()