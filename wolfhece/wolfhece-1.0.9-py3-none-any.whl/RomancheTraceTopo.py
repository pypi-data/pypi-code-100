import sys
from os import path
import json
import matplotlib.pyplot as plt
import numpy as np
from .wolf_array import WolfArray
from .PyVertexvectors import vector

mydir=path.normpath('D:\Programmation2\wolf_oo\Examples\Comparaison de traces topo après interpolation')
myfile='newtopo.bin.json'

ftopo=['G1_topo2017.bin','G1_interpGeom.bin','G1_smoothed2.bin']
topo=[]
for curtop in ftopo:
    topo.append(WolfArray(path.join(mydir,curtop)))

with open(path.join(mydir,myfile)) as json_file:
    data = json.load(json_file)

elev=np.zeros((3,len(data['skeleton']['curvi'])))

for k,(x,y) in enumerate(zip(data['skeleton']['x'],data['skeleton']['y'])):
    i,j = topo[0].get_ij_from_xy(x,y)
    for m in range(3):
        elev[m,k]=topo[m].array[i,j]

nbsect=data['nbsect']

label=['Lidar 2017','Interpolation','Lissage']
plt.figure(figsize=(10,5))
for m in range(3):
    plt.plot(data['skeleton']['curvi'],elev[m,:],label=label[m])

for k in range(1,nbsect+1):
    y=data['sect'+str(k)]['elevation']
    x=np.zeros(len(y))
    x[:]=data['sect'+str(k)]['curvi']
    if k==1:
        plt.scatter(x,y,marker='+',color='k',label='sections "géomètre"')
    else:
        plt.scatter(x,y,marker='+',color='k')

plt.xlabel('Distance curviligne depuis l\'amont [m]')
plt.ylabel('Altitude [m]')
plt.title('Comparaison des données altimétriques')
plt.legend()
plt.savefig(path.join(mydir,'fig.png'))

