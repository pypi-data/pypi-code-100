#-------------------------------------------------------------------------------
# Name:        simulation options
# Author:      d.fathi
# Created:     20/03/2015
# Update:      04/10/2021
# Copyright:   (c) pyams 2021
# Web:         www.PyAMS.org
# Licence:     unlicense
# info:        initial conditions of simulation
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# class simulationOption: pyams simulation options
#-------------------------------------------------------------------------------

class simulationOption(object):
    def __init__(self):
        self.RELTOL=1e-5    #"Relative accuracy of V's and I's    (RELTOL)"
        self.VNTOL=1e-8     #'Volts',"Best accuracy of voltages    (VNTOL)"
        self.ABSTOL=1e-12   #'Amps',"Best accuracy of currents    (ABSTOL)"
        self.CHGTOL=1e-14
        self.ITL1=200
        self.ITL2=100
        self.ITL4=40
        self.RELTOL=1.0e-3
        self.MaxiNumbPnt=900000
        self.MInteg=1
        self.MSolve=1
        self.ITLC=60
        self.len=0
        self.les=0
        self.ldt=0
        self.niter=0
        self.nStep=0
        self.Run=True
        self.MethodIntegration='BR'
        self.Trapezoidal=True
        self.t1=0.0;
        self.t0=0.0;
        self.Start=True
        self.SegnalUsedSameTime=False
        self.TimeStep=1.2;
        self.GetStep=0.0;
        self.SaveSignalsInData=True;
    def SetOption(self,Option):
        #Get Option from PyAMS interface and cnovert paramater to real value

        if 'RELTOL' in Option:
            self.RELTOL=Option['RELTOL'];
            print('RELTOL =',self.RELTOL)

        if 'VNTOL' in Option:
            self.VNTOL=Option['VNTOL'];
            print('VNTOL =',self.VNTOL)

        if 'MethodIntegration' in Option:
            self.MethodIntegration=Option['MethodIntegration'];
            self.Trapezoidal=(self.MethodIntegration==1);
            if self.Trapezoidal:
               print('MethodIntegration =Trapezoidal')

        if 'ITL1' in Option:
            self.ITL1=Option['ITL1'];
            print('ITL1 =',self.ITL1)

        if 'ITL4' in Option:
            self.ITL4=Option['ITL4'];
            print('ITL4 =',self.ITL1)

    def Result(self):
        print('numbre of iteration: ',self.niter)
        print('numbre of step: ',self.nStep)
    def SetTimeStep(self,T):
        self.TimeStep=T;
        self.TimeStepMax=T;

simulationOption=simulationOption()

'''
if UniteToValeur(Edit_Step.Text) <= 0 then
  ListOfErrors.Add('[Error] E6004:TR Statmet error "Step time" must be positive');

if UniteToValeur(Edit_Stop.Text) <= 0 then
  ListOfErrors.Add('[Error] E6005:TR Statmet error "Stop time" must be positive');

if UniteToValeur(Edit_Step.Text) > UniteToValeur(Edit_Stop.Text) then
  ListOfErrors.Add('[Error] E6006:TR Statmet error "Stop time" must be greater than "Step time"');

if abstol <=0  then
  ListOfErrors.Add('[Error] E6007:TR Statmet error "AbsToL" must be positive');

if reltol <=0  then
  ListOfErrors.Add('[Error] E6008:TR Statmet error "RelToL" must be positive');

if ChgTol <=0  then
  ListOfErrors.Add('[Error] E6009:TR Statmet error "ChgToL" must be positive');

if TrTol <=0  then
  ListOfErrors.Add('[Error] E6009:TR Statmet error "TrToL" must be positive');

if Vntol <=0  then
  ListOfErrors.Add('[Error] E6010:TR Statmet error "VnToL" must be positive');

if ITL1 <=0  then
  ListOfErrors.Add('[Error] E6011:TR Statmet error "ITL1" must be positive');

if ITL2 <=0  then
  ListOfErrors.Add('[Error] E6012:TR Statmet error "ITL2" must be positive');

if ITL2 > ITL1 then
  ListOfErrors.Add('[Error] E6013:TR Statmet error "ITL1" must be greater than "ITL2"');

if ITL3 <=0  then
  ListOfErrors.Add('[Error] E6014:TR Statmet error "ITL3" must be positive');

if ITL4 <=0  then
  ListOfErrors.Add('[Error] E6015:TR Statmet error "ITL4" must be positive');

if ITL3 > ITL4 then
  ListOfErrors.Add('[Error] E6016:TR Statmet error "ITL4" must be greater than "ITL3"');
'''