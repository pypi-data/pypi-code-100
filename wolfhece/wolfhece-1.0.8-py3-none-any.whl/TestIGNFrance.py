import pyproj
from .PyWMS import getIGNFrance

#'EPSG:27573' Lambert III
#'EPSG:4326' WGS84
epsg27573=pyproj.CRS.from_epsg(27573)
epsg4326=pyproj.CRS.from_epsg(4326)
print(epsg27573)
print(epsg4326)
transf=pyproj.Transformer.from_crs(27573,4326)
y1,x1=transf.transform(876875.60,3311362.70)
y2,x2=transf.transform(886007.10,3319768.25)
for pt in transf.itransform([(800000,300000),(900000,400000)]):
    print(pt)
getIGNFrance('OI.OrthoimageCoverage.HR','EPSG:4326',x1,y1,x2,y2,1000,1000)