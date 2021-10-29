import os
from scipy.interpolate import interpolate

from .PyVertex import wolfvertex
from .wolf_array import *
from .PyCrosssections import crosssections

listdem=['dem1','dem2','dem10m','dem20m','cs']

class node_watershed:
    i:int
    j:int
    index:int

    dem:dict    
    demcorr:float

    mycs:list = None

    time:float
    slope:float
    sloped8:float
    slopecorr:dict

    river:bool
    reach:int
    sub:int
    forced:bool
    uparea:float

    strahler:int
    reachlevel:int
    
    cums:float
    incrs:float

    down=None
    up:list
    upriver:list

    flatindex:int = -1

    def incr_curvi(self):
        if self.down is None:
            self.cums=0.
        else:
            self.cums = self.down.cums+self.incrs
        
        #for curup in self.upriver:
        #    curup.incr_curvi()
        for curup in self.up:
            curup.incr_curvi()

    def mean_slope_up(self,threshold):
        curnode: node_watershed
        meanslope=0.
        nbmean=0
        for curnode in self.up:
            if curnode.slope>threshold:
                nbmean+=1.
                meanslope+=curnode.slope
        if nbmean>0:
            meanslope=meanslope/nbmean

        return meanslope

    def slope_down(self,threshold):
        slopedown=0.
        curnode=self
        while curnode.slope < threshold:
            if curnode.down is None:
                break
            curnode=curnode.down

        slopedown = curnode.slope
        return slopedown

    def slope_upriver(self,threshold):
        slopeup=0.

        if self.slope<threshold:
            if len(self.upriver)>0:
                slopeup=self.upriver[0].slope_upriver(threshold)
            else:
                slopeup=-1.
        else:
            slopeup = self.slope

        return slopeup

