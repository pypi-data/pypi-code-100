# GridWorkbench: A Python structure for power system data
#
# Adam Birchfield, Texas A&M University
# 
# Log:
# 9/29/2021 Initial version, rearranged from prior draft so that most object fields
#   are only listed in one place, the PW_Fields table. Now to add a field you just
#   need to add it in that list.
# 11/2/2021 Renamed this file to core and added fuel type object
#
#
# TODO: Add Areas, Substations, Zones, SuperAreas
#
# Package in some way, possibly rename.

from typing import OrderedDict
import pandas as pd

# To add fields to a particular object type, see the list in the main power system
# class below, not in the individual object class

class Bus:

    def __init__(self, sys, number):
        self.sys = sys
        if number in sys.bus_map:
            raise Exception(f"Bus number {number} already exists")
        sys.bus_map[number] = self
        self.number = number
        self.gen_map = OrderedDict()
        self.load_map = OrderedDict()
        self.branch_from_map = OrderedDict()
        self.branch_to_map = OrderedDict()
        self.shunt_map = OrderedDict()
        for f in self.sys.bus_pw_fields:
            setattr(self, f[0], f[2])

    def __str__(self):
        return f"Bus {self.number} {self.name if hasattr(self, 'name') else ''}"

    def __repr__(self):
        return str(self) + f" {hex(id(self))}"

    def gen(self, id):
        if id in self.gen_map:
            return self.gen_map[id]

    def gens(self):
        return (gen for gen in self.gen_map.values())

    def load(self, id):
        if id in self.load_map:
            return self.load_map[id]

    def loads(self):
        return (load for load in self.load_map.values())

    def branch_from(self, to_bus_number, id):
        if (to_bus_number, id) in self.branch_from_map:
            return self.branch_from_map[(to_bus_number, id)]

    def branches_from(self):
        return (branch for branch in self.branch_from_map.values())

    def branch_to(self, from_bus_number, id):
        if (from_bus_number, id) in self.branch_to_map:
            return self.branch_to_map[(from_bus_number, id)]

    def branches_to(self):
        return (branch for branch in self.branch_to_map.values())

    def branches(self):
        return (branch for branchset in (self.branches_to(), self.branches_from()) for branch in branchset)

    def shunt(self, id):
        if id in self.shunt_map:
            return self.shunt_map[id]

    def shunts(self):
        return (shunt for shunt in self.shunt_map.values())

class Gen:

    def __init__(self, bus, id):
        self.bus = bus
        self.id = id
        bus.gen_map[id] = self
        for f in self.bus.sys.gen_pw_fields:
            setattr(self, f[0], f[2])

    def __str__(self):
        return f"Gen {self.bus.number} {self.id} " \
            + f"{self.bus.name if hasattr(self.bus, 'name') else ''}"

    def __repr__(self):
        return str(self) + f" {hex(id(self))}"

class Load:

    def __init__(self, bus, id):
        self.bus = bus
        self.id = id
        bus.load_map[id] = self
        for f in self.bus.sys.load_pw_fields:
            setattr(self, f[0], f[2])

    def __str__(self):
        return f"Load {self.bus.number} {self.id} " \
            + f"{self.bus.name if hasattr(self.bus, 'name') else ''}"

    def __repr__(self):
        return str(self) + f" {hex(id(self))}"

class Branch:

    def __init__(self, from_bus, to_bus, id):
        self.from_bus = from_bus
        self.to_bus = to_bus
        self.id = id
        from_bus.branch_from_map[(to_bus.number, id)] = self
        to_bus.branch_to_map[(from_bus.number, id)] = self
        for f in self.from_bus.sys.branch_pw_fields:
            setattr(self, f[0], f[2])

    def __str__(self):
        return f"Branch {self.from_bus.number} {self.to_bus.number} {self.id} " \
            + f"{self.from_bus.name if hasattr(self.from_bus, 'name') else ''} to " \
            + f"{self.to_bus.name if hasattr(self.to_bus, 'name') else ''}"

    def __repr__(self):
        return str(self) + f" {hex(id(self))}"

class Shunt:

    def __init__(self, bus, id):
        self.bus = bus
        self.id = id
        bus.shunt_map[id] = self
        for f in self.bus.sys.shunt_pw_fields:
            setattr(self, f[0], f[2])

    def __str__(self):
        return f"Shunt {self.bus.number} {self.id} " \
            + f"{self.bus.name if hasattr(self.bus, 'name') else ''}"

    def __repr__(self):
        return str(self) + f" {hex(id(self))}"


