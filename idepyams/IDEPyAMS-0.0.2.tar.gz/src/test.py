from sys import path;
path+=["d:/page_help_web/pypi/pyams/src/lib/analysis"];
path+=["d:/page_help_web/pypi/pyams/src/symbols/basic"];
path+=["d:/page_help_web/pypi/pyams/src/symbols/source"];
#------------------------------------------------------------------
from PyAMS import strToFloat;
from simu import AppPyAMS;
from Resistor import Resistor
from DCVoltage import DCVoltage
#------------------------------------------------------------------
R1=Resistor("N03","N02");
R2=Resistor("0","N02");
V1=DCVoltage("N03","N04");
R3=Resistor("N02","0");
R4=Resistor("0","N04");
V2=DCVoltage("N05","N04");
R5=Resistor("N05","0");
#------------------------------------------------------------------
R1.R+=strToFloat("100Ω ");
R2.R+=strToFloat("100Ω ");
V1.Vdc+=strToFloat("30V");
R3.R+=strToFloat("100Ω ");
R4.R+=strToFloat("50Ω ");
V2.Vdc+=strToFloat("15.0V");
R5.R+=strToFloat("150Ω ");
#------------------------------------------------------------------
AppPyAMS.setOut(R2.V,R2.V,R3.V,R4.V,R5.V,V1.V,V2.V)
AppPyAMS.circuit({"R1":R1,"R2":R2,"V1":V1,"R3":R3,"R4":R4,"V2":V2,"R5":R5});
AppPyAMS.analysis(mode="op",start=0.0,stop=0.1,step=0.1);
AppPyAMS.run(True);