class riversystem:
    nbreaches:int
    myreaches:dict
    
    myupmin:dict
    
    myslopes:dict
    parent=None
    myupstreams:dict 
    
    maxlevels:int
    maxstrahler:int

    tslope:float =None
    tz:float =None


    def __init__(self,rivers:list,parent,thresholdz=None,thresholdslope=None, *args, **kwargs):
        curnode:node_watershed

        self.parent=parent
        self.nbreaches = max([x.reach for x in rivers])
        self.myreaches={}
        self.myreaches['reaches']={}
        self.myupstreams={}
        self.myupstreams['list']=[]

        for curreach in range(1,self.nbreaches+1):
            curup:node_watershed
            listreach,curup=parent.find_rivers(whichreach=curreach)

            if len(curup.upriver)==0:
                self.myupstreams['list'].append(curup)

            self.myreaches['reaches'][curreach]={}
            curdict=self.myreaches['reaches'][curreach]
            curdict['upstream']=curup
            curdict['baselist']=listreach
            
        self.create_index()
        if not thresholdz is None:
            self.tz=thresholdz
        elif not thresholdslope is None:
            self.tslope=thresholdslope

        self.selectmin()

        return super().__init__(*args, **kwargs)

    def get_x(self,whichreach=None,whichup=None):
        if not whichreach is None:
            nodeslist=self.myreaches['reaches'][whichreach]['baselist']
            x=list(curnode.cums for curnode in nodeslist)
        elif not whichup is None:
            curnode:node_watershed
            x=[]
            curnode=self.myupstreams['list'][whichup]
            while not curnode is None:
                x.append(curnode.cums)
                curnode=curnode.down
        else:
            x=[]

        return x

    def get_dem(self,whichdem,whichreach=None,whichup=None):
        if not whichreach is None:
            nodeslist=self.myreaches['reaches'][whichreach]['baselist']
            dem=list(curnode.dem[whichdem] for curnode in nodeslist)
        elif not whichup is None:
            curnode:node_watershed
            dem=[]
            curnode=self.myupstreams['list'][whichup]
            while not curnode is None:
                dem.append(curnode.dem[whichdem])
                curnode=curnode.down
        return dem

    def get_dem_corr(self,whichdem,whichreach=None,whichup=None):
        if not whichreach is None:
            nodeslist=self.myreaches['reaches'][whichreach]['baselist']
            dem=list(curnode.demcorr[whichdem] for curnode in nodeslist)
        elif not whichup is None:
            curnode:node_watershed
            dem=[]
            curnode=self.myupstreams['list'][whichup]
            while not curnode is None:
                dem.append(curnode.dem[whichdem])
                curnode=curnode.down
        return dem

    def get_slope(self,whichslope=None,whichreach=None,whichup=None):
        if whichslope is None:
            if not whichreach is None:
                nodeslist=self.myreaches['reaches'][whichreach]['baselist']
                slope=list(curnode.slope for curnode in nodeslist)
            elif not whichup is None:
                curnode:node_watershed
                slope=[]
                curnode=self.myupstreams['list'][whichup]
                while not curnode is None:
                    slope.append(curnode.slope)
                    curnode=curnode.down
        else:        
            if not whichreach is None:
                nodeslist=self.myreaches['reaches'][whichreach]['baselist']
                slope=list(curnode.slopecorr[whichslope]['value'] for curnode in nodeslist)
            elif not whichup is None:
                curnode:node_watershed
                slope=[]
                curnode=self.myupstreams['list'][whichup]
                while not curnode is None:
                    slope.append(curnode.slopecorr[whichslope]['value'])
                    curnode=curnode.down
        
        return slope

    def create_index(self):
        #incrément d'index depuis l'amont jusque l'exutoire final
        for curup in self.myupstreams['list']:
            curnode:node_watershed
            curnode=curup
            while not curnode is None:
                curnode.reachlevel +=1
                curnode=curnode.down

        #recherche de l'index max --> à l'exutoire
        self.maxlevels = self.parent.myoutlet.reachlevel
        self.maxstrahler=0
        self.myreaches['indexed']={}
        for i in range(1,self.maxlevels+1):
            self.myreaches['indexed'][i]=[]

        #création de listes pour chaque niveau
        for curreach in self.myreaches['reaches']:
            curdict=self.myreaches['reaches'][curreach]
            listreach=curdict['baselist']                       
            curlevel=listreach[0].reachlevel
            self.myreaches['indexed'][curlevel].append(curreach)

        #création de listes pour chaque amont
        #  on parcourt toutes les mailles depuis chaque amont et on ajoute les index de biefs qui sont différents
        for idx,curup in enumerate(self.myupstreams['list']):
            curdict=self.myupstreams[idx]={}
            curdict['up']=curup
            curdict['fromuptodown']=[]
            curdict['fromuptodown'].append(curup.reach)
            curnode=curup.down
            while not curnode is None:
                if curnode.reach!=curdict['fromuptodown'][-1]:
                    curdict['fromuptodown'].append(curnode.reach)
                curnode=curnode.down

        #création de l'indice de strahler
        self.myreaches['strahler']={}
        #on commence par ajouter les biefs de 1er niveau qui sont à coup sûr d'indice 1
        self.myreaches['strahler'][1]=self.myreaches['indexed'][1]
        for curreach in self.myreaches['strahler'][1]:
            self.set_strahler_in_nodes(curreach,1)

        #on parcourt les différents niveaux
        for i in range(2,self.maxlevels+1):
            listlevel=self.myreaches['indexed'][i]
            for curreach in listlevel:
                curup:node_watershed
                curup=self.myreaches['reaches'][curreach]['upstream']
                upidx=list(x.strahler for x in curup.upriver)
                sameidx=upidx[0]==upidx[-1]
                maxidx=max(upidx)

                curidx=maxidx
                if sameidx:
                    curidx+=1
                    if not curidx in self.myreaches['strahler'].keys():
                         #création de la liste du niveau supérieur
                         self.myreaches['strahler'][curidx]=[]
                         self.maxstrahler=curidx
                    
                self.myreaches['strahler'][curidx].append(curreach)
                self.set_strahler_in_nodes(curreach,curidx)


        myarray=WolfArray(mold=self.parent.subs)
        myarray.reset()
        curnode:node_watershed
        for curreach in self.myreaches['reaches']:
            curdict=self.myreaches['reaches'][curreach]
            listreach=curdict['baselist']
            for curnode in listreach:
                i=curnode.i
                j=curnode.j
                myarray.array[i,j]=curnode.strahler
        myarray.filename = self.parent.mydir+'\\Characteristic_maps\\Drainage_basin.strahler'
        myarray.write_all()
        myarray.reset()
        for curreach in self.myreaches['reaches']:
            curdict=self.myreaches['reaches'][curreach]
            listreach=curdict['baselist']
            for curnode in listreach:
                i=curnode.i
                j=curnode.j
                myarray.array[i,j]=curnode.reachlevel
        myarray.filename = self.parent.mydir+'\\Characteristic_maps\\Drainage_basin.reachlevel'
        myarray.write_all()
                 
    def set_strahler_in_nodes(self,whichreach,strahler):
        listnodes = self.myreaches['reaches'][whichreach]['baselist']
        curnode:node_watershed
        for curnode in listnodes:
            curnode.strahler = strahler

    def plot_dem(self,which=-1):
        mymarkers=['x','+','1','2','3','4']
        if which==-1:
            plt.figure()
            for curreach in self.myreaches['reaches']:
                x=np.array(self.get_x(whichreach=curreach))
                for idx,curdem in enumerate(listdem):
                    y=np.array(self.get_dem(curdem,whichreach=curreach))

                    xmask=np.ma.masked_where(y==99999.,x)
                    ymask=np.ma.masked_where(y==99999.,y)

                    plt.scatter(xmask,ymask,marker=mymarkers[idx],label=curdem)
            plt.legend()            
        elif which==-99:
            size=int(np.ceil(np.sqrt(self.nbreaches)))
            fig,ax=plt.subplots(size,size)
            for index,curreach in enumerate(self.myreaches['reaches']):
                curax=ax[int(np.floor(index/size)),int(np.mod(index,size))]

                curdict=self.myreaches['reaches'][curreach]
                x=np.array(self.get_x(whichreach=curreach))

                for idx,curdem in enumerate(listdem):
                    y=np.array(self.get_dem(curdem,whichreach=curreach))

                    xmask=np.ma.masked_where(y==99999.,x)
                    ymask=np.ma.masked_where(y==99999.,y)

                    curax.scatter(xmask,ymask,marker=mymarkers[idx],label=curdem)
            curax.legend()
        elif which==-98:
            size=int(np.ceil(np.sqrt(len(self.myupstreams['list']))))
            fig,ax=plt.subplots(size,size)
            for idxup,curup in enumerate(self.myupstreams['list']):
                curax=ax[int(np.floor(idxup/size)),int(np.mod(idxup,size))]
                x=np.array(self.get_x(whichup=idxup))

                for idx,curdem in enumerate(listdem):
                    y=np.array(self.get_dem(curdem,whichup=idxup))
                    
                    xmask=np.ma.masked_where(y==99999.,x)
                    ymask=np.ma.masked_where(y==99999.,y)
                    curax.scatter(xmask,ymask,marker=mymarkers[idx],label=curdem)
                
            curax.legend()
        elif which>-1:
            if which<len(self.myupstreams['list']):
                fig=plt.figure()
                fig.suptitle('Upstream n°'+str(which))               
                
                x=np.array(self.get_x(whichup=which))
                for idx,curdem in enumerate(listdem):
                    y=np.array(self.get_dem(curdem,whichup=which))
                    
                    xmask=np.ma.masked_where(y==99999.,x)
                    ymask=np.ma.masked_where(y==99999.,y)
                    plt.scatter(xmask,ymask,marker=mymarkers[idx],label=curdem)
                
            plt.legend()
        plt.show()

    def plot_dem_and_corr(self,which=-1,whichdem='dem2'):
        if which<len(self.myupstreams['list']):
            fig=plt.figure()
            fig.suptitle('Upstream n°'+str(which))               
            
            x=np.array(self.get_x(whichup=which))
            y=np.array(self.get_dem(whichdem,whichup=which))
            
            xcorr=self.myupmin[which][whichdem][0]
            ycorr=self.myupmin[which][whichdem][1]
            
            xmask=np.ma.masked_where(y==99999.,x)
            ymask=np.ma.masked_where(y==99999.,y)

            plt.scatter(xmask,ymask,marker='x',label=whichdem)
            plt.scatter(xcorr,ycorr,marker='+',label='selected points')
            
            plt.legend()
            plt.savefig(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\Simulations\Hydrologie\Up'+str(which)+'_'+whichdem+'.png')
            #plt.show()

    def plot_slope(self,which=-1):
        mymarkers=['x','+','1','2','3','4']
        if which==-1:
            plt.figure()
            for curreach in self.myreaches['reaches']:
                x=self.get_x(whichreach=curreach)
                for idx,curdem in enumerate(listdem):
                    y=self.get_slope(curdem,whichreach=curreach)
                    plt.scatter(x,y,marker=mymarkers[idx],label=curdem)
            plt.legend()
            plt.show()
        elif which==-99:
            size=int(np.ceil(np.sqrt(self.nbreaches)))
            fig,ax=plt.subplots(size,size)
            for index,curreach in enumerate(self.myreaches['reaches']):
                curax=ax[int(np.floor(index/size)),int(np.mod(index,size))]

                x=self.get_x(whichreach=curreach)

                for idx,curdem in enumerate(listdem):
                    y=self.get_slope(curdem,whichreach=curreach)
                    curax.scatter(x,y,marker=mymarkers[idx],label=curdem)
            curax.legend()
            plt.show()
        elif which==-98:
            size=int(np.ceil(np.sqrt(len(self.myupstreams['list']))))
            fig,ax=plt.subplots(size,size)
            for idxup,curup in enumerate(self.myupstreams['list']):
                curax=ax[int(np.floor(idxup/size)),int(np.mod(idxup,size))]
                x=self.get_x(whichup=idxup)

                for idx,curdem in enumerate(listdem):
                    y=self.get_slope(curdem,whichup=idxup)
                    curax.scatter(x,y,marker=mymarkers[idx],label=curdem)
            curax.legend()
            plt.show()
    
    def write_slopes(self):
        #Uniquement les pentes rivières
        for curlist in listdem:
            slopes= WolfArray(self.parent.mydir+'\\Characteristic_maps\\Drainage_basin.slope')
            slopes.reset()
            for curreach in self.myreaches['reaches']:
                curdict=self.myreaches['reaches'][curreach]
                listreach=curdict['baselist']

                curnode:node_watershed
                for curnode in listreach:
                    i=curnode.i
                    j=curnode.j
                    slopes.array[i,j]=curnode.slopecorr[curlist]['value']

            slopes.filename = self.parent.mydir+'\\Characteristic_maps\\Drainage_basin.slope_corr_riv_'+curlist
            slopes.write_all()

    def selectmin(self):
        #Sélection des valeurs minimales afin de conserver une topo décroissante vers l'aval --> une pente positive
        self.myupmin={}
        
        #on initialise le dictionnaire de topo min pour chaque amont
        for idx,curup in enumerate(self.myupstreams['list']):
            self.myupmin[idx]={}

        curnode:node_watershed
        for curdem in listdem:
            for idx,curup in enumerate(self.myupstreams['list']):
                curnode=curup
                x=[]
                y=[]
                
                x.append(curnode.cums)
                
                if curdem=='cs':
                    basey=min(curnode.dem[curdem],curnode.dem['dem2'])
                else:
                    basey=curnode.dem[curdem]

                y.append(basey)
                curnode=curnode.down

                if not self.tz is None:
                    while not curnode is None:
                        if curdem=='cs':
                            yloc=min(curnode.dem[curdem],curnode.dem['dem2'])
                        else:
                            yloc=curnode.dem[curdem]
                        
                        if basey-yloc>self.tz:
                            x.append(curnode.cums)
                            y.append(yloc)
                            basey=yloc
                        curnode=curnode.down
                elif not self.tslope is None:
                    locs= self.parent.myresolution
                    while not curnode is None:
                        if curdem=='cs':
                            yloc=min(curnode.dem[curdem],curnode.dem['dem2'])
                        else:
                            yloc=curnode.dem[curdem]
                        
                        if (basey-yloc)/locs>self.tslope:
                            x.append(curnode.cums)
                            y.append(yloc)
                            basey=yloc
                            locs= self.parent.myresolution
                        else:
                            locs+= self.parent.myresolution
                        curnode=curnode.down

                self.myupmin[idx][curdem]=[x,y]

    def compute_slopes(self):
        self.myslopes={}
        #on initialise le dictionnaire de topo min pour chaque amont
        for idx,curup in enumerate(self.myupstreams['list']):
            self.myslopes[idx]={}

        curnode:node_watershed
        for curdem in listdem:
            for idx,curup in enumerate(self.myupstreams['list']):
                curdict=self.myupmin[idx][curdem]
                xmin=curdict[0]
                if len(xmin)>1:
                    ymin=curdict[1]
                    x=self.get_x(whichup=idx)

                    f=interpolate.interp1d(xmin,ymin, fill_value='extrapolate')
                    y=f(x)
                    slopes=self.compute_slope_down(x,y)

                    curnode=curup
                    i=0
                    while not curnode is None:
                        curnode.slopecorr[curdem]['parts'].append(slopes[i])
                        i+=1
                        curnode=curnode.down

        #calcul de la moyenne sur base des valeurs partielles
        for curdem in listdem:
            for curreach in self.myreaches['reaches']:
                nodeslist=self.myreaches['reaches'][curreach]['baselist']
                for curnode in nodeslist:
                    if len(nodeslist)<2:
                        if not self.tslope is None:
                            curnode.slopecorr[curdem]['value']=max(self.tslope,curnode.slope)
                        else:
                            curnode.slopecorr[curdem]['value']=self.tslope=1.e-4
                    else:
                        curnode.slopecorr[curdem]['value']=np.mean(curnode.slopecorr[curdem]['parts'])
                
    def compute_slope_down(self,x,y):
        slope=[]
        for i in range(len(x)-1):
            slope.append((y[i+1]-y[i])/(x[i+1]-x[i]))
        slope.append(slope[-1])
        return slope

class runoffsystem:   
    myupmin:dict
    mynodes:list
    
    myslopes:dict
    parent=None
    myupstreams:dict 
    
    maxlevels:int
    maxstrahler:int

    tslope:float =None
    tz:float =None

    def __init__(self,runoff:list,parent,thresholdz=None,thresholdslope=None, *args, **kwargs):
        curnode:node_watershed

        self.parent=parent
        self.mynodes=runoff
        self.myupstreams={}
        #sélection des mailles qui ont une surface unitaire comme surface drainée
        areaup = pow(parent.myresolution,2)/1.e6
        self.myupstreams['list']=list(filter(lambda x: (x.uparea-areaup)<1.e-6 ,runoff))            
        if not thresholdz is None:
            self.tz=thresholdz
        elif not thresholdslope is None:
            self.tslope=thresholdslope
        
        self.selectmin()
        return super().__init__(*args, **kwargs)

    def get_x(self,whichup=None):
        if not whichup is None:
            curnode:node_watershed
            x=[]
            curnode=self.myupstreams['list'][whichup]
            while not curnode.river:
                x.append(curnode.cums)
                curnode=curnode.down
        else:
            x=[]

        return x

    def get_dem(self,whichdem,whichup=None):
        if not whichup is None:
            curnode:node_watershed
            dem=[]
            curnode=self.myupstreams['list'][whichup]
            while not curnode.river:
                dem.append(curnode.dem[whichdem])
                curnode=curnode.down
        return dem

    def get_dem_corr(self,whichdem,whichup=None):
        if not whichup is None:
            curnode:node_watershed
            dem=[]
            curnode=self.myupstreams['list'][whichup]
            while not curnode.river:
                dem.append(curnode.dem[whichdem])
                curnode=curnode.down
        return dem

    def get_slope(self,whichslope=None,whichup=None):
        if whichslope is None:
            if not whichup is None:
                curnode:node_watershed
                slope=[]
                curnode=self.myupstreams['list'][whichup]
                while not curnode.river:
                    slope.append(curnode.slope)
                    curnode=curnode.down
        else:        
            if not whichup is None:
                curnode:node_watershed
                slope=[]
                curnode=self.myupstreams['list'][whichup]
                while not curnode.river:
                    slope.append(curnode.slopecorr[whichslope]['value'])
                    curnode=curnode.down
        
        return slope

    def plot_dem(self,which=-1):
        mymarkers=['x','+','1','2','3','4']
        if which>-1:
            if which<len(self.myupstreams['list']):
                fig=plt.figure()
                fig.suptitle('Upstream n°'+str(which))               
                
                x=np.array(self.get_x(whichup=which))
                for idx,curdem in enumerate(listdem):
                    y=np.array(self.get_dem(curdem,whichup=which))
                    
                    xmask=np.ma.masked_where(y==99999.,x)
                    ymask=np.ma.masked_where(y==99999.,y)
                    plt.scatter(xmask,ymask,marker=mymarkers[idx],label=curdem)
                
            plt.legend()
        plt.show()

    def plot_dem_and_corr(self,which=-1,whichdem='dem2'):
        if which<len(self.myupstreams['list']):
            fig=plt.figure()
            fig.suptitle('Upstream n°'+str(which))               
            
            x=np.array(self.get_x(whichup=which))
            y=np.array(self.get_dem(whichdem,whichup=which))
            
            xcorr=self.myupmin[which][whichdem][0]
            ycorr=self.myupmin[which][whichdem][1]
            
            xmask=np.ma.masked_where(y==99999.,x)
            ymask=np.ma.masked_where(y==99999.,y)

            plt.scatter(xmask,ymask,marker='x',label=whichdem)
            plt.scatter(xcorr,ycorr,marker='+',label='selected points')
            
            plt.legend()
            plt.savefig(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\Simulations\Hydrologie\Up'+str(which)+'_'+whichdem+'.png')
            #plt.show()
    
    def write_slopes(self):
        #Uniquement les pentes runoff
        for curlist in listdem:
            slopes= WolfArray(self.parent.mydir+'\\Characteristic_maps\\Drainage_basin.slope')
            slopes.reset()
            curnode:node_watershed
            for curnode in self.mynodes:
                i=curnode.i
                j=curnode.j
                slopes.array[i,j]=curnode.slopecorr[curlist]['value']

            slopes.filename = self.parent.mydir+'\\Characteristic_maps\\Drainage_basin.slope_corr_run_'+curlist
            slopes.write_all()

    def selectmin(self):
        #Sélection des valeurs minimales afin de conserver une topo décroissante vers l'aval --> une pente positive
        self.myupmin={}
        
        #on initialise le dictionnaire de topo min pour chaque amont
        for idx,curup in enumerate(self.myupstreams['list']):
            self.myupmin[idx]={}

        curnode:node_watershed
        for curdem in listdem:
            for idx,curup in enumerate(self.myupstreams['list']):
                curnode=curup
                x=[]
                y=[]
                
                x.append(curnode.cums)
                
                if curdem=='cs':
                    basey=min(curnode.dem[curdem],curnode.dem['dem2'])
                else:
                    basey=curnode.dem[curdem]

                y.append(basey)
                curnode=curnode.down

                if not self.tz is None:
                    while not curnode.river:
                        if curdem=='cs':
                            yloc=min(curnode.dem[curdem],curnode.dem['dem2'])
                        else:
                            yloc=curnode.dem[curdem]
                        
                        if basey-yloc>self.tz:
                            x.append(curnode.cums)
                            y.append(yloc)
                            basey=yloc
                        curnode=curnode.down
                elif not self.tslope is None:
                    locs=self.parent.myresolution
                    while not curnode.river:
                        if curdem=='cs':
                            yloc=min(curnode.dem[curdem],curnode.dem['dem2'])
                        else:
                            yloc=curnode.dem[curdem]
                        
                        if (basey-yloc)/locs>self.tslope:
                            x.append(curnode.cums)
                            y.append(yloc)
                            basey=yloc
                            locs=self.parent.myresolution
                        else:
                            locs+=self.parent.myresolution
                        curnode=curnode.down
                        

                self.myupmin[idx][curdem]=[x,y]

    def compute_slopes(self):
        self.myslopes={}
        #on initialise le dictionnaire de topo min pour chaque amont
        for idx,curup in enumerate(self.myupstreams['list']):
            self.myslopes[idx]={}

        curnode:node_watershed
        for curdem in listdem:
            for idx,curup in enumerate(self.myupstreams['list']):
                curdict=self.myupmin[idx][curdem]
                xmin=curdict[0]
                if len(xmin)>1:                
                    ymin=curdict[1]
                    x=self.get_x(whichup=idx)

                    f=interpolate.interp1d(xmin,ymin, fill_value='extrapolate')
                    y=f(x)
                    slopes=self.compute_slope_down(x,y)

                    curnode=curup
                    i=0
                    while not curnode.river:
                        curnode.slopecorr[curdem]['parts'].append(slopes[i])
                        i+=1
                        curnode=curnode.down
        #calcul de la moyenne sur base des valeurs partielles
        for curdem in listdem:
            for curnode in self.mynodes:
                if len(curnode.slopecorr[curdem]['parts'])<2:
                    #Ce cas particulier peut arriver si des mailles BV sont remplies par une zone plate qui s'étend en rivière
                    # Comme on ne recherche de mailles plus basses que dans la partie BV, il n'est pas possible de corriger les pentes
                    if not self.tslope is None:
                        curnode.slopecorr[curdem]['value']=max(self.tslope,curnode.slope)
                    else:
                        curnode.slopecorr[curdem]['value']=1.e-4
                else:
                    curnode.slopecorr[curdem]['value']=np.mean(curnode.slopecorr[curdem]['parts'])
                
    def compute_slope_down(self,x,y):
        slope=[]
        for i in range(len(x)-1):
            slope.append((y[i+1]-y[i])/(x[i+1]-x[i]))
        slope.append(slope[-1])
        return slope

class watershed:
    
    mydir: str
    myresolution: float

    myoutlet=None

    subs: WolfArray

    mynodes:list
    mynodesindex:np.array
    myrivers:list
    myrunoff:list
    up=None

    mycoupled:list

    mysubs: dict
    nbsubs: int
    mystats: dict

    mycouplednodesxy:list
    mycouplednodesij:list
    myriversystem:riversystem
    myrunoffsystem:runoffsystem
    mycs:crosssections = None    

    def __init__(self,dir,thresholdz=None,thresholdslope=None,mycs=None, *args, **kwargs):

        self.mydir=os.path.normpath(dir)

        self.subs= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basin.sub')
        self.nbsubs = ma.max(self.subs.array)
        self.myresolution = self.subs.dx

        f = open(self.mydir+'\\Coupled_pairs.txt', 'r')
        lines = f.read().splitlines()
        f.close()

        self.mycouplednodesxy=[]
        self.mycouplednodesij=[]

        if lines[0]=='COORDINATES':
            for xy in enumerate(lines[1:]):
                xup,yup,xdown,ydown=xy[1].split('\t')
                self.mycouplednodesxy.append([float(xup),float(yup),float(xdown),float(ydown)])
                self.mycouplednodesij.append([self.subs.get_ij_from_xy(float(xup),float(yup)),self.subs.get_ij_from_xy(float(xdown),float(ydown))])

        self.mynodesindex = np.zeros([self.subs.nbx,self.subs.nby],dtype=int)

        self.init_nodes()
        
        if not mycs is None:
            self.set_crossSections(mycs)
            self.attrib_cs_to_nodes()

        if not thresholdz is None:
            self.myriversystem = riversystem(self.myrivers,self,thresholdz=thresholdz)
            self.myrunoffsystem = runoffsystem(self.myrunoff,self,thresholdz=thresholdz)
            self.myriversystem.compute_slopes()
            self.myrunoffsystem.compute_slopes()
        elif not thresholdslope is None:
            self.myriversystem = riversystem(self.myrivers,self,thresholdslope=thresholdslope)
            self.myrunoffsystem = runoffsystem(self.myrunoff,self,thresholdslope=thresholdslope)
            self.myriversystem.compute_slopes()
            self.myrunoffsystem.compute_slopes()
        
        return super().__init__(*args, **kwargs)

    def write_slopes(self):
        
        for curlist in listdem:
            curpath=self.mydir+'\\Characteristic_maps\\corrslopes\\'+curlist
            os.makedirs(curpath,exist_ok=True)
            slopes= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basin.slope')
        
            curnode:node_watershed
            for curnode in self.mynodes:
                i=curnode.i
                j=curnode.j
                slopes.array[i,j]=curnode.slopecorr[curlist]['value']

            slopes.filename = curpath +'\\Drainage_basin.slope_corr'
            slopes.write_all()

    def set_crossSections(self,cs):
        self.mycs=cs

    def attrib_cs_to_nodes(self):
        if not self.mycs is None:
            for curlist in self.mycs:
                for namecs in curlist.myprofiles:
                    curvert:wolfvertex
                    curcs=curlist.myprofiles[namecs]
                    
                    try:
                        curvert=curcs['bed']
                    except:
                        curvert=curlist.get_min(whichprofile=curcs)

                    i,j=self.subs.get_ij_from_xy(curvert.x,curvert.y)
                    curnode:node_watershed
                    curnode =self.mynodes[self.mynodesindex[i,j]]

                    if curnode.river:
                        if curnode.mycs is None:
                            curnode.mycs=[]
                        curnode.mycs.append(curcs)                
                        curnode.dem['cs']=min(curnode.dem['cs'],curvert.z)            

    def init_nodes(self):
        self.mynodes=[node_watershed() for i in range(self.subs.nbnotnull)]

        dem1= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basin.b')
        dem2= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basincorr.b')
        demcorr= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basindiff.b')
        slopes= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basin.slope',masknull=False)
        reaches= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basin.reachs')
        cnv= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basin.cnv')
        times= WolfArray(self.mydir+'\\Characteristic_maps\\Drainage_basin.time')

        dem2.array.mask = self.subs.array.mask

        nb=0
        for index,x in np.ndenumerate(self.subs.array):
            if(x>0):
                i=int(index[0])
                j=int(index[1])
                self.mynodesindex[i,j]=nb
                nb+=1

        curnode:node_watershed
        nb=0
        for index,x in np.ndenumerate(self.subs.array):
            if(x>0):
                i=int(index[0])
                j=int(index[1])
                curnode =self.mynodes[self.mynodesindex[i,j]]

                curnode.i = i
                curnode.j = j
                curnode.index=nb
                curnode.dem={}
                curnode.dem['dem1']=dem1.array[i,j]
                curnode.dem['dem2']=dem2.array[i,j]
                curnode.dem['cs']=99999.
                curnode.demcorr=demcorr.array[i,j]
                curnode.slope=slopes.array[i,j]
                curnode.slopecorr={}
                for curlist in listdem:
                    curnode.slopecorr[curlist]={}
                    curnode.slopecorr[curlist]['parts']=[]
                    curnode.slopecorr[curlist]['value']=curnode.slope

                curnode.sub=int(x)
                curnode.time=times.array[i,j]
                curnode.uparea=cnv.array[i,j]
                curnode.river=reaches.array[i,j]>0
                if curnode.river:
                    curnode.reach=int(reaches.array[i,j])
                curnode.forced=False
                curnode.up=[]
                curnode.upriver=[]
                curnode.strahler=0
                curnode.reachlevel=0
                nb+=1
                
        #Liaison échanges forcés
        incr=slopes.dx
        for curexch in self.mycouplednodesij:
            i=int(curexch[0][0])
            j=int(curexch[0][1])
            curnode=self.mynodes[self.mynodesindex[i,j]]
            curnode.forced=True
            idown = int(curexch[1][0])
            jdown = int(curexch[1][1])
            curdown = self.mynodes[self.mynodesindex[idown,jdown]]
            curnode.down = curdown
            curdown.up.append(curnode)
            if curnode.river:
                curdown.upriver.append(curnode)
            curnode.incrs = incr * np.sqrt(pow(curdown.i-i,2)+pow(curdown.j-j,2))

        #Liaison hors échanges forcés
        for curnode in self.mynodes:
            if not curnode.forced:
                i=curnode.i
                j=curnode.j

                curtop=curnode.dem['dem2']
                diff=[dem2.array[i-1,j] - curtop,dem2.array[i+1,j] - curtop,dem2.array[i,j-1] - curtop,dem2.array[i,j+1] - curtop]
                mindiff = ma.min(diff)
                if mindiff<0:
                    index = diff.index(mindiff)
                    if index==0:
                        curdown = self.mynodes[self.mynodesindex[i-1,j]]
                    elif index==1:
                        curdown = self.mynodes[self.mynodesindex[i+1,j]]
                    elif index==2:
                        curdown = self.mynodes[self.mynodesindex[i,j-1]]
                    else:
                        curdown = self.mynodes[self.mynodesindex[i,j+1]]

                    curnode.down = curdown
                    curdown.up.append(curnode)
                    if curnode.river:
                        curdown.upriver.append(curnode)
                    curnode.incrs=incr
                else:
                    self.myoutlet = curnode

        #Rechreche de la pente dans les voisins en croix dans la topo non remaniée
        for curnode in self.mynodes:
            if not curnode.forced:
                i=curnode.i
                j=curnode.j

                curtop = curnode.dem['dem1']
                diff=[dem1.array[i-1,j] - curtop,dem1.array[i+1,j] - curtop,dem1.array[i,j-1] - curtop,dem1.array[i,j+1] - curtop,
                      dem1.array[i-1,j-1] - curtop,dem1.array[i+1,j+1] - curtop,dem1.array[i+1,j-1] - curtop,dem1.array[i-1,j+1] - curtop]
                mindiff = ma.min(diff)

                fact=1.
                if mindiff<0:
                    index = diff.index(mindiff)
                    if index>3:
                        fact=np.sqrt(2)

                curnode.sloped8 = -mindiff/(100.*fact)

        self.myrivers=list(filter(lambda x: x.river,self.mynodes))
        self.myrivers.sort(key=lambda x: x.dem['dem2'])
        self.myoutlet.incr_curvi()
        
        self.find_dem_subpixels()

        self.myrunoff=self.find_runoffnodes()


    def find_rivers(self,whichsub=0,whichreach=0):
        """
        Recherche des mailles rivières 
        @param whichsub : numéro du sous-bassin à traiter
        @param whicreach : numéro du tronçon à identifier
        """
        if whichsub>0 and whichsub<=self.nbsubs:
            if whichreach>0:
                myrivers=list(filter(lambda x: x.river and x.sub==whichsub and x.reach==whichreach,self.myrivers))
            else:
                myrivers=list(filter(lambda x: x.river and x.sub==whichsub,self.myrivers))
        else:
            if whichreach>0:
                myrivers=list(filter(lambda x: x.river and x.reach==whichreach,self.myrivers))
            else:
                myrivers=list(filter(lambda x: x.river,self.myrivers))

        myrivers.sort(key=lambda x: x.dem['dem2'])
        
        up=None
        if len(myrivers)>0:
            up=myrivers[-1]

        return myrivers,up

    def find_sub(self,whichsub=0):
        """
        Recherche des mailles du sou-bassin versant
        @param whichsub : numéro du sous-bassin à traiter
        """
        if whichsub>0 and whichsub<=self.nbsubs:
            mysub=list(filter(lambda x: x.sub==whichsub,self.mynodes))
        else:
            mysub=self.mynodes.copy

        mysub.sort(key=lambda x: x.dem['dem2'])
        
        return mysub

    def find_runoffnodes(self,whichsub=0):
        """
        Recherche des mailles du bassin versant seul (sans les rivières)    
        @param whichsub : numéro du sous-bassin à traiter
        """
        if whichsub>0 and whichsub<=self.nbsubs:
            myrunoff=list(filter(lambda x: not x.river and x.sub==whichsub,self.mynodes))
        else:
            myrunoff=list(filter(lambda x: not x.river,self.mynodes))

        myrunoff.sort(key=lambda x: x.dem['dem2'])
        
        return myrunoff

    def index_flatzone(self,listofsortednodes,threshold):
        curnode:node_watershed
        curflat:node_watershed

        curindex=0
        for curnode in listofsortednodes[-1:1:-1]:
            addone=False
            while curnode.slope<threshold and curnode.flatindex==-1:
                addone=True
                curnode.flatindex=curindex
                if curnode.down is None:
                    break
                curnode=curnode.down
            if addone:
                curindex+=1

        return curindex

    def find_flatnodes(self,listofsortednodes):
        """
        Recherche des mailles dans des zones de faibles pentes    
        @param listofsortednodes : liste triée de mailles
        """
        myflatnodes=list(filter(lambda x: x.flatindex>-1,listofsortednodes))
        
        return myflatnodes

    def find_flatzones(self,listofsortednodes,maxindex):
        """
        Recherche des mailles dans des zones de faibles pentes    
        @param listofsortednodes : liste triée de mailles
        """
        myflatzones=[[]] * maxindex
        for i in range(maxindex):
            myflatzones[i]=list(filter(lambda x: x.flatindex==i,listofsortednodes))
        
        return myflatzones


    def find_dem_subpixels(self):
        """
        Recherche des altitudes dans un mnt plus dense    
        """        
        dem10m=WolfArray(self.mydir+'\\mnt10m.bin')
        dem20m=WolfArray(self.mydir+'\\mnt20m.bin')

        demsubs={'dem10m':dem10m,'dem20m':dem20m}

        curnode:node_watershed
        for curdem in demsubs:
            locdem=demsubs[curdem]
            dx=locdem.dx
            dy=locdem.dy

            for curnode in self.mynodes:
                curi=curnode.i
                curj=curnode.j

                curx,cury=self.subs.get_xy_from_ij(curi,curj)
                
                decalx=(self.myresolution-dx)/2.
                decaly=(self.myresolution-dy)/2.
                x1=curx-decalx
                y1=cury-decaly
                x2=curx+decalx
                y2=cury+decaly

                i1,j1=locdem.get_ij_from_xy(x1,y1)
                i2,j2=locdem.get_ij_from_xy(x2,y2)

                curnode.dem[curdem]=np.min(locdem.array[i1:i2+1,j1:j2+1])

    def compute_stats(self):
        
        self.mystats={}
        
        slopes=np.array(list(x.slope for x in self.mynodes))
        slopesrunoff=np.array(list(x.slope for x in list(filter(lambda x: not x.river,self.mynodes))))
        slopesriver=np.array(list(x.slope for x in list(filter(lambda x: x.river,self.mynodes))))

        self.mystats['slopemin'] = np.min(slopes)
        self.mystats['slopemax'] = np.max(slopes)
        self.mystats['slopemedian'] = np.median(slopes)
        self.mystats['slopemean'] = np.mean(slopes)
        self.mystats['hist'] = slopes
        self.mystats['hist_watershed'] = slopesrunoff
        self.mystats['hist_reaches'] = slopesriver

        for curlist in listdem:
            curdict=self.mystats[curlist]={}
            
            slopes=np.array(list(x.slopecorr[curlist]['value'] for x in self.mynodes))
            slopesrunoff=np.array(list(x.slopecorr[curlist]['value'] for x in list(filter(lambda x: not x.river,self.mynodes))))
            slopesriver=np.array(list(x.slopecorr[curlist]['value'] for x in list(filter(lambda x: x.river,self.mynodes))))

            curdict['slopemin'] = np.min(slopes)
            curdict['slopemax'] = np.max(slopes)
            curdict['slopemedian'] = np.median(slopes)
            curdict['slopemean'] = np.mean(slopes)
            curdict['hist'] = slopes
            curdict['hist_watershed'] = slopesrunoff
            curdict['hist_reaches'] = slopesriver


    def plot_stats(self):

        bin1=np.array([1.e-8,1.e-7,1.e-6,5.e-6])
        bin2=np.linspace(1.e-5,1,num=2000)
        bins=np.concatenate((bin1,bin2)) #[0,1e-8,1e-7,1e-5,1e-2,1e-1,2e-1,3e-1,4e-1,5e-1,6e-1,7e-1,8e-1,9e-1,1,2]
        fig,ax = plt.subplots(3)
        fig.suptitle('Slope distribution')
        ax[0].hist(self.mystats['hist'],bins,cumulative=True,density=True,histtype=u'step',label='base')
        ax[0].set_xscale('log')
        ax[0].set_xlabel('All meshes')
        ax[1].hist(self.mystats['hist_watershed'],bins,cumulative=True,density=True,histtype=u'step',label='base')
        ax[1].set_xscale('log')
        ax[1].set_xlabel('Watershed')
        ax[2].hist(self.mystats['hist_reaches'],bins,cumulative=True,density=True,histtype=u'step',label='base')
        ax[2].set_xscale('log')
        ax[2].set_xlabel('River')
        plt.show()

        for curlist in listdem:
            #fig,ax = plt.subplots(3)
            #fig.suptitle(curlist)
            curdict=self.mystats[curlist]
            ax[0].hist(curdict['hist'],bins,cumulative=True,density=True,histtype=u'step',label=curlist)
            ax[0].set_xscale('log')
            ax[0].set_xlabel('All meshes')
            ax[1].hist(curdict['hist_watershed'],bins,cumulative=True,density=True,histtype=u'step',label=curlist)
            ax[1].set_xscale('log')
            ax[1].set_xlabel('Watershed')
            ax[2].hist(curdict['hist_reaches'],bins,cumulative=True,density=True,histtype=u'step',label=curlist)
            ax[2].set_xscale('log')
            ax[2].set_xlabel('River')
        
        plt.legend()
        plt.show()