class GridWorkbench:

    def __init__(self):
        self.bus_map = OrderedDict()

        # Converter functions from PowerWorld data. If unknown use pw2py_default
        pw2py_default = lambda x:x
        pw2py_connected = lambda x:x.lower() == "connected"
        pw2py_closed = lambda x:x.lower() == "closed"
        pw2py_yes = lambda x:x.lower() == "yes"

        # For each field in these lists, there are four items
        # [0] Name of field of the Python object
        # [1] Name of the field in PowerWorld
        # [2] Default value of the field (not currently implemented)
        # [3] Function to convert data from PowerWorld (see examples above)

        self.bus_pw_fields = [
            ("name", "BusName", "Default", pw2py_default),
            ("nominal_kv", "BusNomVolt", 138, pw2py_default),
            ("vpu", "BusPUVolt", 1.0, pw2py_default),
            ("vang", "BusAngle", 0.0, pw2py_default),
            ("status", "BusStatus", True, pw2py_connected),
            ("sub_number", "SubNum", 0, pw2py_default),
            ("area_number", "AreaNum", 0, pw2py_default),
            ("zone_number", "ZoneNum", 0, pw2py_default)
        ]

        self.gen_pw_fields = [
            ("status", "GenStatus", True, pw2py_closed),
            ("p", "GenMW", 0, pw2py_default),
            ("q", "GenMVR", 0, pw2py_default),
            ("pset", "GenMWSetPoint", 0, pw2py_default),
            ("qset", "GenMvrSetPoint", 0, pw2py_default),
            ("pmax", "GenMWMax", 9999, pw2py_default),
            ("pmin", "GenMWMin", 0, pw2py_default),
            ("qmax", "GenMVRMax", 9999, pw2py_default),
            ("qmin", "GenMVRMin", -9999, pw2py_default),
            ("reg_bus_num", "GenRegNum", 0, pw2py_default),
            ("reg_pu_v", "GenVoltSet", 1.0, pw2py_default),
            ("p_auto_status", "GenAGCAble", True, pw2py_yes),
            ("q_auto_status", "GenAVRAble", True, pw2py_yes),
            ("ramp_rate", "GenMWRampLimit", 0.0, pw2py_default),
            ("crank_p", "CustomFloat", 0.0, pw2py_default),
            ("crank_t", "CustomFloat:1", 0.0, pw2py_default),
            ("availability", "CustomFloat:2", 0.0, pw2py_default),
            ("fuel_type", "GenFuelType", "Unknown", pw2py_default)
        ]

        self.load_pw_fields = [
            ("status", "LoadStatus", True, pw2py_closed),
            ("p", "LoadMW", 0, pw2py_default),
            ("q", "LoadMVR", 0, pw2py_default),
            ("ps", "LoadSMW", 0, pw2py_default),
            ("qs", "LoadSMVR", 0, pw2py_default),
            ("benefit", "GenBidMWHR", 0, pw2py_default)
        ]

        self.branch_pw_fields = [
            ("status", "LineStatus", True, pw2py_closed),
            ("B", "LineC", 0, pw2py_default),
            ("MVA_Limit_A", "LineAMVA", 0, pw2py_default),
            ("MVA_Limit_B", "LineAMVA:1", 0, pw2py_default),
            ("MVA_Limit_C", "LineAMVA:2", 0, pw2py_default),
            ("p1", "LineMW", 0, pw2py_default),
            ("q1", "LineMVR", 0, pw2py_default),
            ("p2", "LineMW:1", 0, pw2py_default),
            ("q2", "LineMVR:1", 0, pw2py_default),
            ("availability", "CustomInteger", 0, pw2py_default)
        ]

        self.shunt_pw_fields = [
            ("status","SSStatus", True, pw2py_closed),
            ("qnom", "SSNMVR", 0, pw2py_default),
            ("q", "SSAMVR", 0, pw2py_default),
            ("availability", "CustomInteger", 0, pw2py_default)
        ]

    def clear(self):
        self.bus_map = OrderedDict()

    def bus(self, number):
        if number in self.bus_map:
            return self.bus_map[number]

    def buses(self):
        return (bus for bus in self.bus_map.values())

    def gen(self, bus_number, id):
        bus = self.bus(bus_number)
        if bus is not None:
            return bus.gen(id)

    def gens(self):
        return (gen for bus in self.buses() for gen in bus.gens())

    def load(self, bus_number, id):
        bus = self.bus(bus_number)
        if bus is not None:
            return bus.load(id)

    def loads(self):
        return (load for bus in self.buses() for load in bus.loads())

    def branch(self, from_bus_number, to_bus_number, id):
        from_bus = self.bus(from_bus_number)
        if from_bus is not None:
            return from_bus.branch_from(to_bus_number, id)
    
    def branches(self):
        return (branch for bus in self.buses() for branch in bus.branches_from())

    def shunt(self, bus_number, id):
        bus = self.bus(bus_number)
        if bus is not None:
            return bus.shunt(id)

    def shunts(self):
        return (shunt for bus in self.buses() for shunt in bus.shunts())

    def saw_read_all(self, s):

        bus_df = s.GetParametersMultipleElement("bus", 
            ["BusNum"] + [f[1] for f in self.bus_pw_fields])
        for i in range(len(bus_df)):
            bus_info = bus_df.loc[i, :]
            bus_num = bus_info["BusNum"]
            bus = self.bus(bus_num)
            if bus is None:
                bus = Bus(self, bus_num)
            for f in self.bus_pw_fields:
                setattr(bus, f[0], f[3](bus_info[f[1]]))

        gen_df = s.GetParametersMultipleElement("gen", 
            ["BusNum", "GenID"] + [f[1] for f in self.gen_pw_fields])
        for i in range(len(gen_df)):
            gen_info = gen_df.loc[i, :]
            gen_bus_num = gen_info["BusNum"]
            gen_id = gen_info["GenID"]
            gen = self.gen(gen_bus_num, gen_id)
            if gen is None:
                bus = self.bus(gen_bus_num)
                gen = Gen(bus, gen_id)
            for f in self.gen_pw_fields:
                setattr(gen, f[0], f[3](gen_info[f[1]]))

        load_df = s.GetParametersMultipleElement("load", 
            ["BusNum", "LoadID"] + [f[1] for f in self.load_pw_fields])
        for i in range(len(load_df)):
            load_info = load_df.loc[i, :]
            load_bus_num = load_info["BusNum"]
            load_id = load_info["LoadID"]
            load = self.load(load_bus_num, load_id)
            if load is None:
                bus = self.bus(load_bus_num)
                load = Load(bus, load_id)
            for f in self.load_pw_fields:
                setattr(load, f[0], f[3](load_info[f[1]]))

        branch_df = s.GetParametersMultipleElement("branch", 
            ["BusNum", "BusNum:1", "LineCircuit"] 
            + [f[1] for f in self.branch_pw_fields])
        for i in range(len(branch_df)):
            branch_info = branch_df.loc[i, :]
            from_bus_num = branch_info["BusNum"]
            to_bus_num = branch_info["BusNum:1"]
            branch_id = branch_info["LineCircuit"]
            branch = self.branch(from_bus_num, to_bus_num, branch_id)
            if branch is None:
                from_bus = self.bus(from_bus_num)
                to_bus = self.bus(to_bus_num)
                branch = Branch(from_bus, to_bus, branch_id)
            for f in self.branch_pw_fields:
                setattr(branch, f[0], f[3](branch_info[f[1]]))

        shunt_df = s.GetParametersMultipleElement("shunt", 
            ["BusNum", "ShuntID"] + [f[1] for f in self.shunt_pw_fields])
        for i in range(len(shunt_df)):
            shunt_info = shunt_df.loc[i, :]
            shunt_bus_num = shunt_info["BusNum"]
            shunt_id = shunt_info["ShuntID"]
            shunt = self.shunt(shunt_bus_num, shunt_id)
            if shunt is None:
                bus = self.bus(shunt_bus_num)
                shunt = Shunt(bus, shunt_id)
            for f in self.shunt_pw_fields:
                setattr(shunt, f[0], f[3](shunt_info[f[1]]))

    def saw_write_all(self, s):
        self.saw_write_data(s, buses=self.buses(), loads=self.loads(),
            gens=self.gens(), branches=self.branches(),
            shunts=self.shunts())
    
    def saw_write_data(self, s, buses=None, loads=None, gens=None, branches=None,
        shunts=None):
        if buses is not None:
            buses = tuple(buses)
            bus_data = {
                f[1]:[getattr(bus, f[0]) for bus in buses]
                for f in self.bus_pw_fields
            }
            bus_data["BusNum"] = [bus.number for bus in buses]
            bus_df = pd.DataFrame.from_dict(bus_data)
            s.change_parameters_multiple_element_df("bus", bus_df)

        if gens is not None:
            gens = tuple(gens)
            gen_data = {
                f[1]:[getattr(gen, f[0]) for gen in gens]
                for f in self.gen_pw_fields
            }
            gen_data["BusNum"] = [gen.bus.number for gen in gens]
            gen_data["GenID"] = [gen.id for gen in gens]
            gen_df = pd.DataFrame.from_dict(gen_data)
            s.change_parameters_multiple_element_df("gen", gen_df)

        if loads is not None:
            loads = tuple(loads)
            load_data = {
                f[1]:[getattr(load, f[0]) for load in loads]
                for f in self.load_pw_fields
            }
            load_data["BusNum"] = [load.bus.number for load in loads]
            load_data["LoadID"] = [load.id for load in loads]
            load_df = pd.DataFrame.from_dict(load_data)
            s.change_parameters_multiple_element_df("load", load_df)

        if branches is not None:
            branches = tuple(branches)
            branch_data = {
                f[1]:[getattr(branch, f[0]) for branch in branches]
                for f in self.branch_pw_fields
            }
            branch_data["BusNum"] = [branch.from_bus.number for branch in branches]
            branch_data["BusNum:1"] = [branch.to_bus.number for branch in branches]
            branch_data["LineCircuit"] = [branch.id for branch in branches]
            branch_df = pd.DataFrame.from_dict(branch_data)
            s.change_parameters_multiple_element_df("branch", branch_df)

        if shunts is not None:
            shunts = tuple(shunts)
            shunt_data = {
                f[1]:[getattr(shunt, f[0]) for shunt in shunts]
                for f in self.shunt_pw_fields
            }
            shunt_data["BusNum"] = [shunt.bus.number for shunt in shunts]
            shunt_data["ShuntID"] = [shunt.id for shunt in shunts]
            shunt_df = pd.DataFrame.from_dict(shunt_data)
            s.change_parameters_multiple_element_df("shunt", shunt_df)