def sustainedwindduration(windvel, winddir, MaxwindvelVar=2.5, MaxwinddirVar=15, WindInterval=3600, dispout='no'):
    """
    .. ++++++++++++++++++++++++++++++++YA LATIF++++++++++++++++++++++++++++++++++
    .. +                                                                        +
    .. + ScientiMate                                                            +
    .. + Earth-Science Data Analysis Library                                    +
    .. +                                                                        +
    .. + Developed by: Arash Karimpour                                          +
    .. + Contact     : www.arashkarimpour.com                                   +
    .. + Developed/Updated (yyyy-mm-dd): 2017-07-01                             +
    .. +                                                                        +
    .. ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    scientimate.sustainedwindduration
    =================================

    .. code:: python

        SustWindDur = scientimate.sustainedwindduration(windvel, winddir, MaxwindvelVar=2.5, MaxwinddirVar=15, WindInterval=3600, dispout='no')

    Description
    -----------

    Calculate the sustained wind duration

    Inputs
    ------

    windvel
        Wind velocity time series data in (m/s)
    winddir
        Wind direction time series data in (Degree)
    MaxwindvelVar=2.5
        | Maximum allowed wind velocity variation around a mean to allow wind to be considered sustained in (m/s)
        | Coastal Engineering Manual (2015) suggests 2.5 m/s
    MaxwinddirVar=15
        | Maximum allowed wind direction variation around a mean to allow wind to be considered sustained in (Degree)
        | Coastal Engineering Manual (2015) suggests 15 degree
    WindInterval=3600
        Time interval between two consecutive wind measurements (data points) in (second)
    dispout='no'
        Define to display outputs or not ('yes': display, 'no': not display)

    Outputs
    -------

    SustWindDur
        Sustained Wind Duration in (second)

    Examples
    --------

    .. code:: python

        import scientimate as sm

        #Data from https://tidesandcurrents.noaa.gov for Grand Isle, LA, USA (8761724), for June 1st, 2017, reported hourly
        windvel=[3,4.7,4.9,5.3,3.3,3.4,3.3,3.8,3.1,2,1.3,1.2,1.5,3.2,2.9,3,2.9,3.7,3.7,3.1,3.4,2.6,2.5,2.5] #24 Hour wind velocity
        winddir=[78,86,88,107,131,151,163,163,153,150,148,105,105,75,95,103,97,103,108,111,124,183,171,113] #24 Hour wind direction
        SustWindDur=sm.sustainedwindduration(windvel,winddir,2.5,15,3600,'yes')

    References
    ----------

    U.S. Army Corps of Engineers (2015). 
    Coastal Engineering Manual. 
    Engineer Manual 1110-2-1100, Washington, D.C.: U.S. Army Corps of Engineers.

    Yamartino, R. J. (1984). 
    A comparison of several "single-pass" estimators of the standard deviation of wind direction. 
    Journal of Climate and Applied Meteorology, 23(9), 1362-1366.

    .. License & Disclaimer
    .. --------------------
    ..
    .. Copyright (c) 2020 Arash Karimpour
    ..
    .. http://www.arashkarimpour.com
    ..
    .. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    .. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    .. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    .. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    .. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    .. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    .. SOFTWARE.
    """

    #--------------------------------------------------------------------------
    #CODE
    #--------------------------------------------------------------------------
    #Import required packages

    import numpy as np
    import scipy as sp
    if dispout=='yes':
        import matplotlib.pyplot as plt 

    #--------------------------------------------------------------------------
    #Convert inputs to numpy array

    #Changing type to numpy array
    def type2numpy(variable):
        if type(variable) is not str:
            if np.size(variable)==1:
                if ((type(variable) is list) or (type(variable) is np.ndarray)):
                    variable=np.array(variable)
                else:
                    variable=np.array([variable])
            elif np.size(variable)>1:
                if (type(variable).__module__)!='numpy':
                    variable=np.array(variable) 
        return variable
    
    windvel=type2numpy(windvel)
    winddir=type2numpy(winddir)

    #--------------------------------------------------------------------------
    #Calculating the sustained wind duration

    #Pre-assigning array
    SustWindIndex=np.zeros(len(windvel)) #Pre-assigning array
    SustWindDurIndex=np.zeros(len(windvel)) #Pre-assigning array
    SustWindDur=np.zeros(len(windvel)) #Pre-assigning array
    windvelavg=np.zeros(len(windvel)) #Pre-assigning array
    winddiravg=np.zeros(len(windvel)) #Pre-assigning array
    deltawindvel=np.zeros(len(windvel)) #Pre-assigning array
    deltawinddir=np.zeros(len(windvel)) #Pre-assigning array
    
    #Assigning first element
    SustWindIndex[0]=1 #Sustained wind index (1: Sustained, 0: Un-sustained)
    SustWindDurIndex[0]=SustWindIndex[0] #Sustained wind duration index
    SustWindDur[0]=SustWindDurIndex[0]*WindInterval # Sustained Wind Duration
    
    #Calculating the sustained wind duration
    k=0 #Sustained wind index counter
    for i in range(1,len(windvel),1):
        
        #Mean wind velocity
        windvelavg[i-1]=np.nanmean(windvel[k:i])
        
        #Simple wind direction averaging
        #winddiravg[i-1]=np.nanmean(winddir[k:i]) #Simple mean calculation
        
        #Wind direction averaging using Yamartino (1984) method
        x=np.cos(np.deg2rad(winddir[k:i]))
        y=np.sin(np.deg2rad(winddir[k:i]))
        xmean=np.nanmean(x)
        ymean=np.nanmean(y)
        Dir=np.rad2deg(np.arctan2(ymean,xmean)) #Use arctan2 instead of arctan to get the averaged wind direction between -180 and 180
        winddiravg[i-1]=((Dir+360)%360) #Use mod(360) to take care of the ones larger than 360 (Add 360 to all numbers to make them all positive)
        
        deltawindvel[i]=windvel[i]-windvelavg[i-1]
        deltawinddir[i]=winddir[i]-winddiravg[i-1]
        
        #Checking if winddiravg is right before 360 degree and winddir is right after 360 (0) degree
        if ((winddiravg[i-1]>(360-MaxwinddirVar)) and (winddiravg[i-1]<=360) and (winddir[i]>=0) and (winddir[i]<MaxwinddirVar)):
            deltawinddir[i]=(winddir[i]+360)-winddiravg[i-1]
        
        #Checking if winddiravg is right after 360 (0) degree and winddir is right before 360 degree
        if ((winddiravg[i-1]>=0) and (winddiravg[i-1]<MaxwinddirVar) and (winddir[i]>(360-MaxwinddirVar)) and (winddir[i]<=360)):
            deltawinddir[i]=(360-winddir[i])-winddiravg[i-1]
        
        #Calculating sustained wind duration index, each index means duration equal to 1 WindInterval
        if ((np.abs(deltawindvel[i])<=MaxwindvelVar) and (np.abs(deltawinddir[i])<=MaxwinddirVar)): #Checking for Sustained Wind (1: Sustained, 0: Un-sustained)
            SustWindIndex[i]=1 #Checking for Sustained Wind (1: Sustained, 0: Un-sustained)
            SustWindDurIndex[i]=SustWindDurIndex[i-1]+SustWindIndex[i] #Sustained Wind Duration Unit
        else:
            SustWindIndex[i]=0 #Checking for Sustained Wind (1: Sustained, 0: Un-sustained)
            SustWindDurIndex[i]=1
            k=i-1
        

    SustWindDur=SustWindDurIndex*WindInterval #Sustained Wind Duration
    SustWindDur[SustWindDurIndex==0]=1*WindInterval #Shortest Sustained Wind Duration is WindInterval seceond
    SustWindDur[SustWindDur<WindInterval]=WindInterval #Shortest Sustained Wind Duration is WindInterval seceond

    #--------------------------------------------------------------------------
    #Displaying results

    if dispout=='yes':
    
        Time=np.arange(1,len(windvel)+1)*WindInterval
    
        plt.subplot(3,1,1)
        plt.plot(Time/3600,windvel)
        plt.xlabel('Time (Hour)')
        plt.ylabel('Velocity (m/s)')
        plt.title('Velocity')
    
        plt.subplot(3,1,2)
        plt.plot(Time/3600,winddir)
        plt.xlabel('Time (Hour)')
        plt.ylabel('Direction (Degree)')
        plt.title('Direction')
    
        plt.subplot(3,1,3)
        plt.plot(Time/3600,SustWindDur/3600)
        plt.xlabel('Time (s)')
        plt.ylabel('Sustained Wind Duration (Hour)')
        plt.title('Sustained Wind Duration')
    

    #--------------------------------------------------------------------------
    #Outputs
    return SustWindDur

    #--------------------------------------------------------------------------
