import numpy as np
import pandas as pd
import sympy as sym
import matplotlib.pyplot as plt
from control.matlab import *
from collections import Counter
import sys
# from Basic_blocks import *


def RL_full(df_RL, df_RLC, w):
    """
    Form all RL classes

    :param df_RL: full data of RL, straight from the .xlsx file
    :param df_RLC: data of RLC pi models, to input their RL
    :param w: pulsation, in rad/s
    :return: it builds the state space with the corresponding names
    """

    class RL_particular:
        """
        Class for a particular RL, to be used in the RL_full class

        :param df_line: row of the full RL dataframe
        :param w: pulsation, in rad/s
        :return: the state space and the names, also stores the R and L values
        """

        def __init__(self, df_line, w):
            self.name = df_line['name']
            self.R = df_line['R']
            self.L = df_line['L']
            self.bus_i = str(df_line['bus i'])
            self.bus_j = str(df_line['bus j'])

            if self.bus_i == self.bus_j:  # if it is a load
                self.A = [[-self.R / self.L, -w], [w, -self.R / self.L]]
                self.B = [[1 / self.L, 0], [0, 1 / self.L]]
                self.C = [[1, 0], [0, 1]]
                self.D = [[0, 0], [0, 0]]
                self.ssm = ss(self.A, self.B, self.C, self.D)

                self.inputs = ['vq_'+self.bus_i, 'vd_'+self.bus_i]
                self.outputs = ['iq_'+self.bus_i+'_'+self.bus_j, 'id_'+self.bus_i+'_'+self.bus_j]
                self.states = ['iq_'+self.bus_i+'_'+self.bus_j, 'id_'+self.bus_i+'_'+self.bus_j]

            else:  # if it is not a load, but a line
                self.A = [[-self.R / self.L, -w], [w, -self.R / self.L]]
                self.B = [[1 / self.L, 0, -1 / self.L, 0], [0, 1 / self.L, 0, -1 / self.L]]
                self.C = [[1, 0], [0, 1]]
                self.D = [[0, 0, 0, 0], [0, 0, 0, 0]]
                self.ssm = ss(self.A, self.B, self.C, self.D)

                self.inputs = ['vq_'+self.bus_i, 'vd_' +
                    self.bus_i, 'vq_'+self.bus_j, 'vd_'+self.bus_j]
                self.outputs = ['iq_'+self.bus_i+'_' +
                    self.bus_j, 'id_'+self.bus_i+'_'+self.bus_j]
                self.states = ['iq_'+self.bus_i+'_' +
                    self.bus_j, 'id_'+self.bus_i+'_'+self.bus_j]

    RLs = [RL_particular(df_RL.iloc[ll, :], w) for ll in range(len(df_RL))]
    RLs += [RL_particular(df_RLC.iloc[ll, :], w) for ll in range(len(df_RLC))]

    return RLs


def RLC_full(df_RLC, w):
    """
    Form all C classes, to output the voltages only

    :param df_RLC: full data of RLC, straight from the .xlsx file
    :param w: pulsation, in rad/s
    :return: it builds the state space with the corresponding names
    """


    class C_particular:
        """
        Class for a particular capacitor to output its particular voltage

        :param df_line: row of the full RLC dataframe
        :param w: pulsation, in rad/s
        :param summed_C: value of the added capacitors at this bus
        :return: the state space and the names, also stores the C value
        """

        def __init__(self, bus, w, summed_C):
            self.bus = bus
            self.C = summed_C


            self.A = [
                [0, -w],
                [w, 0]
            ]
            self.B = [
                [1 / self.C, 0],
                [0, 1 / self.C]
            ]
            self.C = [
                [1, 0],
                [0, 1]
            ]
            self.D = [
                [0, 0],
                [0, 0]
            ]

            self.ssm = ss(self.A, self.B, self.C, self.D)

            self.inputs = ['iqx_'+str(self.bus), 'idx_'+str(self.bus)]
            self.outputs = ['vq_'+str(self.bus), 'vd_'+str(self.bus)]
            self.states = ['vq_'+str(self.bus), 'vd_'+str(self.bus)]



    def sum_C(df_RLC):
        """
        Adds all the capacitors placed in the same bus
        :param df_RLC: dataframe of the RLC sheet
        :return: dictionary bus : C value
        """

        summed_C = dict()
        for ll in range(len(df_RLC)):
            if df_RLC['bus i'][ll] in summed_C:
                summed_C[df_RLC['bus i'][ll]] += df_RLC['C'][ll]
            else:
                summed_C[df_RLC['bus i'][ll]] = df_RLC['C'][ll]

            if df_RLC['bus j'][ll] in summed_C:
                summed_C[df_RLC['bus j'][ll]] += df_RLC['C'][ll]
            else:
                summed_C[df_RLC['bus j'][ll]] = df_RLC['C'][ll]

        return summed_C


    def build_C(row, w, done_V, summed_C):
        """
        Builds the full Cs classes according to the already expressed as output voltages

        :param row: row of the form: df_RLC.iloc[ll, :]
        :param w: pulsation in rad/s
        :param done_V: vector that stores the index of the bus if it has been already used as an output
        :param summed_C: vector with sums of capacitors at each bus
        :return: row of the full class structure to append and updated done_V object
        """
        error = False
        if row['bus i'] not in done_V:
            RLC_row = C_particular(int(row['bus i']), w, summed_C[int(row['bus i'])])
            done_V.append(int(row['bus i']))
        elif row['bus j'] not in done_V:
            RLC_row = C_particular(int(row['bus j']), w, summed_C[int(row['bus j'])])
            done_V.append(int(row['bus j']))
        else:
            error = True

        return RLC_row, done_V, error


    summed_C = sum_C(df_RLC)
    done_V = []
    RLCs = []
    for ll in range(len(df_RLC)):
        RLC_row, done_V, error = build_C(df_RLC.iloc[ll, :], w, done_V, summed_C)
        if error is False:
            RLCs.append(RLC_row)

    return RLCs


def Other_full(df_other):

    def build_ss_others(df_other):
        """
        Parses the A, B, C, D matrices from the dataframe

        :param df_other: full dataframe for a 'rare' element
        :return: the full state space built with the control library
        """

        indx_A = df_other['name'].values.tolist().index('A')
        indx_B = df_other['name'].values.tolist().index('B')
        indx_C = df_other['name'].values.tolist().index('C')
        indx_D = df_other['name'].values.tolist().index('D')

        indx_col = df_other.columns.get_loc('name')

        # number of states, inputs, outputs
        n_x = len(list_non_nan(
            df_other.loc[df_other['name'] == 'A'].values[0].tolist()[indx_col + 1:]))
        n_i = len(list_non_nan(
            df_other.loc[df_other['name'] == 'B'].values[0].tolist()[indx_col + 1:]))
        n_o = len(df_other) - indx_D

        A = df_other.iloc[indx_A:indx_A + n_x,
            indx_col + 1: indx_col + 1 + n_x].values
        B = df_other.iloc[indx_B:indx_B + n_x,
            indx_col + 1: indx_col + 1 + n_i].values
        C = df_other.iloc[indx_C:indx_C + n_o,
            indx_col + 1: indx_col + 1 + n_x].values
        D = df_other.iloc[indx_D:indx_D + n_o,
            indx_col + 1: indx_col + 1 + n_i].values

        ssm = ss(A, B, C, D)

        return ssm

    def build_names(input_var, input_bus, output_var, output_bus, state_var, state_bus):
        """
        Creates the names of the magntidues in a full string fashion from the buses and variables

        :param input_var: list of input magnitudes (for now, either 'V' or 'I')
        :param input_bus: bus of the voltage or branch busi_busj for the current
        :param output_var: list of output magnitudes (for now, either 'V' or 'I')
        :param output_bus: bus of the voltage or branch busi_busj for the current
        :param state_var: list of state magnitudes (for now, either 'V' or 'I')
        :param state_bus: bus of the voltage or branch busi_busj for the current
        :return: the names of the inputs, outputs and states correctly presented
        """

        name_inputs = []
        name_outputs = []
        name_states = []

        for ll in range(len(input_var)):
            if input_var[ll] == 'V':
                name_inputs.append('vq_'+str(int(input_bus[ll])))
                name_inputs.append('vd_'+str(int(input_bus[ll])))
            elif input_var[ll] == 'I':
                name_inputs.append('iq_'+str(input_bus[ll]))
                name_inputs.append('id_'+str(input_bus[ll]))

        for ll in range(len(output_var)):
            if output_var[ll] == 'V':
                name_outputs.append('vq_'+str(int(output_bus[ll])))
                name_outputs.append('vd_'+str(int(output_bus[ll])))
            elif output_var[ll] == 'I':
                name_outputs.append('iq_'+str(output_bus[ll]))
                name_outputs.append('id_'+str(output_bus[ll]))

        for ll in range(len(state_var)):
            if state_var[ll] == 'V':
                name_states.append('vq_'+str(int(state_bus[ll])))
                name_states.append('vd_'+str(int(state_bus[ll])))
            elif state_var[ll] == 'I':
                name_states.append('iq_'+str(state_bus[ll]))
                name_states.append('id_'+str(state_bus[ll]))

        return name_inputs, name_outputs, name_states

    """
    Form all 'rare' state spaces entered by the used

    :param df_other: full sheet of the rare ss, straight from the .xlsx file
    :param w: pulsation, in rad/s
    :return: it builds the state space with the corresponding names
    """

    names = list_non_nan(df_other['name'].values.tolist())
    input_var = list_non_nan(df_other['input Mag.'].values.tolist())
    input_bus = list_non_nan(df_other['input Bus'].values.tolist())
    output_var = list_non_nan(df_other['output Mag.'].values.tolist())
    output_bus = list_non_nan(df_other['output Bus'].values.tolist())
    state_var = list_non_nan(df_other['state Mag.'].values.tolist())
    state_bus = list_non_nan(df_other['state Bus'].values.tolist())
    bus_i = int(df_other['bus i'].values.tolist()[0])
    bus_j = int(df_other['bus j'].values.tolist()[0])

    ins, outs, sts = build_names(
        input_var, input_bus, output_var, output_bus, state_var, state_bus)
    ssm = build_ss_others(df_other)

    class Others_particular:
            """
            Class for a particular 'others' object

            :param ssm: full state space previously created
            :param ins: names of the inputs
            :param outs: names of the outputs
            :param sts: names of the states
            :return: store the ss and its names in a structure
            """

            def __init__(self, ssm, ins, outs, sts, bus_i, bus_j):
                self.ssm = ssm
                self.inputs = ins
                self.outputs = outs
                self.states = sts
                self.bus_i = bus_i
                self.bus_j = bus_j

    # by now, only 1 element
    Other = [Others_particular(ssm, ins, outs, sts, bus_i, bus_j)]

    return Other


def Other_full_direct(df_other):

    def build_ss_others(df_other):
        """
        Parses the A, B, C, D matrices from the dataframe

        :param df_other: full dataframe for a 'rare' element
        :return: the full state space built with the control library
        """

        indx_A = df_other['name'].values.tolist().index('A')
        indx_B = df_other['name'].values.tolist().index('B')
        indx_C = df_other['name'].values.tolist().index('C')
        indx_D = df_other['name'].values.tolist().index('D')

        indx_col = df_other.columns.get_loc('name')

        # number of states, inputs, outputs
        n_x = len(list_non_nan(
            df_other.loc[df_other['name'] == 'A'].values[0].tolist()[indx_col + 1:]))
        n_i = len(list_non_nan(
            df_other.loc[df_other['name'] == 'B'].values[0].tolist()[indx_col + 1:]))
        n_o = len(df_other) - indx_D

        A = df_other.iloc[indx_A:indx_A + n_x,
            indx_col + 1: indx_col + 1 + n_x].values
        B = df_other.iloc[indx_B:indx_B + n_x,
            indx_col + 1: indx_col + 1 + n_i].values
        C = df_other.iloc[indx_C:indx_C + n_o,
            indx_col + 1: indx_col + 1 + n_x].values
        D = df_other.iloc[indx_D:indx_D + n_o,
            indx_col + 1: indx_col + 1 + n_i].values

        ssm = ss(A, B, C, D)

        return ssm

    """
    Form all 'rare' state spaces entered by the used. Assumes the user enters correctly the names

    :param df_other: full sheet of the rare ss, straight from the .xlsx file
    :param w: pulsation, in rad/s
    :return: it builds the state space with the corresponding names
    """

    names = list_non_nan(df_other['name'].values.tolist())
    input_var = list_non_nan(df_other['input Mag.'].values.tolist())
    output_var = list_non_nan(df_other['output Mag.'].values.tolist())
    state_var = list_non_nan(df_other['state Mag.'].values.tolist())
    ext_input = list_non_nan(df_other['ext. input'].values.tolist())
    ext_output = list_non_nan(df_other['ext. output'].values.tolist())
    bus_i = int(df_other['bus i'].values.tolist()[0])
    bus_j = int(df_other['bus j'].values.tolist()[0])

    # ins, outs, sts = build_names(input_var, input_bus, output_var, output_bus, state_var, state_bus)
    ins, outs, sts = input_var, output_var, state_var
    ssm = build_ss_others(df_other)

    class Others_particular:
            """
            Class for a particular 'others' object

            :param ssm: full state space previously created
            :param ins: names of the inputs
            :param outs: names of the outputs
            :param sts: names of the states
            :return: store the ss and its names in a structure
            """

            def __init__(self, ssm, ins, outs, sts, bus_i, bus_j):
                self.ssm = ssm
                self.inputs = ins
                self.outputs = outs
                self.states = sts
                self.bus_i = bus_i
                self.bus_j = bus_j

    # by now, only 1 element
    Other = [Others_particular(ssm, ins, outs, sts, bus_i, bus_j)]

    return Other, ext_input, ext_output


def I_balance(RLs, VSCs):
    """
    Form the state space for the current balances in repeated buses

    :param RLs: class with all the information about RLs
    :param VSCs: class with all the information about VSCs
    :return: it builds the state space with the corresponding names
    """

    class Isum_particular:
        """
        Class for a particular current balance object

        :param ssm: full state space previously created
        :param ins: names of the inputs
        :param outs: names of the outputs
        :param sts: names of the states
        :return: store the ss and its names in a structure
        """

        def __init__(self, ssm, ins, outs, sts):
            self.ssm = ssm
            self.inputs = ins
            self.outputs = outs
            self.states = sts

    I_sum = []  # list of classes

    # analyze buses
    bus_i_list = []
    bus_j_list = []
    bus_vsc_list = []

    for ll in range(len(RLs)):
        bus_i_list.append(int(RLs[ll].bus_i))
        bus_j_list.append(int(RLs[ll].bus_j))

    for ll in range(len(VSCs)):
        bus_vsc_list.append(int(VSCs[ll].bus_ac))


    merged_list = [*bus_i_list, *bus_j_list, *bus_vsc_list]
    dic_occ = Counter(merged_list)  # dictionary of occurrences of each bus
    list_buses = list(dict.keys(dic_occ))

    buses_repeated = []
    for key in list_buses:
        if dic_occ[key] > 1:
            buses_repeated.append(key)


    # current balance
    for bus_x in buses_repeated:
        states_Isum = []
        inputs_Isum = []
        outputs_Isum = []
        D_array_q = []  # upper row
        D_array_d = []  # lower row
        # perform search to find pairs of buses where there is a repeated bus
        for kk in range(len(bus_i_list)):  # for RLs
            if bus_i_list[kk] == bus_x:
                D_array_q.append(-1)
                D_array_q.append(0)
                D_array_d.append(0)
                D_array_d.append(-1)
                inputs_Isum.append(['iq_'+str(bus_i_list[kk])+'_'+str(bus_j_list[kk]),
                               'id_'+str(bus_i_list[kk])+'_'+str(bus_j_list[kk])])
            elif bus_j_list[kk] == bus_x:
                D_array_q.append(+1)
                D_array_q.append(0)
                D_array_d.append(0)
                D_array_d.append(+1)
                inputs_Isum.append(['iq_'+str(bus_i_list[kk])+'_'+str(bus_j_list[kk]),
                               'id_'+str(bus_i_list[kk])+'_'+str(bus_j_list[kk])])
        for kk in range(len(bus_vsc_list)):  # for VSCs, current always entering
            if bus_vsc_list[kk] == bus_x:
                D_array_q.append(-1)
                D_array_q.append(0)
                D_array_d.append(0)
                D_array_d.append(-1)
                inputs_Isum.append(['iqxv_'+str(bus_vsc_list[kk]),
                                'idxv_'+str(bus_vsc_list[kk])])

        inputs_Isum = [item for sublist in inputs_Isum for item in sublist]


        D_array = [D_array_q, D_array_d]
        outputs_Isum.append(['iqx_'+str(bus_x), 'idx_'+str(bus_x)])
        outputs_Isum = [item for sublist in outputs_Isum for item in sublist]

        states_Isum = []

        A_Isum = [[]]
        B_Isum = [[]]
        C_Isum = [[]]
        D_Isum = D_array
        ss_Isum = ss(A_Isum, B_Isum, C_Isum, D_Isum)

        I_sum.append(Isum_particular(
            ss_Isum, inputs_Isum, outputs_Isum, states_Isum))


    return I_sum


def list_non_nan(list):
    """
    Looks for a NaN entry and returns the list before it

    :param list: list where we have to search
    :return: index of the first NaN entry
    """

    indx = 0
    found = False
    ll = 0

    while found is False or ll > len(list):
        if pd.isnull(list[ll]) is True:
            found = True
            indx = ll
        ll += 1

    return list[:indx]


def all_names(*ss_class):
    """
    Creates a full string of inputs, outputs and states from all classes

    :param ss_class: tuple of all classes
    :return: list of inputs, outputs and states
    """

    full_inputs = [sub_cl.inputs for cl in ss_class for sub_cl in cl]
    full_outputs = [sub_cl.outputs for cl in ss_class for sub_cl in cl]
    full_states = [sub_cl.states for cl in ss_class for sub_cl in cl]

    full_inputs = [item for sublist in full_inputs for item in sublist]
    full_outputs = [item for sublist in full_outputs for item in sublist]
    full_states = [item for sublist in full_states for item in sublist]

    return full_inputs, full_outputs, full_states


def adapt_in_outs(full_inputs, full_outputs):
    """
    Changes names of inputs and creates the associated ss of the division

    :param full_inputs: list of all the input names
    :param full_outputs: list of all the outputs names
    :return: modified list of input names, full list of output names with the division additions and the class with the ss of the division
    """

    # append _Tx in the name of the repeated variables
    dic_occ = Counter(full_inputs)
    dic_repeated = {}
    for key in dic_occ:
        if dic_occ[key] > 1:
            dic_repeated[key] = 0

    for ll in range(len(full_inputs)):
        if full_inputs[ll] in dic_repeated.keys():
            dic_repeated[full_inputs[ll]] += 1
            full_inputs[ll] = full_inputs[ll]+'_T'+str(dic_repeated[full_inputs[ll]])

    # create ss classes
    class Xdiv_particular:
        """
        Class for a particular variable division object

        :param ssm: full state space previously created
        :param ins: names of the inputs
        :param outs: names of the outputs
        :param sts: names of the states
        :return: store the ss and its names in a structure
        """

        def __init__(self, ssm, ins, outs, sts):
            self.ssm = ssm
            self.inputs = ins
            self.outputs = outs
            self.states = sts

    Xdivs = []  # list of classes

    for key in dic_repeated:
        A = [[]]
        B = [[]]
        C = [[]]
        Dd = [[1]] * dic_repeated[key]
        ssm = ss(A, B, C, Dd)
        inputs = [key]
        outputs = []
        for ll in range(dic_repeated[key]):
            outputs.append(key+'_T'+str(ll + 1))
            full_outputs.append(outputs[-1])
        states = []
        full_inputs.append(key)
        Xdivs.append(Xdiv_particular(ssm, inputs, outputs, states))

    return full_inputs, full_outputs, Xdivs


class Net:
    """
    Full class where the subclasses such as RLs, RLCs... are stored

    :param clss: a given class, among many
    :return: nothing, basically store all classes in the same object
    """

    def __init__(self, RLs, RLCs):  # enter the meaningful classes, not Isum and similars
        self.RLs = RLs
        self.RLCs = RLCs


def names_ext_in_outs(df_ext_inputs, df_ext_outputs):
    """
    Converts the info in the dataframe to the right names for inputs and outputs

    :param df_ext_inputs: full dataframe of external inputs
    :param df_ext_outputs: full dataframe of external outputs
    :return: list of names of inputs and outputs
    """

    full_ext_inputs = []
    for ll in range(len(df_ext_inputs)):
        if df_ext_inputs['Magnitude'][ll] == 'I':
            full_ext_inputs.append('iqx_'+str(df_ext_inputs['Bus'][ll]))
            full_ext_inputs.append('idx_'+str(df_ext_inputs['Bus'][ll]))
        elif df_ext_inputs.iloc[ll, 0] == 'V':
            full_ext_inputs.append('vq_'+str(df_ext_inputs['Bus'][ll]))
            full_ext_inputs.append('vd_'+str(df_ext_inputs['Bus'][ll]))

    full_ext_outputs = []
    for ll in range(len(df_ext_outputs)):
        if df_ext_outputs['Magnitude'][ll] == 'I':
            full_ext_outputs.append('iq_'+str(df_ext_outputs['Bus'][ll]))
            full_ext_outputs.append('id_'+str(df_ext_outputs['Bus'][ll]))
        elif df_ext_outputs['Magnitude'][ll] == 'V':
            full_ext_outputs.append('vq_'+str(df_ext_outputs['Bus'][ll]))
            full_ext_outputs.append('vd_'+str(df_ext_outputs['Bus'][ll]))

    return full_ext_inputs, full_ext_outputs


def dics_in_out_sts(full_inputs, full_outputs, full_states):
    """
    Builds dictionaries for inputs, outputs and states, to pass to Qvec_builder_full

    :param full_inputs: full list of inputs
    :param full_outputs: full list of outputs
    :param full_states: full list of states
    :return: dictionaries for inputs, outputs and states
    """

    dic_inputs = {}
    for ll in range(len(full_inputs)):
        dic_inputs[full_inputs[ll]] = ll + 1

    dic_outputs = {}
    for ll in range(len(full_outputs)):
        dic_outputs[full_outputs[ll]] = ll + 1

    dic_states = {}
    for ll in range(len(full_states)):
        dic_states[full_states[ll]] = ll + 1

    return dic_inputs, dic_outputs, dic_states


def Qvec_builder_full(name_in, name_out, dic_i, dic_o, dic_x):
    '''
    Generates the Qq array and the name of inputs and outputs. To be used just before the final connect

    :param name_in: list of the input names
    :param name_out: list of the otput names
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final Qq array for the connect, and the lists of names and indices of states, inputs and outputs
    '''

    Qq = []
    list_indx_x = []
    list_indx_in = [dic_i[name_in[ll]] for ll in range(len(name_in))]
    list_indx_out = [dic_o[name_out[ll]] for ll in range(len(name_out))]
    list_name_x = []
    list_name_in = [name_in[ll] for ll in range(len(name_in))]
    list_name_out = [name_out[ll] for ll in range(len(name_out))]

    for ll in range(len(dic_i)):
        name_key_in = list(dic_i.keys())[ll]
        if name_key_in in list(dic_o.keys())[:]:
            vec_Q = [dic_i[name_key_in], dic_o[name_key_in]]
        else:
            vec_Q = [dic_i[name_key_in], 0]
        Qq.append(vec_Q)

    for ll in range(len(dic_x)):
        name_key_x = list(dic_x.keys())[ll]
        list_indx_x.append(dic_x[name_key_x])
        list_name_x.append(list(dic_x.keys())[ll])

    return Qq, list_indx_x, list_indx_in, list_indx_out, list_name_x, list_name_in, list_name_out


def FPrinter(ss_all, list_name_x0, list_name_in0, list_name_out0, prnt):
    '''
    Print the state space with the names

    :param ss_all: full state space representation
    :param list_name_x0: list of states names
    :param list_name_in0: list of inputs names
    :param list_name_out0: list of outputs names
    :param prnt: boolean to print or not
    :return: nothing, only prints
    '''

    mA = ss_all.A
    mB = ss_all.B
    mC = ss_all.C
    mD = ss_all.D

    dfA = pd.DataFrame(mA)
    dfB = pd.DataFrame(mB)
    dfC = pd.DataFrame(mC)
    dfD = pd.DataFrame(mD)

    list_name_x = []
    list_name_in = []
    list_name_out = []

    for ll in range(len(list_name_x0)):
        list_name_x.append(list_name_x0[ll])

    for ll in range(len(list_name_in0)):
        list_name_in.append(list_name_in0[ll])

    for ll in range(len(list_name_out0)):
        list_name_out.append(list_name_out0[ll])

    dfA_row = pd.DataFrame(list_name_x).T
    dfA = dfA_row.append(dfA)

    dfB_row = pd.DataFrame(list_name_in).T
    dfB = dfB_row.append(dfB)

    dfC_row = pd.DataFrame(list_name_x).T
    dfC = dfC_row.append(dfC)

    dfD_row = pd.DataFrame(list_name_in).T
    dfD = dfD_row.append(dfD)

    list_name_xa = list_name_x
    list_name_xa.insert(0, 'Identifier')
    dfA.insert(loc=0, column='t', value=list_name_xa)

    list_name_xb = list_name_x
    dfB.insert(loc=0, column='t', value=list_name_xb)

    if len(list_name_x0) > 0:
        list_name_xc = list_name_out
        list_name_xc.insert(0, 'Identifier')
        dfC.insert(loc=0, column='t', value=list_name_xc)
    else:
        new_list = []
        # new_list.append('Identifier')
        for ll in range(len(list_name_out)):
            new_list.append(list_name_out[ll])
        dfC['Identifier'] = new_list


    if len(list_name_x0) > 0:
        list_name_xd = list_name_out
        dfD.insert(loc=0, column='t', value=list_name_xd)
    else:
        list_name_xd = list_name_out
        list_name_xd.insert(0, 'Identifier')
        dfD.insert(loc=0, column='t', value=list_name_xd)


    if prnt is True:
        print('\n')
        print('A:')
        print(dfA.to_string(index=False, header=False))
        print('\n')
        print('B:')
        print(dfB.to_string(index=False, header=False))
        print('\n')
        print('C:')
        print(dfC.to_string(index=False, header=False))
        print('\n')
        print('D:')
        print(dfD.to_string(index=False, header=False))

    # write in excel
    writer = pd.ExcelWriter('results/solution_good.xlsx')
    dfA.to_excel(writer, 'A')
    dfB.to_excel(writer, 'B')
    dfC.to_excel(writer, 'C')
    dfD.to_excel(writer, 'D')
    writer.save()

    return dfA, dfB, dfC, dfD


def CSystem(excel_file):
    """
    Creates the full state space of a complete system
    VSC and SG to be done

    :param excel_file: .xlsx file with multiple sheets
    :return: the final state space witht he corresponding names
    """


    # 0. initialization
    xlsx = pd.ExcelFile(excel_file)
    df_global = pd.read_excel(xlsx, 'Global')
    df_ext_inputs = pd.read_excel(xlsx, 'External_inputs')
    df_ext_outputs = pd.read_excel(xlsx, 'External_outputs')
    df_RL = pd.read_excel(xlsx, 'RL')
    df_RLC = pd.read_excel(xlsx, 'RLC')
    df_other = pd.read_excel(xlsx, 'Others')
    df_VSC = pd.read_excel(xlsx, 'VSC')
    df_SG = pd.read_excel(xlsx, 'SG')

    w = df_global['w (rad/s)'].values[0]
    Sb = df_global['S base (MVA)'].values[0]
    # Vb = df_global['V base (kV)'].values[0]

    # many lines commented because I exclude Others for the annakkage system

    # 1. parser
    RLs = RL_full(df_RL, df_RLC, w)
    Cs = RLC_full(df_RLC, w)
    VSCs = VSC_full(df_VSC, w)
    SGs = SG_full(df_SG, w)
    # Other, other_ext_inputs, other_ext_outputs = Other_full_direct(df_other)  # assuming user enters correctly the names


    # ISum = I_balance(RLs, Other)  # exclude RLCs or any class where current is an input
    ISum = I_balance(RLs, VSCs)  # exclude RLCs or any class where current is an input


    # 2. merge everything, rename inputs/outputs/states if necessary
    # full_inputs, full_outputs, full_states = all_names(RLs, RLCs, Other, ISum)  # merge all ss up to this point
    # full_inputs, full_outputs, Xdivs = adapt_in_outs(full_inputs, full_outputs)  # where Xdivs is a class, to manage repeated names

    # print(VSCs[0].inputs_full)
    full_inputs, full_outputs, full_states = all_names(RLs, Cs, VSCs, ISum)  # merge all ss up to this point
    full_inputs, full_outputs, Xdivs = adapt_in_outs(full_inputs, full_outputs)  # where Xdivs is a class, to manage repeated names

    # 3. final connect
    # all_classes = [RLs, RLCs, Other, ISum, Xdivs]  # unify everything. Use the same order as before!
    # ext_inputs, ext_outputs = names_ext_in_outs(df_ext_inputs, df_ext_outputs)

    all_classes = [RLs, Cs, VSCs, ISum, Xdivs]  # unify everything. Use the same order as before!
    ext_inputs, ext_outputs = names_ext_in_outs(df_ext_inputs, df_ext_outputs)
    for ll in range(len(VSCs)):  # add external inputs from the VSC
        ext_inputs += VSCs[ll].ext_inputs
        ext_outputs += VSCs[ll].ext_outputs

    net_full = Net(RLs, Cs)

    # add the external from others, for full2
    # ext_inputs = ext_inputs + other_ext_inputs
    # ext_outputs = ext_outputs + other_ext_outputs

    # full system with appends
    ss_complete = []
    for cl in all_classes:
        for sub_cl in cl:
            ss_complete = append(ss_complete, sub_cl.ssm)

    dic_inputs, dic_outputs, dic_states = dics_in_out_sts(full_inputs, full_outputs, full_states)

    Qq, list_indx_x, list_indx_in, list_indx_out, list_name_x, list_name_in, list_name_out = Qvec_builder_full(ext_inputs, ext_outputs, dic_inputs, dic_outputs, dic_states)

    ss_final = connect(ss_complete, Qq, list_indx_in, list_indx_out)

    dfA, dfB, dfC, dfD = FPrinter(ss_final, list_name_x, list_name_in, list_name_out, prnt=False)  # to nicely print


    class ss_data:
        """
        Class where the most relevant final objects are stored
        """
        def __init__(self, ss_final, list_name_x, list_name_in, list_name_out):
            self.ss = ss_final
            self.list_name_x = list_name_x
            self.list_name_in = list_name_in
            self.list_name_out = list_name_out
            self.dic_x = {}
            self.dic_i = {}
            self.dic_o = {}

            for ll in range(len(self.list_name_x)):
                self.dic_x[self.list_name_x[ll]] = ll
            for ll in range(len(self.list_name_in)):
                self.dic_i[self.list_name_in[ll]] = ll
            for ll in range(len(self.list_name_out)):
                self.dic_o[self.list_name_out[ll]] = ll


    data_all = ss_data(ss_final, list_name_x, list_name_in, list_name_out)


    # 4. verify results, done
    # with Maple, for instance
    # print(net_full.RLs[0].inputs)  # for example

    # return data_all
    # return RLs, Cs, VSCs, SGs, data_all
    return RLs, Cs, VSCs, ISum, Xdivs, SGs, data_all


def VSC_full(df_VSC, w):
    """
    Form all VSCs classes

    :param df_VSC: full data of VSC, straight from the .xlsx file
    :param w: pulsation, in rad/s
    :return: it builds the state space with the corresponding names
    """

    class VSC_particular:
        """
        Class for a particular VSC

        :param df_VSC: row of the full VSC dataframe
        :param w: pulsation, in rad/s
        :param indx: index of the VSC, from 0 to n
        :return: the state space and the names, also stores the input values
        """


        class BP_outer:
            """
            Class for the active power outer loop

            :param indx: index of the VSC
            :param vcq0: equilibrium point for the q voltage
            :param vcd0: equilibrium point for the d voltage
            :param icq0: equilibrium point for the q current
            :param icd0: equilibrium point for the d current
            :param kp_f: proportional constant for the frequency control
            :param kp_p: proportional constant for the active power control
            :param ki_p: integral constant for the active power control
            :return: state space of the active power outer loop with the inputs, outputs, states
            """

            def __init__(self, indx, vcq0, vcd0, icq0, icd0, kp_f, kp_p, ki_p):
                # store variables in the structure
                self.indx = indx
                self.vcq0 = vcq0
                self.vcd0 = vcd0
                self.icq0 = icq0
                self.icd0 = icd0
                self.kp_f = kp_f
                self.kp_p = kp_p
                self.ki_p = ki_p

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # Active power calculation
                self.inputs_p = ['vcq_'+istr+'_P', 'vcd_'+istr+'_P', 'icq_'+istr+'_P', 'icd_'+istr+'_P']
                self.outputs_p = 'AP_c_'+istr
                self.ss_p, self.inputs, self.outputs, self.states = FP_active(self.inputs_p, self.outputs_p, self.vcq0, self.vcd0, self.icq0, self.icd0, self.indx, self.inputs, self.outputs, self.states)

                # print(self.ss_p)

                # # Sum of frequencies
                # self.inputs_s1 = ['w_c_'+istr, 'w_ref_'+istr]
                # self.sign_s1 = [-1, +1]
                # self.outputs_s1 = 'err_w_c_'+istr
                # self.ss_s1, self.inputs, self.outputs, self.states = FSum(self.inputs_s1, self.sign_s1, self.outputs_s1, self.indx, self.inputs, self.outputs, self.states)

                # # P controller
                # self.inputs_PI = 'err_w_c_'+istr
                # self.outputs_PI = 'err_P_'+istr
                # self.ss_PI, self.inputs, self.outputs, self.states = FP_controller(self.kp_f, self.inputs_PI, self.outputs_PI, self.indx, self.inputs, self.outputs, self.states)

                # Sum of powers
                # self.inputs_s2 = ['err_P_'+istr, 'Ap_ref_'+istr, 'AP_c_'+istr]
                self.inputs_s2 = ['Ap_ref_'+istr, 'AP_c_'+istr]
                # self.sign_s2 = [+1, +1, -1]
                self.sign_s2 = [+1, -1]
                self.outputs_s2 = 'diff_AP_'+istr
                self.ss_s2, self.inputs, self.outputs, self.states = FSum(self.inputs_s2, self.sign_s2, self.outputs_s2, self.indx, self.inputs, self.outputs, self.states)

                # PI controller
                self.inputs_PI2 = 'diff_AP_'+istr
                self.outputs_PI2 = 'icq_ref_'+istr
                self.ss_PI2, self.inputs, self.outputs, self.states = FPI_controller(self.ki_p, self.kp_p, self.inputs_PI2, self.outputs_PI2, self.indx, self.inputs, self.outputs, self.states)


                # Merge
                # self.ss_full = append(self.ss_p, self.ss_s1, self.ss_PI, self.ss_s2, self.ss_PI2)
                self.ss_full = append(self.ss_p, self.ss_s2, self.ss_PI2)
                self.inputs_full = ['vcq_'+istr+'_P', 'vcd_'+istr+'_P', 'icq_'+istr+'_P', 'icd_'+istr+'_P', 'Ap_ref_'+istr]  # removed w_ref
                self.outputs_full = ['icq_ref_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BQ_outer:
            """
            Class for the reactive power outer loop

            :param indx: index of the VSC
            :param vcq0: equilibrium point for the q voltage
            :param vcd0: equilibrium point for the d voltage
            :param icq0: equilibrium point for the q current
            :param icd0: equilibrium point for the d current
            :param kp_v: proportional constant for the voltage control
            :param ki_v: integral constant for the voltage control
            :param kp_q: proportional constant for the reactive power control
            :param ki_q: integral constant for the reactive power control
            :return: state space of the reactive power outer loop with the inputs, outputs, states
            """

            def __init__(self, indx, vcq0, vcd0, icq0, icd0, kp_v, ki_v, kp_q, ki_q):
                # store variables in the structure
                self.indx = indx
                self.vcq0 = vcq0
                self.vcd0 = vcd0
                self.icq0 = icq0
                self.icd0 = icd0
                self.kp_v = kp_v
                self.ki_v = ki_v
                self.kp_q = kp_q
                self.ki_q = ki_q

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)


                # division for q voltages
                # self.inputs_n1 = 'vcq_'+istr+'_Q'
                # self.outputs_n1 = ['vcq1_'+istr, 'vcq2_'+istr]
                # self.ss_n1, self.inputs, self.outputs, self.states = FNode(self.inputs_n1, self.outputs_n1, self.indx, self.inputs, self.outputs, self.states)

                # division of d voltages
                # self.inputs_n2 = 'vcd_'+istr+'_Q'
                # self.outputs_n2 = ['vcd1_'+istr, 'vcd2_'+istr]
                # self.ss_n2, self.inputs, self.outputs, self.states = FNode(self.inputs_n2, self.outputs_n2, self.indx, self.inputs, self.outputs, self.states)

                # ac voltage calculation
                # self.inputs_v = ['vcq1_'+istr, 'vcd1_'+istr]
                # self.outputs_v = 'v_full_'+istr
                # self.ss_v, self.inputs, self.outputs, self.states = FAC_voltage(self.inputs_v, self.outputs_v, self.vcq0, self.vcd0, self.indx, self.inputs, self.outputs, self.states)

                # Q active  calculation
                self.inputs_q = ['vcq_'+istr+'_Q', 'vcd_'+istr+'_Q', 'icq_'+istr+'_Q', 'icd_'+istr+'_Q']
                self.outputs_q = 'AQ_c_'+istr
                self.ss_q, self.inputs, self.outputs, self.states = FQ_active(self.inputs_q, self.outputs_q, self.vcq0, self.vcd0, self.icq0, self.icd0, self.indx, self.inputs, self.outputs, self.states)

                # sum on the voltage control side
                # self.inputs_s1 = ['v_full_'+istr, 'v_ref_'+istr]
                # self.sign_s1 = [-1, +1]
                # self.outputs_s1 = 'err_Av_'+istr
                # self.ss_s1, self.inputs, self.outputs, self.states = FSum(self.inputs_s1, self.sign_s1, self.outputs_s1, self.indx, self.inputs, self.outputs, self.states)

                # proportional controller on the voltage side
                # self.inputs_P = 'err_Av_'+istr
                # self.outputs_P = 'err_AQ_'+istr
                # self.ss_P, self.inputs, self.outputs, self.states = FP_controller(self.kp_v, self.inputs_P, self.outputs_P, self.indx, self.inputs, self.outputs, self.states)

                # sum on the Q control side
                # self.inputs_s2 = ['err_AQ_'+istr, 'Aq_ref_'+istr, 'AQ_c_'+istr]
                self.inputs_s2 = ['Aq_ref_'+istr, 'AQ_c_'+istr]
                # self.sign_s2 = [+1, +1, -1]
                self.sign_s2 = [+1, -1]
                self.outputs_s2 = 'diff_AQ_'+istr
                self.ss_s2, self.inputs, self.outputs, self.states = FSum(self.inputs_s2, self.sign_s2, self.outputs_s2, self.indx, self.inputs, self.outputs, self.states)

                # proportional integral controller
                self.inputs_PI = 'diff_AQ_'+istr
                self.outputs_PI = 'icd_ref_'+istr
                self.ss_PI, self.inputs, self.outputs, self.states = FPI_controller(self.ki_q, self.kp_q, self.inputs_PI, self.outputs_PI, self.indx, self.inputs, self.outputs, self.states)

                # Merge
                self.ss_full = append(self.ss_q, self.ss_s2, self.ss_PI)  # removed v_ref loop
                self.inputs_full = ['vcq_'+istr+'_Q', 'vcd_'+istr+'_Q', 'icq_'+istr+'_Q', 'icd_'+istr+'_Q', 'Aq_ref_'+istr]  # removed v_ref
                self.outputs_full = ['icd_ref_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BPLL:
            """
            Class for the PLL (the simple version, built directly)

            :param indx: index of the VSC
            :param kp_pll: proportional constant for the frequency tracking
            :param ki_pll: integral constant for the frequency tracking
            :return: state space of the PLL with the inputs, outputs, states
            """

            def __init__(self, indx, kp_pll, ki_pll):
                # store variables in the structure
                self.indx = indx
                self.kp_pll = kp_pll
                self.ki_pll = ki_pll

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # directly obtained ss
                A = [[0, 1], [0, 0]]
                B = [[0], [1]]
                C = [[-self.ki_pll, -self.kp_pll]]
                # C = [[-self.ki_pll, -self.kp_pll], [0, -self.ki_pll]]
                D = [[0]]
                # D = [[0], [-self.kp_pll]]

                self.ss_full = ss(A, B, C, D)

                self.states['PLL_etheta1_'+istr] = 1
                self.states['PLL_etheta2_'+istr] = 2
                self.inputs['vmd_'+istr+'_PLL'] = 1
                self.outputs['ang_'+istr] = 1
                # self.outputs['w_c_'+istr] = 2

                # Merge
                self.inputs_full = ['vmd_'+istr+'_PLL']
                self.outputs_full = ['ang_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BInnerCurrentLoop:
            """
            Class for the inner current control loop

            :param indx: index of the VSC
            :param w: pulsation in rad/s
            :param Lc: inductance value to be used in the decoupling
            :param kp_i: proportional parameter of the current loop controller
            :param ki_i: integral parameter of the current loop controller
            :return: state space of the inner current control loop with the inputs, outputs, states
            """

            def __init__(self, indx, w, Lc, kp_i, ki_i):
                # store variables in the structure
                self.indx = indx
                self.w = w
                self.Lc = Lc
                self.kp_i = kp_i
                self.ki_i = ki_i

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # division of the q current
                self.inputs_n1 = 'icq_'+istr+'_curr'
                self.outputs_n1 = ['icq_v1_'+istr, 'icq_v2_'+istr]
                self.ss_n1, self.inputs, self.outputs, self.states = FNode(self.inputs_n1, self.outputs_n1, self.indx, self.inputs, self.outputs, self.states)

                # division of the d current
                self.inputs_n2 = 'icd_'+istr+'_curr'
                self.outputs_n2 = ['icd_v1_'+istr, 'icd_v2_'+istr]
                self.ss_n2, self.inputs, self.outputs, self.states = FNode(self.inputs_n2, self.outputs_n2, self.indx, self.inputs, self.outputs, self.states)

                # comparator of q currents
                self.inputs_s1 = ['icq_ref_'+istr, 'icq_v1_'+istr]
                self.sign_s1 = [+1, -1]
                self.outputs_s1 = 'err_icq_'+istr
                self.ss_s1, self.inputs, self.outputs, self.states = FSum(self.inputs_s1, self.sign_s1, self.outputs_s1, self.indx, self.inputs, self.outputs, self.states)

                # comparator of d currents
                self.inputs_s2 = ['icd_ref_'+istr, 'icd_v1_'+istr]
                self.sign_s2 = [+1, -1]
                self.outputs_s2 = 'err_icd_'+istr
                self.ss_s2, self.inputs, self.outputs, self.states = FSum(self.inputs_s2, self.sign_s2, self.outputs_s2, self.indx, self.inputs, self.outputs, self.states)

                # PI controller for the q currents
                self.inputs_PI1 = 'err_icq_'+istr
                self.outputs_PI1 = 'err_vcq_'+istr
                self.ss_PI1, self.inputs, self.outputs, self.states = FPI_controller(self.ki_i, self.kp_i, self.inputs_PI1, self.outputs_PI1, self.indx, self.inputs, self.outputs, self.states)

                # PI controller for the d currents
                self.inputs_PI2 = 'err_icd_'+istr
                self.outputs_PI2 = 'err_vcd_'+istr
                self.ss_PI2, self.inputs, self.outputs, self.states = FPI_controller(self.ki_i, self.kp_i, self.inputs_PI2, self.outputs_PI2, self.indx, self.inputs, self.outputs, self.states)

                # product q component in the decoupling
                self.inputs_X1 = 'icq_v2_'+istr
                self.outputs_X1 = 'ixcq_'+istr
                self.ct_val = w * Lc
                self.ss_X1, self.inputs, self.outputs, self.states = FProduct(self.inputs_X1, self.ct_val, self.outputs_X1, self.indx, self.inputs, self.outputs, self.states)

                # product d component in the decoupling
                self.inputs_X2 = 'icd_v2_'+istr
                self.outputs_X2 = 'ixcd_'+istr
                self.ct_val = w * Lc
                self.ss_X2, self.inputs, self.outputs, self.states = FProduct(self.inputs_X2, self.ct_val, self.outputs_X2, self.indx, self.inputs, self.outputs, self.states)

                # final addition q component
                self.inputs_s3 = ['vcq_'+istr+'_curr', 'err_vcq_'+istr, 'ixcd_'+istr]
                self.sign_s3 = [+1, -1, -1]
                self.outputs_s3 = 'vcq_ref_'+istr
                self.ss_s3, self.inputs, self.outputs, self.states = FSum(self.inputs_s3, self.sign_s3, self.outputs_s3, self.indx, self.inputs, self.outputs, self.states)

                # final addition d component
                self.inputs_s4 = ['vcd_'+istr+'_curr', 'err_vcd_'+istr, 'ixcq_'+istr]
                self.sign_s4 = [+1, -1, +1]
                self.outputs_s4 = 'vcd_ref_'+istr
                self.ss_s4, self.inputs, self.outputs, self.states = FSum(self.inputs_s4, self.sign_s4, self.outputs_s4, self.indx, self.inputs, self.outputs, self.states)


                # Merge
                self.ss_full = append(self.ss_n1, self.ss_n2, self.ss_s1, self.ss_s2, self.ss_PI1, self.ss_PI2, self.ss_X1, self.ss_X2, self.ss_s3, self.ss_s4)
                self.inputs_full = ['icq_'+istr+'_curr', 'icd_'+istr+'_curr', 'icq_ref_'+istr, 'icd_ref_'+istr, 'vcq_'+istr+'_curr', 'vcd_'+istr+'_curr']
                self.outputs_full = ['vcq_ref_'+istr, 'vcd_ref_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BGd:
            """
            Class for the 1st order transfer function (the simple version, built directly)

            :param indx: index of the VSC
            :param k: k parameter of the transfer function
            :param tau: tau parameter of the transfer function
            :return: state space of the 1st order transfer cuntion with the inputs, outputs, states
            """

            def __init__(self, indx, k_gd, tau_gd):
                # store variables in the structure
                self.indx = indx
                self.k_gd = k_gd
                self.tau_gd = tau_gd

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # directly obtained ss
                A = [[- 1 / self.tau_gd, 0], [0, - 1 / self.tau_gd]]
                B = [[self.k_gd / self.tau_gd, 0], [0, self.k_gd / self.tau_gd]]
                C = [[1, 0], [0, 1]]
                D = [[0, 0], [0, 0]]

                self.ss_full = ss(A, B, C, D)

                self.inputs['vcq_ref_'+istr] = 1
                self.inputs['vcd_ref_'+istr] = 2
                self.outputs['vccq_'+istr] = 1
                self.outputs['vccd_'+istr] = 2
                self.states['int_vccq_ref_'+istr] = 1
                self.states['int_vccd_ref_'+istr] = 2

                # Merge
                self.inputs_full = ['vcq_ref_'+istr, 'vcd_ref_'+istr]
                self.outputs_full = ['vccq_'+istr, 'vccd_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BTv:
            """
            Park transformation for the voltages

            :param indx: index of the VSC
            :param xq0: equilibrium point for the q voltage
            :param xd0: equilibrium point for the d voltage
            :param ang0: equilibrium point for the angle
            :return: state space of the Park transformation for the voltages
            """

            def __init__(self, indx, xq0, xd0, ang0):
                # store variables in the structure
                self.indx = indx
                self.xq0 = xq0
                self.xd0 = xd0
                self.ang0 = ang0

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # directly obtained ss
                # A = [[0]]
                # B = [[0, 0, 0]]
                # C = [[0], [0]]
                A = [[]]
                B = [[]]
                C = [[]]
                D = [[np.cos(self.ang0), - np.sin(self.ang0), - self.xd0 * np.cos(self.ang0) - self.xq0 * np.sin(self.ang0)], [np.sin(self.ang0), np.cos(self.ang0), self.xq0 * np.cos(self.ang0) - self.xd0 * np.sin(self.ang0)], [np.sin(self.ang0), np.cos(self.ang0), self.xq0 * np.cos(self.ang0) - self.xd0 * np.sin(self.ang0)]]

                self.ss_full = ss(A, B, C, D)

                self.inputs['vmq_'+istr+'_Tv'] = 1
                self.inputs['vmd_'+istr+'_Tv'] = 2
                self.inputs['ang_'+istr+'_Tv'] = 3

                self.outputs['vcq_'+istr] = 1
                self.outputs['vcd_'+istr]= 2
                self.outputs['vmd_'+istr+'_PLL']= 3

                # self.states['dummy_Tv_'+istr] = 1
                self.states = {}

                # Merge
                self.inputs_full = ['vmq_'+istr+'_Tv', 'vmd_'+istr+'_Tv', 'ang_'+istr+'_Tv']
                self.outputs_full = ['vcq_'+istr, 'vcd_'+istr, 'vmd_'+istr+'_PLL']
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BTi:
            """
            Park transformation for the currents

            :param indx: index of the VSC
            :param xq0: equilibrium point for the q current
            :param xd0: equilibrium point for the d current
            :param ang0: equilibrium point for the angle
            :return: state space of the Park transformation for the currents
            """

            def __init__(self, indx, xq0, xd0, ang0):
                # store variables in the structure
                self.indx = indx
                self.xq0 = xq0
                self.xd0 = xd0
                self.ang0 = ang0

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # directly obtained ss
                # A = [[0]]
                # B = [[0, 0, 0]]
                # C = [[0], [0]]
                A = [[]]
                B = [[]]
                C = [[]]
                D = [[np.cos(self.ang0), - np.sin(self.ang0), - self.xd0 * np.cos(self.ang0) - self.xq0 * np.sin(self.ang0)], [np.sin(self.ang0), np.cos(self.ang0), self.xq0 * np.cos(self.ang0) - self.xd0 * np.sin(self.ang0)]]

                self.ss_full = ss(A, B, C, D)

                self.inputs['iq_'+istr] = 1
                self.inputs['id_'+istr] = 2
                self.inputs['ang_'+istr+'_Ti'] = 3

                self.outputs['icq_'+istr] = 1
                self.outputs['icd_'+istr] = 2

                # self.states['dummy_Ti_'+istr] = 1
                self.states = {}

                # Merge
                self.inputs_full = ['iq_'+istr, 'id_'+istr, 'ang_'+istr+'_Ti']
                self.outputs_full = ['icq_'+istr, 'icd_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)



        class BTvinv:
            """
            Inverse Park transformation for the voltages

            :param indx: index of the VSC
            :param xq0: equilibrium point for the q voltage
            :param xd0: equilibrium point for the d voltage
            :param ang0: equilibrium point for the angle
            :return: state space of the inverse Park transformation for the voltages
            """

            def __init__(self, indx, xq0, xd0, ang0):
                # store variables in the structure
                self.indx = indx
                self.xq0 = xq0
                self.xd0 = xd0
                self.ang0 = ang0

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # directly obtained ss
                # A = [[0]]
                # B = [[0, 0, 0]]
                # C = [[0], [0]]
                A = [[]]
                B = [[]]
                C = [[]]
                D = [[np.cos(self.ang0), np.sin(self.ang0), - self.xq0 * np.sin(self.ang0) + self.xd0 * np.cos(self.ang0)], [- np.sin(self.ang0), np.cos(self.ang0), - self.xq0 * np.cos(self.ang0) - self.xd0 * np.sin(self.ang0)]]

                self.ss_full = ss(A, B, C, D)

                self.inputs['vccq_'+istr] = 1
                self.inputs['vccd_'+istr] = 2
                self.inputs['ang_'+istr+'_Tvinv'] = 3

                self.outputs['vxq_'+istr] = 1
                self.outputs['vxd_'+istr]= 2

                # self.states['dummy_Tvinv_'+istr] = 1
                self.states = {}

                # Merge
                self.inputs_full = ['vccq_'+istr, 'vccd_'+istr, 'ang_'+istr+'_Tvinv']
                self.outputs_full = ['vxq_'+istr, 'vxd_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BDivs:
            """
            Class for the divison of repeated variables

            :param indx: index of the VSC
            :return: state space of all variables' division
            """

            def __init__(self, indx, bus_ac):
                # store variables in the structure
                self.indx = indx
                self.bus_ac = bus_ac

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)
                bus_ac = str(self.bus_ac)


                # vcq divsion
                self.inputs_nAvq = 'vcq_'+istr
                self.outputs_nAvq = ['vcq_'+istr+'_curr', 'vcq_'+istr+'_P', 'vcq_'+istr+'_Q']
                self.ss_nAvq, self.inputs, self.outputs, self.states = FNode(self.inputs_nAvq, self.outputs_nAvq, self.indx, self.inputs, self.outputs, self.states)

                # vcd division
                self.inputs_nAvd = 'vcd_'+istr
                self.outputs_nAvd = ['vcd_'+istr+'_curr', 'vcd_'+istr+'_P', 'vcd_'+istr+'_Q']
                self.ss_nAvd, self.inputs, self.outputs, self.states = FNode(self.inputs_nAvd, self.outputs_nAvd, self.indx, self.inputs, self.outputs, self.states)

                # icq division
                self.inputs_nAiq = 'icq_'+istr
                self.outputs_nAiq = ['icq_'+istr+'_curr', 'icq_'+istr+'_P', 'icq_'+istr+'_Q']
                self.ss_nAiq, self.inputs, self.outputs, self.states = FNode(self.inputs_nAiq, self.outputs_nAiq, self.indx, self.inputs, self.outputs, self.states)

                # icd division
                self.inputs_nAid = 'icd_'+istr
                self.outputs_nAid = ['icd_'+istr+'_curr', 'icd_'+istr+'_P', 'icd_'+istr+'_Q']
                self.ss_nAid, self.inputs, self.outputs, self.states = FNode(self.inputs_nAid, self.outputs_nAid, self.indx, self.inputs, self.outputs, self.states)

                # angle division
                self.inputs_nAang = 'ang_'+istr
                self.outputs_nAang = ['ang_'+istr+'_Tv', 'ang_'+istr+'_Ti', 'ang_'+istr+'_Tvinv']
                self.ss_nAang, self.inputs, self.outputs, self.states = FNode(self.inputs_nAang, self.outputs_nAang, self.indx, self.inputs, self.outputs, self.states)

                # vd division
                self.inputs_nAvd_div = 'vmd_'+istr
                self.outputs_nAvd_div = ['vmd_'+istr+'_Tv']
                self.ss_nAvd_div, self.inputs, self.outputs, self.states = FNode(self.inputs_nAvd_div, self.outputs_nAvd_div, self.indx, self.inputs, self.outputs, self.states)

                # vq division
                self.inputs_nAvq_div = 'vmq_'+istr
                self.outputs_nAvq_div = ['vmq_'+istr+'_Tv']
                self.ss_nAvq_div, self.inputs, self.outputs, self.states = FNode(self.inputs_nAvq_div, self.outputs_nAvq_div, self.indx, self.inputs, self.outputs, self.states)


                # iqxx division
                self.inputs_nAiqxx_div = 'iqxx_'+bus_ac
                self.outputs_nAiqxx_div = ['iqxv_'+bus_ac, 'iq_'+istr]
                self.ss_nAiqxx_div, self.inputs, self.outputs, self.states = FNode(self.inputs_nAiqxx_div, self.outputs_nAiqxx_div, self.indx, self.inputs, self.outputs, self.states)

                # idxx division
                self.inputs_nAidxx_div = 'idxx_'+bus_ac
                self.outputs_nAidxx_div = ['idxv_'+bus_ac, 'id_'+istr]
                self.ss_nAidxx_div, self.inputs, self.outputs, self.states = FNode(self.inputs_nAidxx_div, self.outputs_nAidxx_div, self.indx, self.inputs, self.outputs, self.states)

                # Merge
                self.ss_full = append(self.ss_nAvq, self.ss_nAvd, self.ss_nAiq, self.ss_nAid, self.ss_nAang, self.ss_nAvd_div, self.ss_nAvq_div, self.ss_nAiqxx_div, self.ss_nAidxx_div)
                self.inputs_full = ['vcq_'+istr, 'vcd_'+istr, 'icq_'+istr, 'icd_'+istr, 'ang_'+istr, 'vmd_'+istr, 'vmq_'+istr, 'iqxx_'+bus_ac, 'idxx_'+bus_ac]
                # self.outputs_full = ['vcq_'+istr+'_curr', 'vcq_'+istr+'_P', 'vcq_'+istr+'_Q',  'vcd_'+istr+'_curr', 'vcd_'+istr+'_P', 'vcd_'+istr+'_Q', 'vmd_'+istr+'_PLL', 'icq_'+istr+'_curr', 'icq_'+istr+'_P', 'icq_'+istr+'_Q', 'icd_'+istr+'_curr', 'icd_'+istr+'_P', 'icd_'+istr+'_Q', 'ang_'+istr+'_Tv', 'ang_'+istr+'_Ti', 'ang_'+istr+'_Tvinv', 'vmd_'+istr+'_Tv', 'vmq_'+istr+'_Tv', 'iqxv_'+bus_ac, 'iq_'+istr, 'idxv_'+bus_ac, 'id_'+istr]
                self.outputs_full = ['vcq_'+istr+'_curr', 'vcq_'+istr+'_P', 'vcq_'+istr+'_Q',  'vcd_'+istr+'_curr', 'vcd_'+istr+'_P', 'vcd_'+istr+'_Q', 'icq_'+istr+'_curr', 'icq_'+istr+'_P', 'icq_'+istr+'_Q', 'icd_'+istr+'_curr', 'icd_'+istr+'_P', 'icd_'+istr+'_Q', 'ang_'+istr+'_Tv', 'ang_'+istr+'_Ti', 'ang_'+istr+'_Tvinv', 'vmd_'+istr+'_Tv', 'vmq_'+istr+'_Tv', 'iqxv_'+bus_ac, 'iq_'+istr, 'idxv_'+bus_ac, 'id_'+istr]  # had to add vmd_PLL!!!!


                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BTrafo_filter:
            """
            Trafo + filter state space

            :param indx: index of the VSC
            :param w: pulsation at the linealization point
            :param bus_ac: ac bus at which the trafo is connected
            :param Rc: filter resistance
            :param Lc: filter inductance
            :param Rg: grid resistance
            :param Lg: grid inductance
            :return: state space of the grid constituted by the filter and the transformer
            """

            def __init__(self, indx, w, bus_ac, Rc, Lc, Rg, Lg):
                # store variables in the structure
                self.indx = indx
                self.w = w
                self.bus_ac = bus_ac
                self.Rc = Rc
                self.Lc = Lc
                self.Rg = Rg
                self.Lg = Lg

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)
                bus_ac = str(self.bus_ac)

                # directly obtained ss, original
                # A = [[-(self.Rc + self.Rg) / (self.Lc + self.Lg), -self.w],
                #      [self.w, -(self.Rc + self.Rg) / (self.Lc + self.Lg)]]
                # B = [[1 / (self.Lc + self.Lg), 0, -1 / (self.Lc + self.Lg), 0],
                #      [0, 1 / (self.Lc + self.Lg), 0, -1 / (self.Lc + self.Lg)]]
                # C = [[(self.Lc * self.Rg - self.Lg * self.Rc) / (self.Lc + self.Lg), 0],
                #      [0, (self.Lc * self.Rg - self.Lg * self.Rc) / (self.Lc + self.Lg)],
                #      [1, 0],
                #      [0, 1]]
                # D = [[self.Lg / (self.Lc + self.Lg), 0, self.Lc / (self.Lc + self.Lg), 0],
                #      [0, self.Lg / (self.Lc + self.Lg), 0, self.Lc / (self.Lc + self.Lg)],
                #      [0, 0, 0, 0],
                #      [0, 0, 0, 0]]


                # changing current sign??
                A = [[-(self.Rc + self.Rg) / (self.Lc + self.Lg), -self.w],
                     [self.w, -(self.Rc + self.Rg) / (self.Lc + self.Lg)]]
                B = [[1 / (self.Lc + self.Lg), 0, -1 / (self.Lc + self.Lg), 0],
                     [0, 1 / (self.Lc + self.Lg), 0, -1 / (self.Lc + self.Lg)]]
                C = [[(self.Lg * self.Rc - self.Lc * self.Rg) / (self.Lc + self.Lg), 0],
                     [0, (self.Lg * self.Rc - self.Lc * self.Rg) / (self.Lc + self.Lg)],
                     [1, 0],
                     [0, 1]]
                D = [[self.Lc / (self.Lc + self.Lg), 0, self.Lg / (self.Lc + self.Lg), 0],
                     [0, self.Lc / (self.Lc + self.Lg), 0, self.Lg / (self.Lc + self.Lg)],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]


                self.ss_full = ss(A, B, C, D)

                # original: 
                # self.inputs['vxq_'+istr] = 1
                # self.inputs['vxd_'+istr] = 2
                # self.inputs['vq_'+bus_ac] = 3
                # self.inputs['vd_'+bus_ac] = 4

                # change sign of the current?
                self.inputs['vq_'+bus_ac] = 1
                self.inputs['vd_'+bus_ac] = 2
                self.inputs['vxq_'+istr] = 3
                self.inputs['vxd_'+istr] = 4


                self.outputs['vmq_'+istr] = 1
                self.outputs['vmd_'+istr] = 2
                self.outputs['iqxx_'+bus_ac] = 3
                self.outputs['idxx_'+bus_ac] = 4

                self.states['iqxx_'+bus_ac] = 1
                self.states['idxx_'+bus_ac] = 2

                # Merge
                self.inputs_full = ['vxq_'+istr, 'vxd_'+istr, 'vq_'+bus_ac, 'vd_'+bus_ac]
                self.outputs_full = ['vmq_'+istr, 'vmd_'+istr, 'iqxx_'+bus_ac, 'idxx_'+bus_ac]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)




        def __init__(self, df_vsc, w, ll):
            self.w = w
            self.indx = ll
            self.name = df_vsc['name']
            self.bus_dc = df_vsc['bus DC']
            self.bus_ac = df_vsc['bus AC']
            self.Rc = df_vsc['Rc']
            self.Lc = df_vsc['Lc']
            self.Rg = df_vsc['Rg']
            self.Lg = df_vsc['Lg']
            self.kp_pll = df_vsc['kp_pll']
            self.ki_pll = df_vsc['ki_pll']
            self.kp_i = df_vsc['kp_i']
            self.ki_i = df_vsc['ki_i']
            self.vcq0 = df_vsc['vcq0']
            self.vcd0 = df_vsc['vcd0']
            self.icq0 = df_vsc['icq0']
            self.icd0 = df_vsc['icd0']
            self.kp_v = df_vsc['kp_v']
            self.ki_v = df_vsc['ki_v']
            self.kp_q = df_vsc['kp_q']
            self.ki_q = df_vsc['ki_q']
            self.kp_f = df_vsc['kp_f']
            self.kp_p = df_vsc['kp_p']
            self.ki_p = df_vsc['ki_p']
            self.k_gd = df_vsc['k_gd']
            self.tau_gd = df_vsc['tau_gd']
            self.vsq0 = df_vsc['vsq0']
            self.vsd0 = df_vsc['vsd0']
            self.isq0 = df_vsc['isq0']
            self.isd0 = df_vsc['isd0']
            self.ang0 = df_vsc['ang0']
            self.vmq0 = df_vsc['vmq0']
            self.vmd0 = df_vsc['vmd0']
            self.imq0 = df_vsc['imq0']
            self.imd0 = df_vsc['imd0']


            # add subblocks
            # self.P_outer = self.BP_outer(self.indx, self.vcq0, self.vcd0, self.icq0, self.icd0, self.kp_f, self.kp_p, self.ki_p)
            # self.Q_outer = self.BQ_outer(self.indx, self.vcq0, self.vcd0, self.icq0, self.icd0, self.kp_v, self.ki_v, self.kp_q, self.ki_q)
            self.P_outer = self.BP_outer(self.indx, self.vmq0, self.vmd0, self.imq0, self.imd0, self.kp_f, self.kp_p, self.ki_p)
            self.Q_outer = self.BQ_outer(self.indx, self.vmq0, self.vmd0, self.imq0, self.imd0, self.kp_v, self.ki_v, self.kp_q, self.ki_q)
            self.PLL = self.BPLL(self.indx, self.kp_pll, self.ki_pll)
            self.Inner_current_loop = self.BInnerCurrentLoop(self.indx, self.w, self.Lc, self.kp_i, self.ki_i)
            self.Gd = self.BGd(self.indx, self.k_gd, self.tau_gd)
            self.Tv = self.BTv(self.indx, self.vsq0, self.vsd0, self.ang0)
            self.Ti = self.BTi(self.indx, self.isq0, self.isd0, self.ang0)
            self.Tvinv = self.BTvinv(self.indx, self.vcq0, self.vcd0, self.ang0)
            self.Divs = self.BDivs(self.indx, self.bus_ac)
            self.Trafo_filter = self.BTrafo_filter(self.indx, self.w, self.bus_ac, self.Rc, self.Lc, self.Rg, self.Lg)

            # access information
            # print(self.P_outer.inputs_PI)  # things have to be accessed this way

            # in the end, add the index of the VSC (ll) in the final inputs, states, outputs names?

            # mix all subblocks
            self.dicc_in_pre = {**self.P_outer.dicc_in, **self.Q_outer.dicc_in, **self.PLL.dicc_in, **self.Inner_current_loop.dicc_in, **self.Gd.dicc_in, **self.Tv.dicc_in, **self.Ti.dicc_in, **self.Tvinv.dicc_in, **self.Divs.dicc_in, **self.Trafo_filter.dicc_in}
            self.keys_dicc_in_pre = list(self.dicc_in_pre.keys())
            self.values_dicc_in_pre = [ll + 1 for ll in range(len(self.keys_dicc_in_pre))]

            self.dicc_out_pre = {**self.P_outer.dicc_out, **self.Q_outer.dicc_out, **self.PLL.dicc_out, **self.Inner_current_loop.dicc_out, **self.Gd.dicc_out, **self.Tv.dicc_out, **self.Ti.dicc_out, **self.Tvinv.dicc_out, **self.Divs.dicc_out, **self.Trafo_filter.dicc_out}
            self.keys_dicc_out_pre = list(self.dicc_out_pre.keys())
            self.values_dicc_out_pre = [ll + 1 for ll in range(len(self.keys_dicc_out_pre))]

            self.dicc_x_pre = {**self.P_outer.dicc_x, **self.Q_outer.dicc_x, **self.PLL.dicc_x, **self.Inner_current_loop.dicc_x, **self.Gd.dicc_x, **self.Tv.dicc_x, **self.Ti.dicc_x, **self.Tvinv.dicc_x, **self.Divs.dicc_x, **self.Trafo_filter.dicc_x}
            self.keys_dicc_x_pre = list(self.dicc_x_pre.keys())
            self.values_dicc_x_pre = [ll + 1 for ll in range(len(self.keys_dicc_x_pre))]

            self.dic_i = {}
            for ll in range(len(self.dicc_in_pre)):
                self.dic_i[self.keys_dicc_in_pre[ll]] = ll + 1

            self.dic_o = {}
            for ll in range(len(self.dicc_out_pre)):
                self.dic_o[self.keys_dicc_out_pre[ll]] = ll + 1

            self.dic_x = {}
            for ll in range(len(self.dicc_x_pre)):
                self.dic_x[self.keys_dicc_x_pre[ll]] = ll + 1

            # Debug
            # print(self.dic_i)
            # print(self.dic_o)

            # Build final ss, just trying now
            self.inputs = ['Ap_ref_'+str(self.indx), 'Aq_ref_'+str(self.indx), 'vq_'+str(self.bus_ac), 'vd_'+str(self.bus_ac)]
            self.outputs = ['iqxv_'+str(self.bus_ac), 'idxv_'+str(self.bus_ac)]

            self.ss_full = append(self.P_outer.ss_final, self.Q_outer.ss_final, self.PLL.ss_final, self.Inner_current_loop.ss_final, self.Gd.ss_final, self.Tv.ss_final, self.Ti.ss_final, self.Tvinv.ss_final, self.Divs.ss_final, self.Trafo_filter.ss_final)
            self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs, self.outputs, self.dic_i, self.dic_o, self.dic_x)
            self.ssm = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)
            self.ss = self.ssm

            # print(self.states)

            FPrinter(self.ssm, self.name_x, self.name_in, self.name_out, prnt=False)

            self.states = self.name_x
            self.ext_inputs = ['Ap_ref_'+str(self.indx), 'Aq_ref_'+str(self.indx)]
            self.ext_outputs = ['iqxv_'+str(self.bus_ac), 'idxv_'+str(self.bus_ac)]


    VSCs = [VSC_particular(df_VSC.iloc[ll, :], w, ll) for ll in range(len(df_VSC))]
    # print(VSCs[0].P_outer.inputs_PI)

    return VSCs



def SG_full(df_SG, w):
    """
    Form all SGs classes

    :param df_SG: full data of SG, straight from the .xlsx file
    :param w: pulsation, in rad/s
    :return: it builds the state space with the corresponding names
    """

    class SG_particular:
        """
        Class for a particular SG

        :param df_SG: row of the full SG dataframe
        :param w: pulsation, in rad/s
        :param indx: index of the SG, from 0 to n
        :return: the state space and the names, also stores the input values
        """


        class BExciter:
            """
            Class for the exciter

            :param indx: index of the SG
            :param vsq0: equilibrium point for the q voltage
            :param vsd0: equilibrium point for the d voltage
            :param Vbase: base voltage in kV
            :param Rfd_pu:
            :param Lmd_pu:
            :param NsNf:
            :param Ka: constant of the control of the exciter
            :param Ta: first time constant
            :param Tb: second time constant
            :param Tc: third time constant
            :param Vfbase: base voltage in kV

            :return: state space of the exciter loop with the inputs, outputs, states
            """

            def __init__(self, indx, vsq0, vsd0, Vbase, Rfd_pu, Lmd_pu, NsNf, Ka, Ta, Tb, Tc, Vfbase):
                # store variables in the structure
                self.indx = indx
                self.vsq0 = vsq0
                self.vsd0 = vsd0
                self.Vbase = Vbase
                self.Rfd_pu = Rfd_pu
                self.Lmd_pu = Lmd_pu
                self.NsNf = NsNf
                self.Ka = Ka
                self.Ta = Ta
                self.Tb = Tb
                self.Tc = Tc
                self.Vfbase = Vfbase

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # absolute value of the voltage calculation
                self.inputs_fv = ['vsq_ac_'+istr, 'vsd_ac_'+istr]
                self.outputs_fv = 'vs_ac_'+istr
                self.ss_fv, self.inputs, self.outputs, self.states = FAC_voltage_SG(self.inputs_fv, self.outputs_fv, self.vsq0, self.vsd0, self.Vbase, self.indx, self.inputs, self.outputs, self.states)

                # voltage difference
                self.inputs_s1 = ['vs_ref_'+istr, 'vs_ac_'+istr]
                self.sign_s1 = [+1, -1]
                self.outputs_s1 = 'vs_err_'+istr
                self.ss_s1, self.inputs, self.outputs, self.states = FSum(self.inputs_s1, self.sign_s1, self.outputs_s1, self.indx, self.inputs, self.outputs, self.states)

                # G exciter control
                self.inputs_G = 'vs_err_'+istr
                self.outputs_G = 'vd_gf_'+istr
                self.states_G = ['xexc_1_'+istr, 'xexc_2_'+istr]
                self.ss_G, self.inputs, self.outputs, self.states = FG_exc(self.Rfd_pu, self.Lmd_pu, self.Vfbase, self.NsNf, self.Ka, self.Ta, self.Tb, self.Tc, self.inputs_G, self.outputs_G, self.states_G, self.indx, self.inputs, self.outputs, self.states)

                # Merge
                self.ss_full = append(self.ss_fv, self.ss_s1, self.ss_G)
                self.inputs_full = ['vsq_ac_'+istr, 'vsd_ac_'+istr, 'vs_ref_'+istr]
                self.outputs_full = ['vd_gf_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BGovernor:
            """
            Class for the governor

            :param indx: index of the SG
            :param wb: base frequency
            :param R: the regulation constant

            :return: state space of the governor loop with the inputs, outputs, states
            """

            def __init__(self, indx, wb, R):
                # store variables in the structure
                self.indx = indx
                self.wb = wb
                self.R = R

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # difference of frequencies
                self.inputs_s1 = ['w_ref_'+istr, 'w_g_'+istr]
                self.sign_s1 = [+1, -1]
                self.outputs_s1 = 'w_e_'+istr
                self.ss_s1, self.inputs, self.outputs, self.states = FSum(self.inputs_s1, self.sign_s1, self.outputs_s1, self.indx, self.inputs, self.outputs, self.states)

                # proportional control 1/(wb * R)
                self.inputs_kp1 = 'w_e_'+istr
                self.outputs_kp1 = 'w_err_'+istr
                self.ss_kp1, self.inputs, self.outputs, self.states = FP_controller(1 / (self.wb * self.R), self.inputs_kp1, self.outputs_kp1, self.indx, self.inputs, self.outputs, self.states)

                # difference of active powers
                self.inputs_s2 = ['p_ref_'+istr, 'w_err_'+istr]
                self.sign_s2 = [+1, +1]
                self.outputs_s2 = 'Ay_'+istr
                self.ss_s2, self.inputs, self.outputs, self.states = FSum(self.inputs_s2, self.sign_s2, self.outputs_s2, self.indx, self.inputs, self.outputs, self.states)

                # Merge
                self.ss_full = append(self.ss_s1, self.ss_kp1, self.ss_s2)
                self.inputs_full = ['w_ref_'+istr, 'w_g_'+istr, 'p_ref_'+istr]
                self.outputs_full = ['Ay_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BTurbine:
            """
            Class for the turbine

            :param indx: index of the SG
            :param T5: time constant for the 5th turbine
            :param T4: time constant for the 4th turbine
            :param T3: time constant for the 3th turbine
            :param T2: time constant for the 2th turbine
            :param F5: time constant for the 5th turbine
            :param F4: time constant for the 4th turbine
            :param F3: time constant for the 3th turbine
            :param F2: time constant for the 2th turbine

            :return: state space of the turbine with the inputs, outputs, states
            """

            def __init__(self, indx, T5, T4, T3, T2, F5, F4, F3, F2):
                # store variables in the structure
                self.indx = indx
                self.T5 = T5
                self.T4 = T4
                self.T3 = T3
                self.T2 = T2
                self.F5 = F5
                self.F4 = F4
                self.F3 = F3
                self.F2 = F2


                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # stage number 5
                self.inputs_s5 = ['Ay_'+istr]
                self.outputs_s5 = ['Ay5_'+istr, 'AT5_'+istr]
                self.ss_s5, self.inputs, self.outputs, self.states = FPiFi_turbine(self.T5, self.F5, self.inputs_s5, self.outputs_s5, self.indx, self.inputs, self.outputs, self.states)

                # stage number 4
                self.inputs_s4 = ['Ay5_'+istr]
                self.outputs_s4 = ['Ay4_'+istr, 'AT4_'+istr]
                self.ss_s4, self.inputs, self.outputs, self.states = FPiFi_turbine(self.T4, self.F4, self.inputs_s4, self.outputs_s4, self.indx, self.inputs, self.outputs, self.states)

                # stage number 3
                self.inputs_s3 = ['Ay4_'+istr]
                self.outputs_s3 = ['Ay3_'+istr, 'AT3_'+istr]
                self.ss_s3, self.inputs, self.outputs, self.states = FPiFi_turbine(self.T3, self.F3, self.inputs_s3, self.outputs_s3, self.indx, self.inputs, self.outputs, self.states)

                # stage number 2
                self.inputs_s2 = ['Ay3_'+istr]
                self.outputs_s2 = ['AT2_'+istr]
                self.ss_s2, self.inputs, self.outputs, self.states = FPiF_turbine(self.T2, self.F2, self.inputs_s2, self.outputs_s2, self.indx, self.inputs, self.outputs, self.states)


                # Merge
                self.ss_full = append(self.ss_s5, self.ss_s4, self.ss_s3, self.ss_s2)
                self.inputs_full = ['Ay_'+istr]
                self.outputs_full = ['AT5_'+istr, 'AT4_'+istr, 'AT3_'+istr, 'AT2_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)



        class BShaft:
            """
            Class for the multi-mass shaft

            :param indx: index of the SG
            :param wb: base pulsation in rad/s
            :param D1:
            :param D2:
            :param D3:
            :param D4:
            :param D5:
            :param H1:
            :param H2:
            :param H3:
            :param H4:
            :param H5:
            :param K12:
            :param K23:
            :param K34:
            :param K45:
            :return: state space of the shaft with the inputs, outputs, states
            """

            def __init__(self, indx, wb, Pn, D1, H1, K12, D2, H2, K23, D3, H3, K34, D4, H4, K45, D5, H5):
                # store variables in the structure
                self.indx = indx
                self.wb = wb
                self.Pn = Pn
                self.D1 = D1
                self.H1 = H1
                self.K12 = K12
                self.D2 = D2
                self.H2 = H2
                self.K23 = K23
                self.D3 = D3
                self.H3 = H3
                self.K34 = K34
                self.D4 = D4
                self.H4 = H4
                self.K45 = K45
                self.D5 = D5
                self.H5 = H5


                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # full shaft
                self.inputs_sh = ['ATe_'+istr, 'AT2_'+istr, 'AT3_'+istr, 'AT4_'+istr, 'AT5_'+istr]
                self.outputs_sh = ['we_'+istr]
                self.states_sh = ['xwpu_1_'+istr, 'xwpu_2_'+istr, 'xwpu_3_'+istr, 'xwpu_4_'+istr, 'xwpu_5_'+istr, 'xdelt_1_'+istr, 'xdelt_2_'+istr, 'xdelt_3_'+istr, 'xdelt_4_'+istr, 'xdelt_5_'+istr]
                self.ss_sh, self.inputs, self.outputs, self.states = FShaft(self.wb, self.Pn, self.D1, self.D2, self.D3, self.D4, self.D5, self.H1, self.H2, self.H3, self.H4, self.H5, self.K12, self.K23, self.K34, self.K45, self.inputs_sh, self.outputs_sh, self.states_sh, self.indx, self.inputs, self.outputs, self.states)


                # Merge
                self.ss_full = append(self.ss_sh)
                self.inputs_full = ['ATe_'+istr, 'AT2_'+istr, 'AT3_'+istr, 'AT4_'+istr, 'AT5_'+istr]
                self.outputs_full = ['we_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BElectricCircuit:
            """
            Class for the electric circuit

            :param indx: index of the SG
            :param Rs:
            :param Rkd:
            :param Rkq1:
            :param Rkq2:
            :param Rfd_pr:
            :param Lmd:
            :param Lmq:
            :param Ll:
            :param Llkd:
            :param Llkq1:
            :param Llkq2:
            :param Llfd_pr:
            :param we0:
            :param isq0:
            :param isd0:
            :param ik1q0:
            :param ik2q0:
            :param ifd0:
            :param ikd0:
            :return: state space of the full electric circuit with the inputs, outputs, states
            """

            def __init__(self, indx, Rs, Rkd, Rkq1, Rkq2, Rfd_pr, Lmd, Lmq, Ll, Llkd, Llkq1, Llkq2, Llfd_pr, we0, isq0, isd0, ik1q0, ik2q0, ifd0, ikd0):
                # store variables in the structure
                self.indx = indx
                self.Rs = Rs
                self.Rkd = Rkd
                self.Rkq1 = Rkq1
                self.Rkq2 = Rkq2
                self.Rfd_pr = Rfd_pr
                self.Lmd = Lmd
                self.Lmq = Lmq
                self.Ll = Ll
                self.Llkd = Llkd
                self.Llkq1 = Llkq1
                self.Llkq2 = Llkq2
                self.Llfd_pr = Llfd_pr
                self.we0 = we0
                self.isq0 = isq0
                self.isd0 = isd0
                self.ik1q0 = ik1q0
                self.ik2q0 = ik2q0
                self.ifd0 = ifd0
                self.ikd0 = ikd0


                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)


                # full electric circuit
                # self.inputs_se = ['vd_x_'+istr, 'vkd_x_'+istr, 'vfd_x_'+istr, 'vq_x_'+istr, 'vk1q_x_'+istr, 'vk2q_x_'+istr, 'we_y_'+istr]
                self.inputs_se = ['vd_x_'+istr, 'vkd_x_'+istr, 'vd_gf_'+istr, 'vq_x_'+istr, 'vk1q_x_'+istr, 'vk2q_x_'+istr, 'we_y_'+istr]
                self.outputs_se = ['isd_x_'+istr, 'ikd_x_'+istr, 'ifd_x_'+istr, 'isq_x_'+istr, 'ik1q_x_'+istr, 'ik2q_x_'+istr, 'ATe_'+istr]
                self.states_se = ['xisd_'+istr, 'xikd_'+istr, 'xifd_'+istr, 'xisq_'+istr, 'xik1q_'+istr, 'xik2q_'+istr]
                self.ss_se, self.inputs, self.outputs, self.states = FElectricCircuit(self.Rs, self.Rkd, self.Rkq1, self.Rkq2, self.Rfd_pr, self.Lmd, self.Lmq, self.Ll, self.Llkd, self.Llkq1, self.Llkq2, self.Llfd_pr, self.we0, self.isq0, self.isd0, self.ik1q0, self.ik2q0, self.ifd0, self.ikd0, self.inputs_se, self.outputs_se, self.states_se, self.indx, self.inputs, self.outputs, self.states)


                # Merge
                self.ss_full = append(self.ss_se)
                # self.inputs_full = ['vd_x_'+istr, 'vkd_x_'+istr, 'vfd_x_'+istr, 'vq_x_'+istr, 'vk1q_x_'+istr, 'vk2q_x_'+istr, 'we_y_'+istr]
                self.inputs_full = ['vd_x_'+istr, 'vkd_x_'+istr, 'vd_gf_'+istr, 'vq_x_'+istr, 'vk1q_x_'+istr, 'vk2q_x_'+istr, 'we_y_'+istr]
                self.outputs_full = ['isd_x_'+istr, 'ikd_x_'+istr, 'ifd_x_'+istr, 'isq_x_'+istr, 'ik1q_x_'+istr, 'ik2q_x_'+istr, 'ATe_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BTiinv:
            """
            Inverse Park transformation for the currents

            :param indx: index of the SG
            :param xq0: equilibrium point for the q current
            :param xd0: equilibrium point for the d current
            :param ang0: equilibrium point for the angle
            :return: state space of the inverse Park transformation for the currents
            """

            def __init__(self, indx, xq0, xd0, ang0):
                # store variables in the structure
                self.indx = indx
                self.xq0 = xq0
                self.xd0 = xd0
                self.ang0 = ang0

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # directly obtained ss
                # A = [[0]]
                # B = [[0, 0, 0]]
                # C = [[0], [0]]
                A = [[]]
                B = [[]]
                C = [[]]
                D = [[np.cos(self.ang0), np.sin(self.ang0), - self.xq0 * np.sin(self.ang0) + self.xd0 * np.cos(self.ang0)], [- np.sin(self.ang0), np.cos(self.ang0), - self.xq0 * np.cos(self.ang0) - self.xd0 * np.sin(self.ang0)]]

                self.ss_full = ss(A, B, C, D)

                self.inputs['isq_x_'+istr] = 1
                self.inputs['isd_x_'+istr] = 2
                self.inputs['ang_'+istr+'_Tiinv'] = 3

                self.outputs['isq_'+istr] = 1
                self.outputs['isd_'+istr]= 2

                # self.states['dummy_Tvinv_'+istr] = 1
                self.states = {}

                # Merge
                self.inputs_full = ['isq_x_'+istr, 'isd_x_'+istr, 'ang_'+istr+'_Tiinv']
                self.outputs_full = ['isq_'+istr, 'isd_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)

        class BTv:
            """
            Park transformation for the voltages

            :param indx: index of the SG
            :param xq0: equilibrium point for the q voltage
            :param xd0: equilibrium point for the d voltage
            :param ang0: equilibrium point for the angle
            :return: state space of the Park transformation for the voltages
            """

            def __init__(self, indx, xq0, xd0, ang0):
                # store variables in the structure
                self.indx = indx
                self.xq0 = xq0
                self.xd0 = xd0
                self.ang0 = ang0

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # directly obtained ss
                # A = [[0]]
                # B = [[0, 0, 0]]
                # C = [[0], [0]]
                A = [[]]
                B = [[]]
                C = [[]]
                D = [[np.cos(self.ang0), - np.sin(self.ang0), - self.xd0 * np.cos(self.ang0) - self.xq0 * np.sin(self.ang0)], [np.sin(self.ang0), np.cos(self.ang0), self.xq0 * np.cos(self.ang0) - self.xd0 * np.sin(self.ang0)]]

                self.ss_full = ss(A, B, C, D)

                self.inputs['vq_g_'+istr+'_Tv'] = 1
                self.inputs['vd_g_'+istr+'_Tv'] = 2
                self.inputs['ang_'+istr+'_Tv'] = 3

                self.outputs['vq_s_'+istr] = 1
                self.outputs['vd_s_'+istr]= 2

                # self.states['dummy_Tv_'+istr] = 1
                self.states = {}

                # Merge
                self.inputs_full = ['vq_g_'+istr+'_Tv', 'vd_g_'+istr+'_Tv', 'ang_'+istr+'_Tv']
                self.outputs_full = ['vq_s_'+istr, 'vd_s_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BDivs:
            """
            Class for the divison of repeated variables

            :param indx: index of the SG
            :return: state space of all variables' division
            """

            def __init__(self, indx, bus_ac):
                # store variables in the structure
                self.indx = indx
                self.bus_ac = bus_ac

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)
                bus_ac = str(self.bus_ac)

                # vq divsion
                self.inputs_nAvq = 'vqx_'+istr
                self.outputs_nAvq = ['vq_x_'+istr, 'vsq_ac_'+istr, 'vq_out_'+istr]
                self.ss_nAvq, self.inputs, self.outputs, self.states = FNode(self.inputs_nAvq, self.outputs_nAvq, self.indx, self.inputs, self.outputs, self.states)

                # vd division
                self.inputs_nAvd = 'vdx_'+istr
                self.outputs_nAvd = ['vd_x_'+istr, 'vsd_ac_'+istr, 'vd_out_'+istr]
                self.ss_nAvd, self.inputs, self.outputs, self.states = FNode(self.inputs_nAvd, self.outputs_nAvd, self.indx, self.inputs, self.outputs, self.states)

                # iq division
                self.inputs_nAiq = 'isq_x_'+istr
                self.outputs_nAiq = ['isq_l_'+istr, 'isq_out_'+istr]
                self.ss_nAiq, self.inputs, self.outputs, self.states = FNode(self.inputs_nAiq, self.outputs_nAiq, self.indx, self.inputs, self.outputs, self.states)

                # id division
                self.inputs_nAid = 'isd_x_'+istr
                self.outputs_nAid = ['isd_l_'+istr, 'isd_out_'+istr]
                self.ss_nAid, self.inputs, self.outputs, self.states = FNode(self.inputs_nAid, self.outputs_nAid, self.indx, self.inputs, self.outputs, self.states)

                # w division
                self.inputs_nw = 'we_'+istr
                self.outputs_nw = ['w_g_'+istr, 'we_y_'+istr]
                self.ss_nw, self.inputs, self.outputs, self.states = FNode(self.inputs_nw, self.outputs_nw, self.indx, self.inputs, self.outputs, self.states)

                # Merge
                self.ss_full = append(self.ss_nAvq, self.ss_nAvd, self.ss_nAiq, self.ss_nAid, self.ss_nw)
                self.inputs_full = ['vqx_'+istr, 'vdx_'+istr, 'isq_x_'+istr, 'isd_x_'+istr, 'we_'+istr]
                self.outputs_full = ['vq_x_'+istr, 'vsq_ac_'+istr, 'vq_out_'+istr, 'vd_x_'+istr, 'vsd_ac_'+istr, 'vd_out_'+istr, 'isq_l_'+istr, 'isq_out_'+istr, 'isd_l_'+istr, 'isd_out_'+istr, 'w_g_'+istr, 'we_y_'+istr]

                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)


        class BRload:
            """
            Basic Rload to extract the voltage

            :param indx: index of the SG
            :param Rload: value of the load resistance
            :param isq0: linealization point for the q current
            :param isd0: linealization point for the d current
            :return: state space of the voltage drop on a resistance
            """

            def __init__(self, indx, Rload, isq0, isd0):
                # store variables in the structure
                self.indx = indx
                self.Rload = Rload
                self.isq0 = isq0
                self.isd0 = isd0

                # initialize dictionaries and get the index
                self.inputs = {}
                self.outputs = {}
                self.states = {}
                istr = str(self.indx)

                # directly obtained ss
                A = [[]]
                B = [[]]
                C = [[]]
                D = [[-Rload, 0, Rload, 0, self.isq0], [0, -Rload, 0, Rload, self.isd0]]

                self.ss_full = ss(A, B, C, D)

                self.inputs['iq_load_'+istr] = 1
                self.inputs['id_load_'+istr] = 2
                self.inputs['isq_l_'+istr] = 3
                self.inputs['isd_l_'+istr] = 4
                self.inputs['Rload_'+istr] = 5

                self.outputs['vqx_'+istr] = 1
                self.outputs['vdx_'+istr] = 2

                self.states = {}

                # Merge
                self.inputs_full = ['iq_load_'+istr, 'id_load_'+istr, 'isq_l_'+istr, 'isd_l_'+istr, 'Rload_'+istr]
                self.outputs_full = ['vqx_'+istr, 'vdx_'+istr]
                self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs_full, self.outputs_full, self.inputs, self.outputs, self.states)
                self.ss_final = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)

                # Refer inputs, outputs and states to index 1
                self.indx_in = [ll + 1 for ll in range(len(self.indx_in))]
                self.indx_out = [ll + 1 for ll in range(len(self.indx_out))]
                self.indx_x = [ll + 1 for ll in range(len(self.indx_x))]

                self.dicc_in = BuildDictionary(self.indx_in, self.name_in)
                self.dicc_out = BuildDictionary(self.indx_out, self.name_out)
                self.dicc_x = BuildDictionary(self.indx_x, self.name_x)




        def __init__(self, df_sg, w, ll):
            self.w = w
            self.indx = ll
            self.name = df_sg['name']
            self.bus_ac = df_sg['bus AC']
            self.Vbase = df_sg['Vbase']
            self.wb = df_sg['wb']
            self.Ka = df_sg['Ka']
            self.Ta = df_sg['Ta']
            self.Tb = df_sg['Tb']
            self.Tc = df_sg['Tc']
            self.vsq0 = df_sg['vsq0']
            self.vsd0 = df_sg['vsd0']
            self.NsNf = df_sg['NsNf']
            self.Pn = df_sg['Pn']
            self.T5 = df_sg['T5']
            self.T4 = df_sg['T4']
            self.T3 = df_sg['T3']
            self.T2 = df_sg['T2']
            self.F5 = df_sg['F5']
            self.F4 = df_sg['F4']
            self.F3 = df_sg['F3']
            self.F2 = df_sg['F2']
            self.D1 = df_sg['D1']
            self.D2 = df_sg['D2']
            self.D3 = df_sg['D3']
            self.D4 = df_sg['D4']
            self.D5 = df_sg['D5']
            self.H1 = df_sg['H1']
            self.H2 = df_sg['H2']
            self.H3 = df_sg['H3']
            self.H4 = df_sg['H4']
            self.H5 = df_sg['H5']
            self.K12 = df_sg['K12']
            self.K23 = df_sg['K23']
            self.K34 = df_sg['K34']
            self.K45 = df_sg['K45']
            self.R = df_sg['R']
            self.Rfd = df_sg['Rfd']
            self.Rs = df_sg['Rs']
            self.Rkd = df_sg['Rkd']
            self.Rkq1 = df_sg['Rkq1']
            self.Rkq2 = df_sg['Rkq2']
            self.Rfd_pr = df_sg['Rfd_pr']
            self.Lmd = df_sg['Lmd']
            self.Lmq = df_sg['Lmq']
            self.Ll = df_sg['Ll']
            self.Llkd = df_sg['Llkd']
            self.Llkq1 = df_sg['Llkq1']
            self.Llkq2 = df_sg['Llkq2']
            self.Llfd_pr = df_sg['Llfd_pr']
            self.we0 = df_sg['we0']
            self.isq0 = df_sg['isq0']
            self.isd0 = df_sg['isd0']
            self.ik1q0 = df_sg['ik1q0']
            self.ik2q0 = df_sg['ik2q0']
            self.ifd0 = df_sg['ifd0']
            self.ikd0 = df_sg['ikd0']
            self.ang0 = df_sg['ang0']
            self.Rload = df_sg['Rload']
            self.Rfd_pu = df_sg['Rfd_pu']
            self.Lmd_pu = df_sg['Lmd_pu']
            self.Vfbase = df_sg['Vfbase']

            # add subblocks
            self.Exciter = self.BExciter(self.indx, self.vsq0, self.vsd0, self.Vbase, self.Rfd_pu, self.Lmd_pu, self.NsNf, self.Ka, self.Ta, self.Tb, self.Tc, self.Vfbase)
            self.Governor = self.BGovernor(self.indx, self.wb, self.R)
            self.Turbine = self.BTurbine(self.indx, self.T5, self.T4, self.T3, self.T2, self.F5, self.F4, self.F3, self.F2)
            self.Shaft = self.BShaft(self.indx, self.wb, self.Pn, self.D1, self.H1, self.K12, self.D2, self.H2, self.K23, self.D3, self.H3, self.K34, self.D4, self.H4, self.K45, self.D5, self.H5)
            self.ElectricCircuit = self.BElectricCircuit(self.indx, self.Rs, self.Rkd, self.Rkq1, self.Rkq2, self.Rfd_pr, self.Lmd, self.Lmq, self.Ll, self.Llkd, self.Llkq1, self.Llkq2, self.Llfd_pr, self.we0, self.isq0, self.isd0, self.ik1q0, self.ik2q0, self.ifd0, self.ikd0)
            self.RloadC = self.BRload(self.indx, self.Rload, self.isq0, self.isd0)
            self.Divs = self.BDivs(self.indx, self.bus_ac)

            # self.Tiinv = self.BTiinv(self.indx, self.isq0, self.isd0, self.ang0)
            # self.Tv = self.BTv(self.indx, self.vsq0, self.vsd0, self.ang0)



            # mix all subblocks
            self.dicc_in_pre = {**self.Exciter.dicc_in, **self.Governor.dicc_in, **self.Turbine.dicc_in, **self.Shaft.dicc_in, **self.ElectricCircuit.dicc_in, **self.RloadC.dicc_in, **self.Divs.dicc_in}
            self.keys_dicc_in_pre = list(self.dicc_in_pre.keys())
            self.values_dicc_in_pre = [ll + 1 for ll in range(len(self.keys_dicc_in_pre))]

            self.dicc_out_pre = {**self.Exciter.dicc_out, **self.Governor.dicc_out, **self.Turbine.dicc_out, **self.Shaft.dicc_out, **self.ElectricCircuit.dicc_out, **self.RloadC.dicc_out, **self.Divs.dicc_out}
            self.keys_dicc_out_pre = list(self.dicc_out_pre.keys())
            self.values_dicc_out_pre = [ll + 1 for ll in range(len(self.keys_dicc_out_pre))]

            self.dicc_x_pre = {**self.Exciter.dicc_x, **self.Governor.dicc_x, **self.Turbine.dicc_x, **self.Shaft.dicc_x, **self.ElectricCircuit.dicc_x, **self.RloadC.dicc_x, **self.Divs.dicc_x}
            self.keys_dicc_x_pre = list(self.dicc_x_pre.keys())
            self.values_dicc_x_pre = [ll + 1 for ll in range(len(self.keys_dicc_x_pre))]

            self.dic_i = {}
            for ll in range(len(self.dicc_in_pre)):
                self.dic_i[self.keys_dicc_in_pre[ll]] = ll + 1

            self.dic_o = {}
            for ll in range(len(self.dicc_out_pre)):
                self.dic_o[self.keys_dicc_out_pre[ll]] = ll + 1

            self.dic_x = {}
            for ll in range(len(self.dicc_x_pre)):
                self.dic_x[self.keys_dicc_x_pre[ll]] = ll + 1

            # Build final ss
            # self.inputs = ['w_ref_'+str(self.indx), 'p_ref_'+str(self.indx), 'vs_ref_'+str(self.indx), 'iq_load_'+str(self.indx), 'id_load_'+str(self.indx), 'Rload_'+str(self.indx)]
            # self.outputs = ['vqx_'+str(self.indx), 'vdx_'+str(self.indx), 'isd_x_'+str(self.indx), 'ikd_x_'+str(self.indx), 'ifd_x_'+str(self.indx), 'isq_x_'+str(self.indx), 'ik1q_x_'+str(self.indx), 'ik2q_x_'+str(self.indx), 'ATe_'+str(self.indx)]

            # for the stability, voltage as input, try it
            self.inputs = ['vqx_'+str(self.indx), 'vdx_'+str(self.indx)]
            self.outputs = ['isq_x_'+str(self.indx), 'isd_x_'+str(self.indx)]




            self.ss_full = append(self.Exciter.ss_final, self.Governor.ss_final, self.Turbine.ss_final, self.Shaft.ss_final, self.ElectricCircuit.ss_final, self.RloadC.ss_final, self.Divs.ss_final)
            self.Qq, self.indx_x, self.indx_in, self.indx_out, self.name_x, self.name_in, self.name_out = Qvec_builder_full(self.inputs, self.outputs, self.dic_i, self.dic_o, self.dic_x)
            self.ssm = connect(self.ss_full, self.Qq, self.indx_in, self.indx_out)
            self.ss = self.ssm

            # Debug
            # FPrinter(self.ssm, self.name_x, self.name_in, self.name_out, prnt=True)
            # print(self.RloadC.ss_final)


            writer = pd.ExcelWriter('results/solutionSG.xlsx')
            dfA = pd.DataFrame(self.ssm.A)
            dfB = pd.DataFrame(self.ssm.B)
            dfC = pd.DataFrame(self.ssm.C)
            dfD = pd.DataFrame(self.ssm.D)
            dfA.to_excel(writer, 'A')
            dfB.to_excel(writer, 'B')
            dfC.to_excel(writer, 'C')
            dfD.to_excel(writer, 'D')
            writer.save()


            # self.states = self.name_x
            # self.ext_inputs = ['Ap_ref_'+str(self.indx), 'Aq_ref_'+str(self.indx)]
            # self.ext_outputs = ['iqxv_'+str(self.bus_ac), 'idxv_'+str(self.bus_ac)]


    SGs = [SG_particular(df_SG.iloc[ll, :], w, ll) for ll in range(len(df_SG))]

    return SGs






def CSystem_test_VSC(excel_file):
    """
    Creates the state space of a single VSC

    :param excel_file: .xlsx file with multiple sheets
    :return: the final state space witht he corresponding names
    """


    # 0. initialization
    xlsx = pd.ExcelFile(excel_file)
    df_global = pd.read_excel(xlsx, 'Global')
    df_ext_inputs = pd.read_excel(xlsx, 'External_inputs')
    df_ext_outputs = pd.read_excel(xlsx, 'External_outputs')
    df_RL = pd.read_excel(xlsx, 'RL')
    df_RLC = pd.read_excel(xlsx, 'RLC')
    df_other = pd.read_excel(xlsx, 'Others')
    df_VSC = pd.read_excel(xlsx, 'VSC')
    df_SG = pd.read_excel(xlsx, 'SG')

    w = df_global['w (rad/s)'].values[0]
    Sb = df_global['S base (MVA)'].values[0]

    # many lines commented because I exclude Others for the annakkage system

    # 1. parser
    print(df_VSC)
    VSCs = VSC_full(df_VSC, w)

    return VSCs


# functions of subelements
def FP_active(name_input, name_output, vcqo, vcdo, icqo, icdo, indx, dic_i, dic_o, dic_x):
    '''
    Active power calculation state space subelement

    :param name_input: array with the names of the inputs
    :param name_output: name of the output reactive power
    :param vcqo: equilibrium point for the q voltage
    :param vcdo: equilibrium point for the d voltage
    :param icqo: equilibrium point for the q current
    :param icdo: equilibrium point for the d current
    :param indx: index to identify the block, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[]]
    B = [[]]
    C = [[]]
    D = [[3 / 2 * icqo, 3 / 2 * icdo, 3 / 2 * vcqo, 3 / 2 * vcdo]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for ll in range(len(name_input)):
        dic_i[name_input[ll]] = n_i + ll

    n_o = len(dic_o) + 1
    dic_o[name_output] = n_o

    return syst, dic_i, dic_o, dic_x


def FSum(name_in, sign_in, name_out, indx, dic_i, dic_o, dic_x):
    '''
    Sum state space subelement

    :param name_in: name of the inputs
    :param sign_in: array of +1 or -1 elements to identify the sign
    :param name_out: name of the output
    :param indx: index to identify the sum, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    n_inp = len(name_in)

    A = [[]]
    B = [[]*n_inp]
    C = [[]]
    D = [sign_in]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for ll in range(n_inp):
        dic_i[name_in[ll]] = n_i + ll

    n_o = len(dic_o) + 1
    dic_o[name_out] = n_o

    return syst, dic_i, dic_o, dic_x


def FP_controller(kp, var_in_name, var_out_name, indx, dic_i, dic_o, dic_x):
    '''
    Proportional controller state space subelement

    :param kp: proportional parameter of the controller
    :param var_in_name: name of the input of the controller
    :param var_out_name: name of the otput of the controller
    :param indx: index to identify the controller, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[]]
    B = [[]]
    C = [[]]
    D = [[kp]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    dic_i[var_in_name] = n_i

    n_o = len(dic_o) + 1
    dic_o[var_out_name] = n_o

    return syst, dic_i, dic_o, dic_x


def FPI_controller(ki, kp, var_in_name, var_out_name, indx, dic_i, dic_o, dic_x):
    '''
    PI controller state space subelement

    :param ki: integral parameter of the controller
    :param kp: proportional parameter of the controller
    :param var_in_name: name of the input of the controller
    :param var_out_name: name of the otput of the controller
    :param indx: index to identify the controller, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[0]]
    B = [[1]]
    C = [[ki]]
    D = [[kp]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    dic_i[var_in_name] = n_i

    n_o = len(dic_o) + 1
    dic_o[var_out_name] = n_o

    n_x = len(dic_x) + 1
    dic_x['int_'+var_in_name] = n_x

    return syst, dic_i, dic_o, dic_x


def FPiFi_turbine(T, F, var_in_name, var_out_name, indx, dic_i, dic_o, dic_x):
    '''
    Repetitive block inside the turbine steps

    :param T: time constant
    :param F: proportional control
    :param var_in_name: name of the input of the controller
    :param var_out_name: name of the otput of the controller
    :param indx: index to identify the SG
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[-1 / T]]
    B = [[1]]
    C = [[1 / T], [F / T]]
    D = [[0], [0]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for ll in range(len(var_in_name)):
        dic_i[var_in_name[ll]] = n_i + ll

    n_o = len(dic_o) + 1
    for ll in range(len(var_out_name)):
        dic_o[var_out_name[ll]] = n_o + ll

    n_x = len(dic_x) + 1
    dic_x['int_'+var_in_name[0]] = n_x

    return syst, dic_i, dic_o, dic_x


def FPiF_turbine(T, F, var_in_name, var_out_name, indx, dic_i, dic_o, dic_x):
    '''
    Final block inside the turbine

    :param T: time constant
    :param F: proportional control
    :param var_in_name: name of the input of the controller
    :param var_out_name: name of the otput of the controller
    :param indx: index to identify the SG
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[-1 / T]]
    B = [[1]]
    C = [[F / T]]
    D = [[0]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for ll in range(len(var_in_name)):
        dic_i[var_in_name[ll]] = n_i + ll

    n_o = len(dic_o) + 1
    for ll in range(len(var_out_name)):
        dic_o[var_out_name[ll]] = n_o + ll

    n_x = len(dic_x) + 1
    dic_x['int_'+var_in_name[0]] = n_x

    return syst, dic_i, dic_o, dic_x



def FShaft(wb, Pn, D1, D2, D3, D4, D5, H1, H2, H3, H4, H5, K12, K23, K34, K45, var_in_name, var_out_name, var_x_name, indx, dic_i, dic_o, dic_x):
    '''
    Final block inside the turbine

    :param wb: base pulsation
    :param Pn: nominal power
    :param D1:
    :param D2:
    :param D3:
    :param D4:
    :param D5:
    :param H1:
    :param H2:
    :param H3:
    :param H4:
    :param H5:
    :param K12:
    :param K23:
    :param K34:
    :param K45:
    :param var_in_name: name of the input of the shaft block
    :param var_out_name: name of the output of the shaft block
    :param var_x_name: name of the state of the shaft block
    :param indx: index to identify the SG
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    # follow what Luis has, rather than the slides
    A = [[-D1 / (2 * H1), 0, 0, 0, 0, -K12 / (2 * H1), K12 / (2 * H1), 0, 0, 0],
         [0, -D2 / (2 * H2), 0, 0, 0, K12 / (2 * H2), -(K12 + K23) / H2, K23 / (2 * H2), 0, 0],
         [0, 0, -D3 / (2 * H3), 0, 0, 0, K23 / (2 * H3), -(K23 + K34) / H3, K34 / (2 * H3), 0],
         [0, 0, 0, -D4 / (2 * H4), 0, 0, 0, K34 / (2 * H4), -(K34 + K45) / H4, K45 / (2 * H4)],
         [0, 0, 0, 0, -D5 / (2 * H5), 0, 0, 0, K45 / (2 * H5), -K45 / (2 * H5)],
         [wb, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, wb, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, wb, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, wb, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, wb, 0, 0, 0, 0, 0]]
    B = [[-wb / (2 * H1 * Pn), 0, 0, 0, 0],
         [0, 1 / (2 * H2), 0, 0, 0],
         [0, 0, 1 / (2 * H3), 0, 0],
         [0, 0, 0, 1 / (2 * H4), 0],
         [0, 0, 0, 0, 1 / (2 * H5)],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]]
    C = [[wb, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    D = [[0, 0, 0, 0, 0]]


    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for ll in range(len(var_in_name)):
        dic_i[var_in_name[ll]] = n_i + ll

    n_o = len(dic_o) + 1
    for ll in range(len(var_out_name)):
        dic_o[var_out_name[ll]] = n_o + ll

    n_x = len(dic_x) + 1
    for ll in range(len(var_x_name)):
        dic_x[var_x_name[ll]] = n_x + ll

    return syst, dic_i, dic_o, dic_x


# self.ss_se, self.inputs, self.outputs, self.states = FElectricCircuit(self.Rs, self.Rkd, self.Rkq1, self.Rkq2, self.Rfd_pr, self.Lmd, self.Lmq, self.Ll, self.Llkd, self.Llkq1, self.Llkq2, self.Llfd_pr, self.we0, self.isq0, self.isd0, self.ik1q0, self.ik2q0, self.ifd0, self.ikd0, self.inputs_se, self.outputs_se, self.states_se, self.indx, self.inputs, self.outputs, self.states)
def FElectricCircuit(Rs, Rkd, Rkq1, Rkq2, Rfd_pr, Lmd, Lmq, Ll, Llkd, Llkq1, Llkq2, Llfd_pr, we0, isq0, isd0, ik1q0, ik2q0, ifd0, ikd0, var_in_name, var_out_name, var_x_name, indx, dic_i, dic_o, dic_x):
    '''
    Final block for the electric circuit of the turbine

    :param Rs:
    :param Rkd:
    :param Rkq1:
    :param Rkq2:
    :param Rfd_pr:
    :param Lmd:
    :param Lmq:
    :param Ll:
    :param Llkd:
    :param Llkq1:
    :param Llkq2:
    :param Llfd_pr:
    :param we0:
    :param isq0:
    :param isd0:
    :param ik1q0:
    :param ik2q0:
    :param ifd0:
    :param ikd0:
    :param var_in_name: name of the input of the electric circuit
    :param var_out_name: name of the output of the electric circuit
    :param var_x_name: name of the state of the electric circuit
    :param indx: index to identify the SG
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    # follow what Luis has, rather than the slides
    # define matrices

    Lmod = [[-(Lmd + Ll), Lmd, Lmd, 0, 0, 0],
            [-Lmd, (Llkd + Lmd), Lmd, 0, 0, 0],
            [-Lmd, Lmd, (Llfd_pr + Lmd), 0, 0, 0],
            [0, 0, 0, -(Lmq + Ll), Lmq, Lmq],
            [0, 0, 0, -Lmq, (Llkq1 + Lmq), Lmq],
            [0, 0, 0, -Lmq, Lmq, (Llkq2 + Lmq)]]
    R8 = [[-Rs, 0, 0, 0, 0, 0],
          [0, Rkd, 0, 0, 0, 0],
          [0, 0, Rfd_pr, 0, 0, 0],
          [0, 0, 0, -Rs, 0, 0],
          [0, 0, 0, 0, Rkq1, 0],
          [0, 0, 0, 0, 0, Rkq2]]
    wLT = [[0, 0, 0, we0 * (Lmq + Ll), -we0 * Lmq, -we0 * Lmq],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [-we0 * (Lmd + Ll), we0 * Lmd, we0 * Lmd, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0]]
    IL1 = [[1, 0, 0, 0, 0, 0, -(isq0 * (Lmq + Ll) - Lmq * ik1q0 - Lmq * ik2q0)],
           [0, 1, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, -(-isd0 * (Lmd + Ll) + Lmd * ikd0 + Lmd * ifd0)],
           [0, 0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0, 1, 0]]
    Anp = np.matmul(- np.linalg.inv(np.array(Lmod)), (np.array(R8) + np.array(wLT)))
    Bnp = np.matmul(np.linalg.inv(np.array(Lmod)), np.array(IL1))
    A = Anp.tolist()
    B = Bnp.tolist()
    C = [[1, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 1],
         [3 / 2 * (isq0 * (-Lmd + Lmq) - Lmq * (ik1q0 + ik2q0)), 3 / 2 * Lmd * isq0, 3 / 2 * Lmd * isq0, 3 / 2 * (isd0 * (- Lmd + Lmq) + Lmd * (ikd0 + ifd0)), -3 / 2 * Lmq * isd0, -3 / 2 * Lmq * isd0]]
    D = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]]


    # process
    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for kk in range(len(var_in_name)):
        dic_i[var_in_name[kk]] = n_i + kk

    n_o = len(dic_o) + 1
    for kk in range(len(var_out_name)):
        dic_o[var_out_name[kk]] = n_o + kk

    n_x = len(dic_x) + 1
    for kk in range(len(var_x_name)):
        dic_x[var_x_name[kk]] = n_x + kk

    return syst, dic_i, dic_o, dic_x




def FNode(name_in, name_out, indx, dic_i, dic_o, dic_x):
    '''
    Node state space subelement, to have a duplicate variable

    :param name_in: name of the input
    :param name_out: name of the outputs
    :param indx: index to identify the node, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    n_out = len(name_out)

    A = [[]]
    B = [[]]
    C = [[]]
    D = [[1]] * n_out

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    dic_i[name_in] = n_i

    n_o = len(dic_o) + 1
    for ll in range(n_out):
        dic_o[name_out[ll]] = n_o + ll

    return syst, dic_i, dic_o, dic_x


def FAC_voltage(name_input, name_output, vcqo, vcdo, indx, dic_i, dic_o, dic_x):
    '''
    AC voltage absolute value calculation state space subelement

    :param name_input: array of the input names
    :param name_output: name of the output voltage
    :param vcqo: equilibrium point for the q voltage
    :param vcdo: equilibrium point for the d voltage
    :param indx: index to identify the block, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[]]
    B = [[]]
    C = [[]]
    D = [[vcqo / np.sqrt(vcqo ** 2 + vcdo ** 2), vcdo / np.sqrt(vcqo ** 2 + vcdo ** 2)]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for ll in range(len(name_input)):
        dic_i[name_input[ll]] = n_i + ll

    n_o = len(dic_o) + 1
    dic_o[name_output] = n_o

    return syst, dic_i, dic_o, dic_x


def FAC_voltage_SG(name_input, name_output, vcqo, vcdo, Vbase, indx, dic_i, dic_o, dic_x):
    '''
    AC voltage absolute value calculation state space subelement, for the SG

    :param name_input: array of the input names
    :param name_output: name of the output voltage
    :param vcqo: equilibrium point for the q voltage
    :param vcdo: equilibrium point for the d voltage
    :param Vbase: base voltage, only used in the SG
    :param indx: index to identify the block, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[]]
    B = [[]]
    C = [[]]
    D = [[vcqo / np.sqrt(vcqo ** 2 + vcdo ** 2), vcdo / np.sqrt(vcqo ** 2 + vcdo ** 2)]] * 1 / Vbase

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for ll in range(len(name_input)):
        dic_i[name_input[ll]] = n_i + ll

    n_o = len(dic_o) + 1
    dic_o[name_output] = n_o

    return syst, dic_i, dic_o, dic_x


def FG_exc(Rfd, Lmd, Vbase, NsNf, Ka, Ta, Tb, Tc, name_input, name_output, name_state, indx, dic_i, dic_o, dic_x):
    '''
    AC voltage absolute value calculation state space subelement, for the SG

    :param Rfd:
    :param Lmd:
    :param Vbase:
    :param NsNf:
    :param Ka: constant of the control of the exciter
    :param Ta: first time constant
    :param Tb: second time constant
    :param Tc: third time constant
    :param name_input: array of the input names
    :param name_output: name of the output voltage
    :param indx: index to identify the block, usually set to indx_SG
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    Ksg = Rfd / Lmd * Vbase * NsNf

    A = [[0, 1], [-1 / (Ta * Tb), -1 / Tb - 1 / Ta]]
    B = [[0], [1]]
    C = [[Ksg * Ka / (Ta * Tb), Ksg * Tc * Ka / (Ta * Tb)]]
    D = [[0]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    dic_i[name_input] = n_i

    n_o = len(dic_o) + 1
    dic_o[name_output] = n_o

    n_x = len(dic_x) + 1
    dic_x[name_state[0]] = n_x
    dic_x[name_state[1]] = n_x + 1

    return syst, dic_i, dic_o, dic_x




def FQ_active(name_input, name_output, vcqo, vcdo, icqo, icdo, indx, dic_i, dic_o, dic_x):
    '''
    Reactive power calculation state space subelement

    :param name_input: array with the names of the inputs
    :param name_output: name of the output reactive power
    :param vcqo: equilibrium point for the q voltage
    :param vcdo: equilibrium point for the d voltage
    :param icqo: equilibrium point for the q current
    :param icdo: equilibrium point for the d current
    :param indx: index to identify the block, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[]]
    B = [[]]
    C = [[]]
    D = [[3 / 2 * icdo, - 3 / 2 * icqo, - 3 / 2 * vcdo, 3 / 2 * vcqo]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    for ll in range(len(name_input)):
        dic_i[name_input[ll]] = n_i + ll

    n_o = len(dic_o) + 1
    dic_o[name_output] = n_o

    return syst, dic_i, dic_o, dic_x


def BuildDictionary(list_indx, list_name):
    '''
    Create a dictionary from the list indices and names

    :param list_indx: array of indices, from 1 to n
    :param list_name: array of the names linked to the indices
    :return: dictionary with both lists merged
    '''

    dicc = {}
    len_indx = len(list_indx)
    len_name = len(list_name)
    if len_indx != len_name:
        print('Error, lengths do not match')
    else:
        for ll in range(len_indx):
            dicc[list_name[ll]] = list_indx[ll]

    return dicc


def FProduct(name_in, ct_val, name_out, indx, dic_i, dic_o, dic_x):
    '''
    Product state space subelement

    :param name_in: name of the input
    :param ct_val: constant value by which we multiply
    :param name_out: name of the output
    :param indx: index to identify the product, usually set to indx_VSC
    :param dic_i: dictionary of inputs
    :param dic_o: dictionary of outputs
    :param dic_x: dictionary of states
    :return: the final state space and the dictionaries of inputs, outputs and states
    '''

    A = [[]]
    B = [[]]
    C = [[]]
    D = [[ct_val]]

    indx = str(indx)
    syst = ss(A, B, C, D)

    n_i = len(dic_i) + 1
    if name_in not in dic_i:
        dic_i[name_in] = n_i

    n_o = len(dic_o) + 1
    dic_o[name_out] = n_o


    return syst, dic_i, dic_o, dic_x


def bode_2x2(ss_class, f_ini=0, f_fin=3, name_in=[], name_out=[], n_p=1000, logx = False, dBy = False, invert = False):
    '''
    Bode plot of a 2x2 system

    :param ss_class: class with the space state, the inputs and the outputs
    :param lim_ini: log of the initial frequency. For instance, -1 represents 10^(-1) Hz
    :param lim_fin: log of the final frequency. For instance, 4 represents 10^(4) Hz
    :param name_in: name of the 2 inputs
    :param name_out: name of the 2 outputs
    :param n_p: number of points to represent. For instance, 1000    
    :param logx: if the horizontal axis has to be logarithmic
    :param dBy: if the vertical axis has to be in dB
    :param invert: divide in / out instead of out / in
    :return: nothing, it just plots
    '''
    # initial definitions
    n_points = n_p
    wfreq = np.logspace(f_ini, f_fin, num=n_points) * 2 * np.pi
    ffreq = np.logspace(f_ini, f_fin, num=n_points)
    (mag, phase, freq) = ss_class.ssm.freqresp(wfreq)

    # print(ss_class.outputs.index('vqx_0'))
    ii0 = ss_class.inputs.index(name_in[0])
    ii1 = ss_class.inputs.index(name_in[1])
    oo0 = ss_class.outputs.index(name_out[0])
    oo1 = ss_class.outputs.index(name_out[1])

    # extract indices for inputs/outputs
    if invert is False:
        in0 = ii0
        in1 = ii1
        out0 = oo0
        out1 = oo1
    else:
        in0 = oo0
        in1 = oo1
        out0 = ii0
        out1 = ii1

    # plot
    fig, axs = plt.subplots(4, 2)

    if logx is True and dBy is True:
        axs[0, 0].semilogx(ffreq, 20 * np.log10(abs(mag[out0, in0])))
        axs[0, 1].semilogx(ffreq, 20 * np.log10(abs(mag[out0, in1])))

        axs[1, 0].semilogx(ffreq, 180 / np.pi * (phase[out0, in0]))
        axs[1, 1].semilogx(ffreq, 180 / np.pi * (phase[out0, in1]))

        axs[2, 0].semilogx(ffreq, 20 * np.log10(abs(mag[out1, in0])))
        axs[2, 1].semilogx(ffreq, 20 * np.log10(abs(mag[out1, in1])))

        axs[3, 0].semilogx(ffreq, 180 / np.pi * (phase[out1, in0]))
        axs[3, 1].semilogx(ffreq, 180 / np.pi * (phase[out1, in1]))

        axs[0, 0].set_xlabel('Frequency (Hz)')
        axs[0, 0].set_ylabel('Magnitude (dB)')

        axs[0, 1].set_xlabel('Frequency (Hz)')
        axs[0, 1].set_ylabel('Magnitude (dB)')

        axs[1, 0].set_xlabel('Frequency (Hz)')
        axs[1, 0].set_ylabel('Phase (deg)')

        axs[1, 1].set_xlabel('Frequency (Hz)')
        axs[1, 1].set_ylabel('Phase (deg)')

        axs[2, 0].set_xlabel('Frequency (Hz)')
        axs[2, 0].set_ylabel('Magnitude (dB)')

        axs[2, 1].set_xlabel('Frequency (Hz)')
        axs[2, 1].set_ylabel('Magnitude (dB)')

        axs[3, 0].set_xlabel('Frequency (Hz)')
        axs[3, 0].set_ylabel('Phase (deg)')

        axs[3, 1].set_xlabel('Frequency (Hz)')
        axs[3, 1].set_ylabel('Phase (deg)')

    if logx is False and dBy is True:
        axs[0, 0].plot(ffreq, 20 * np.log10(abs(mag[out0, in0])))
        axs[0, 1].plot(ffreq, 20 * np.log10(abs(mag[out0, in1])))

        axs[1, 0].plot(ffreq, 180 / np.pi * (phase[out0, in0]))
        axs[1, 1].plot(ffreq, 180 / np.pi * (phase[out0, in1]))

        axs[2, 0].plot(ffreq, 20 * np.log10(abs(mag[out1, in0])))
        axs[2, 1].plot(ffreq, 20 * np.log10(abs(mag[out1, in1])))

        axs[3, 0].plot(ffreq, 180 / np.pi * (phase[out1, in0]))
        axs[3, 1].plot(ffreq, 180 / np.pi * (phase[out1, in1]))

        axs[0, 0].set_xlabel('Frequency (Hz)')
        axs[0, 0].set_ylabel('Magnitude (dB)')

        axs[0, 1].set_xlabel('Frequency (Hz)')
        axs[0, 1].set_ylabel('Magnitude (dB)')

        axs[1, 0].set_xlabel('Frequency (Hz)')
        axs[1, 0].set_ylabel('Phase (deg)')

        axs[1, 1].set_xlabel('Frequency (Hz)')
        axs[1, 1].set_ylabel('Phase (deg)')

        axs[2, 0].set_xlabel('Frequency (Hz)')
        axs[2, 0].set_ylabel('Magnitude (dB)')

        axs[2, 1].set_xlabel('Frequency (Hz)')
        axs[2, 1].set_ylabel('Magnitude (dB)')

        axs[3, 0].set_xlabel('Frequency (Hz)')
        axs[3, 0].set_ylabel('Phase (deg)')

        axs[3, 1].set_xlabel('Frequency (Hz)')
        axs[3, 1].set_ylabel('Phase (deg)')

    if logx is True and dBy is False:
        axs[0, 0].semilogx(ffreq, 20 * np.abs(abs(mag[out0, in0])))
        axs[0, 1].semilogx(ffreq, 20 * np.abs(abs(mag[out0, in1])))

        axs[1, 0].semilogx(ffreq, 180 / np.pi * (phase[out0, in0]))
        axs[1, 1].semilogx(ffreq, 180 / np.pi * (phase[out0, in1]))

        axs[2, 0].semilogx(ffreq, 20 * np.abs(abs(mag[out1, in0])))
        axs[2, 1].semilogx(ffreq, 20 * np.abs(abs(mag[out1, in1])))

        axs[3, 0].semilogx(ffreq, 180 / np.pi * (phase[out1, in0]))
        axs[3, 1].semilogx(ffreq, 180 / np.pi * (phase[out1, in1]))

        axs[0, 0].set_xlabel('Frequency (Hz)')
        axs[0, 0].set_ylabel('Magnitude ')

        axs[0, 1].set_xlabel('Frequency (Hz)')
        axs[0, 1].set_ylabel('Magnitude ')

        axs[1, 0].set_xlabel('Frequency (Hz)')
        axs[1, 0].set_ylabel('Phase (deg)')

        axs[1, 1].set_xlabel('Frequency (Hz)')
        axs[1, 1].set_ylabel('Phase (deg)')

        axs[2, 0].set_xlabel('Frequency (Hz)')
        axs[2, 0].set_ylabel('Magnitude ')

        axs[2, 1].set_xlabel('Frequency (Hz)')
        axs[2, 1].set_ylabel('Magnitude ')

        axs[3, 0].set_xlabel('Frequency (Hz)')
        axs[3, 0].set_ylabel('Phase (deg)')

        axs[3, 1].set_xlabel('Frequency (Hz)')
        axs[3, 1].set_ylabel('Phase (deg)')

    else:
        axs[0, 0].plot(ffreq, 20 * np.abs(abs(mag[out0, in0])))
        axs[0, 1].plot(ffreq, 20 * np.abs(abs(mag[out0, in1])))

        axs[1, 0].plot(ffreq, 180 / np.pi * (phase[out0, in0]))
        axs[1, 1].plot(ffreq, 180 / np.pi * (phase[out0, in1]))

        axs[2, 0].plot(ffreq, 20 * np.abs(abs(mag[out1, in0])))
        axs[2, 1].plot(ffreq, 20 * np.abs(abs(mag[out1, in1])))

        axs[3, 0].plot(ffreq, 180 / np.pi * (phase[out1, in0]))
        axs[3, 1].plot(ffreq, 180 / np.pi * (phase[out1, in1]))

        axs[0, 0].set_xlabel('Frequency (Hz)')
        axs[0, 0].set_ylabel('Magnitude ')

        axs[0, 1].set_xlabel('Frequency (Hz)')
        axs[0, 1].set_ylabel('Magnitude ')

        axs[1, 0].set_xlabel('Frequency (Hz)')
        axs[1, 0].set_ylabel('Phase (deg)')

        axs[1, 1].set_xlabel('Frequency (Hz)')
        axs[1, 1].set_ylabel('Phase (deg)')

        axs[2, 0].set_xlabel('Frequency (Hz)')
        axs[2, 0].set_ylabel('Magnitude ')

        axs[2, 1].set_xlabel('Frequency (Hz)')
        axs[2, 1].set_ylabel('Magnitude ')

        axs[3, 0].set_xlabel('Frequency (Hz)')
        axs[3, 0].set_ylabel('Phase (deg)')

        axs[3, 1].set_xlabel('Frequency (Hz)')
        axs[3, 1].set_ylabel('Phase (deg)')


    axs[0, 0].set_title('Yqq')
    axs[0, 1].set_title('Yqd')
    axs[2, 0].set_title('Ydq')
    axs[2, 1].set_title('Ydd')

    axs[1, 0].set_ylim([-180, 180])
    axs[1, 1].set_ylim([-180, 180])
    axs[3, 1].set_ylim([-180, 180])
    axs[3, 1].set_ylim([-180, 180])

    plt.show()

    return ()


def eigen(ss_class, plot=False, prnt=False):
    """
    Print the eigenvalues
    :param ss_class: class from where to extract the ss
    :param plot: if true, plots the eigenvalues map
    :param prnt: if true, prints the eigenvalues
    :return: print eigenvalues
    """

    if prnt is True:
        damp(ss_class.ss)

    if plot is True:
        pp = pole(ss_class.ss)
        pp_re = [ele.real for ele in pp]
        pp_im = [ele.imag for ele in pp]
        plt.scatter(pp_re, pp_im)
        plt.ylabel('Imaginary')
        plt.xlabel('Real')
        plt.show()


def matlab_ss(file_route):
    """
    Build the ss from the csv file
    :param file_route: route to read the matlab info
    :return: class with the ss, inputs, outputs, states
    """

    xls = pd.ExcelFile(file_route)
    dfA = pd.read_excel(xls, 'A', header=None)
    dfB = pd.read_excel(xls, 'B', header=None)
    dfC = pd.read_excel(xls, 'C', header=None)
    dfD = pd.read_excel(xls, 'D', header=None)

    ins = pd.read_excel(xls, 'inputs', header=None)
    outs = pd.read_excel(xls, 'outputs', header=None)
    states = pd.read_excel(xls, 'states', header=None)

    class ss_data:
        """
        Class where the most relevant final objects are stored
        """
        def __init__(self, A, B, C, D, ins, outs, states):
            A = np.array(dfA)
            B = np.array(dfB)
            C = np.array(dfC)
            D = np.array(dfD)

            self.ssm = ss(A, B, C, D)
            self.ss = self.ssm
            self.inputs = ins.T.values[0].tolist()
            self.outputs = outs.T.values[0].tolist()
            self.states = states.T.values[0].tolist()

    mtlb_ss = ss_data(dfA, dfB, dfC, dfD, ins, outs, states)
    return mtlb_ss


def bode_compare(ss_class_py, ss_class_mt, f_ini=0, f_fin=3, name_in_py=[], name_out_py=[], name_in_mt=[], name_out_mt=[], n_p=1000):
    '''
    Bode plot of a 2x2 system

    :param ss_class_py: python class with the space state, the inputs and the outputs
    :param ss_class_mt: matlab class with the space state, the inputs and the outputs
    :param lim_ini: log of the initial frequency. For instance, -1 represents 10^(-1) Hz
    :param lim_fin: log of the final frequency. For instance, 4 represents 10^(4) Hz
    :param name_in_py: python name of the 2 inputs
    :param name_out_py: python name of the 2 outputs
    :param name_in_mt: matlab name of the 2 inputs
    :param name_out_mt: matlab name of the 2 outputs
    :param n_p: number of points to represent. For instance, 1000    
    :return: nothing, it just plots
    '''
    # initial definitions
    n_points = n_p
    wfreq = np.logspace(f_ini, f_fin, num=n_points) * 2 * np.pi
    ffreq = np.logspace(f_ini, f_fin, num=n_points)

    (mag_py, phase_py, freq) = ss_class_py.ssm.freqresp(wfreq)
    (mag_mt, phase_mt, freq) = ss_class_mt.ssm.freqresp(wfreq)

    # extract indices for inputs/outputs
    in0_py = ss_class_py.inputs.index(name_in_py[0])
    in1_py = ss_class_py.inputs.index(name_in_py[1])

    out0_py = ss_class_py.outputs.index(name_out_py[0])
    out1_py = ss_class_py.outputs.index(name_out_py[1])

    in0_mt = ss_class_mt.inputs.index(name_in_mt[0])
    in1_mt = ss_class_mt.inputs.index(name_in_mt[1])

    out0_mt = ss_class_mt.outputs.index(name_out_mt[0])
    out1_mt = ss_class_mt.outputs.index(name_out_mt[1])


    # plot
    fig, axs = plt.subplots(4, 2)

    # python
    axs[0, 0].plot(ffreq, 20 * np.abs(abs(mag_py[out0_py, in0_py])))
    axs[0, 1].plot(ffreq, 20 * np.abs(abs(mag_py[out0_py, in1_py])))

    axs[1, 0].plot(ffreq, 180 / np.pi * (phase_py[out0_py, in0_py]))
    axs[1, 1].plot(ffreq, 180 / np.pi * (phase_py[out0_py, in1_py]))

    axs[2, 0].plot(ffreq, 20 * np.abs(abs(mag_py[out1_py, in0_py])))
    axs[2, 1].plot(ffreq, 20 * np.abs(abs(mag_py[out1_py, in1_py])))

    axs[3, 0].plot(ffreq, 180 / np.pi * (phase_py[out1_py, in0_py]))
    axs[3, 1].plot(ffreq, 180 / np.pi * (phase_py[out1_py, in1_py]))

    # matlab
    axs[0, 0].plot(ffreq, 20 * np.abs(abs(mag_mt[out0_mt, in0_mt])), '--')
    axs[0, 1].plot(ffreq, 20 * np.abs(abs(mag_mt[out0_mt, in1_mt])), '--')

    axs[1, 0].plot(ffreq, 180 / np.pi * (phase_mt[out0_mt, in0_mt]), '--')
    axs[1, 1].plot(ffreq, 180 / np.pi * (phase_mt[out0_mt, in1_mt]), '--')

    axs[2, 0].plot(ffreq, 20 * np.abs(abs(mag_mt[out1_mt, in0_mt])), '--')
    axs[2, 1].plot(ffreq, 20 * np.abs(abs(mag_mt[out1_mt, in1_mt])), '--')

    axs[3, 0].plot(ffreq, 180 / np.pi * (phase_mt[out1_mt, in0_mt]), '--')
    axs[3, 1].plot(ffreq, 180 / np.pi * (phase_mt[out1_mt, in1_mt]), '--')

    axs[0, 0].legend(['Python', 'Matlab'])


    axs[0, 0].set_xlabel('Frequency (Hz)')
    axs[0, 0].set_ylabel('Magnitude ')

    axs[0, 1].set_xlabel('Frequency (Hz)')
    axs[0, 1].set_ylabel('Magnitude ')

    axs[1, 0].set_xlabel('Frequency (Hz)')
    axs[1, 0].set_ylabel('Phase (deg)')

    axs[1, 1].set_xlabel('Frequency (Hz)')
    axs[1, 1].set_ylabel('Phase (deg)')

    axs[2, 0].set_xlabel('Frequency (Hz)')
    axs[2, 0].set_ylabel('Magnitude ')

    axs[2, 1].set_xlabel('Frequency (Hz)')
    axs[2, 1].set_ylabel('Magnitude ')

    axs[3, 0].set_xlabel('Frequency (Hz)')
    axs[3, 0].set_ylabel('Phase (deg)')

    axs[3, 1].set_xlabel('Frequency (Hz)')
    axs[3, 1].set_ylabel('Phase (deg)')


    axs[0, 0].set_title('Yqq')
    axs[0, 1].set_title('Yqd')
    axs[2, 0].set_title('Ydq')
    axs[2, 1].set_title('Ydd')

    axs[1, 0].set_ylim([-180, 180])
    axs[1, 1].set_ylim([-180, 180])
    axs[3, 1].set_ylim([-180, 180])
    axs[3, 1].set_ylim([-180, 180])

    plt.show()

    return ()


class Stability_Analysis:
    """
    Class to store the stability analysis functions and results

    :param ss_class: like VSCs[0], the element we want to study
    :return: bodes, nyquist, passivity...
    """
    def __init__(self, ss_class):
        self.ss = ss_class

    def bode_YZ(ss_class, f_ini=0, f_fin=3, name_in=[], name_out=[], n_p=1000, logx = False, dBy = False, invert = False):
        '''
        Bode plot of a 2x2 system

        :param ss_class: class with the space state, the inputs and the outputs
        :param lim_ini: log of the initial frequency. For instance, -1 represents 10^(-1) Hz
        :param lim_fin: log of the final frequency. For instance, 4 represents 10^(4) Hz
        :param name_in: name of the 2 inputs
        :param name_out: name of the 2 outputs
        :param n_p: number of points to represent. For instance, 1000    
        :param logx: if the horizontal axis has to be logarithmic
        :param dBy: if the vertical axis has to be in dB
        :param invert: divide in / out instead of out / in
        :return: nothing, it just plots
        '''
        # initial definitions
        n_points = n_p
        wfreq = np.logspace(f_ini, f_fin, num=n_points) * 2 * np.pi
        ffreq = np.logspace(f_ini, f_fin, num=n_points)
        (mag, phase, freq) = ss_class.ssm.freqresp(wfreq)

        # print(ss_class.outputs.index('vqx_0'))
        ii0 = ss_class.inputs.index(name_in[0])
        ii1 = ss_class.inputs.index(name_in[1])
        oo0 = ss_class.outputs.index(name_out[0])
        oo1 = ss_class.outputs.index(name_out[1])

        # extract indices for inputs/outputs
        if invert is False:
            in0 = ii0
            in1 = ii1
            out0 = oo0
            out1 = oo1
        else:
            in0 = oo0
            in1 = oo1
            out0 = ii0
            out1 = ii1

        # plot
        fig, axs = plt.subplots(4, 2)

        if logx is True and dBy is True:
            axs[0, 0].semilogx(ffreq, 20 * np.log10(abs(mag[out0, in0])))
            axs[0, 1].semilogx(ffreq, 20 * np.log10(abs(mag[out0, in1])))

            axs[1, 0].semilogx(ffreq, 180 / np.pi * (phase[out0, in0]))
            axs[1, 1].semilogx(ffreq, 180 / np.pi * (phase[out0, in1]))

            axs[2, 0].semilogx(ffreq, 20 * np.log10(abs(mag[out1, in0])))
            axs[2, 1].semilogx(ffreq, 20 * np.log10(abs(mag[out1, in1])))

            axs[3, 0].semilogx(ffreq, 180 / np.pi * (phase[out1, in0]))
            axs[3, 1].semilogx(ffreq, 180 / np.pi * (phase[out1, in1]))

            axs[0, 0].set_xlabel('Frequency (Hz)')
            axs[0, 0].set_ylabel('Magnitude (dB)')

            axs[0, 1].set_xlabel('Frequency (Hz)')
            axs[0, 1].set_ylabel('Magnitude (dB)')

            axs[1, 0].set_xlabel('Frequency (Hz)')
            axs[1, 0].set_ylabel('Phase (deg)')

            axs[1, 1].set_xlabel('Frequency (Hz)')
            axs[1, 1].set_ylabel('Phase (deg)')

            axs[2, 0].set_xlabel('Frequency (Hz)')
            axs[2, 0].set_ylabel('Magnitude (dB)')

            axs[2, 1].set_xlabel('Frequency (Hz)')
            axs[2, 1].set_ylabel('Magnitude (dB)')

            axs[3, 0].set_xlabel('Frequency (Hz)')
            axs[3, 0].set_ylabel('Phase (deg)')

            axs[3, 1].set_xlabel('Frequency (Hz)')
            axs[3, 1].set_ylabel('Phase (deg)')

        if logx is False and dBy is True:
            axs[0, 0].plot(ffreq, 20 * np.log10(abs(mag[out0, in0])))
            axs[0, 1].plot(ffreq, 20 * np.log10(abs(mag[out0, in1])))

            axs[1, 0].plot(ffreq, 180 / np.pi * (phase[out0, in0]))
            axs[1, 1].plot(ffreq, 180 / np.pi * (phase[out0, in1]))

            axs[2, 0].plot(ffreq, 20 * np.log10(abs(mag[out1, in0])))
            axs[2, 1].plot(ffreq, 20 * np.log10(abs(mag[out1, in1])))

            axs[3, 0].plot(ffreq, 180 / np.pi * (phase[out1, in0]))
            axs[3, 1].plot(ffreq, 180 / np.pi * (phase[out1, in1]))

            axs[0, 0].set_xlabel('Frequency (Hz)')
            axs[0, 0].set_ylabel('Magnitude (dB)')

            axs[0, 1].set_xlabel('Frequency (Hz)')
            axs[0, 1].set_ylabel('Magnitude (dB)')

            axs[1, 0].set_xlabel('Frequency (Hz)')
            axs[1, 0].set_ylabel('Phase (deg)')

            axs[1, 1].set_xlabel('Frequency (Hz)')
            axs[1, 1].set_ylabel('Phase (deg)')

            axs[2, 0].set_xlabel('Frequency (Hz)')
            axs[2, 0].set_ylabel('Magnitude (dB)')

            axs[2, 1].set_xlabel('Frequency (Hz)')
            axs[2, 1].set_ylabel('Magnitude (dB)')

            axs[3, 0].set_xlabel('Frequency (Hz)')
            axs[3, 0].set_ylabel('Phase (deg)')

            axs[3, 1].set_xlabel('Frequency (Hz)')
            axs[3, 1].set_ylabel('Phase (deg)')

        if logx is True and dBy is False:
            axs[0, 0].semilogx(ffreq, 20 * np.abs(abs(mag[out0, in0])))
            axs[0, 1].semilogx(ffreq, 20 * np.abs(abs(mag[out0, in1])))

            axs[1, 0].semilogx(ffreq, 180 / np.pi * (phase[out0, in0]))
            axs[1, 1].semilogx(ffreq, 180 / np.pi * (phase[out0, in1]))

            axs[2, 0].semilogx(ffreq, 20 * np.abs(abs(mag[out1, in0])))
            axs[2, 1].semilogx(ffreq, 20 * np.abs(abs(mag[out1, in1])))

            axs[3, 0].semilogx(ffreq, 180 / np.pi * (phase[out1, in0]))
            axs[3, 1].semilogx(ffreq, 180 / np.pi * (phase[out1, in1]))

            axs[0, 0].set_xlabel('Frequency (Hz)')
            axs[0, 0].set_ylabel('Magnitude ')

            axs[0, 1].set_xlabel('Frequency (Hz)')
            axs[0, 1].set_ylabel('Magnitude ')

            axs[1, 0].set_xlabel('Frequency (Hz)')
            axs[1, 0].set_ylabel('Phase (deg)')

            axs[1, 1].set_xlabel('Frequency (Hz)')
            axs[1, 1].set_ylabel('Phase (deg)')

            axs[2, 0].set_xlabel('Frequency (Hz)')
            axs[2, 0].set_ylabel('Magnitude ')

            axs[2, 1].set_xlabel('Frequency (Hz)')
            axs[2, 1].set_ylabel('Magnitude ')

            axs[3, 0].set_xlabel('Frequency (Hz)')
            axs[3, 0].set_ylabel('Phase (deg)')

            axs[3, 1].set_xlabel('Frequency (Hz)')
            axs[3, 1].set_ylabel('Phase (deg)')

        else:
            axs[0, 0].plot(ffreq, 20 * np.abs(abs(mag[out0, in0])))
            axs[0, 1].plot(ffreq, 20 * np.abs(abs(mag[out0, in1])))

            axs[1, 0].plot(ffreq, 180 / np.pi * (phase[out0, in0]))
            axs[1, 1].plot(ffreq, 180 / np.pi * (phase[out0, in1]))

            axs[2, 0].plot(ffreq, 20 * np.abs(abs(mag[out1, in0])))
            axs[2, 1].plot(ffreq, 20 * np.abs(abs(mag[out1, in1])))

            axs[3, 0].plot(ffreq, 180 / np.pi * (phase[out1, in0]))
            axs[3, 1].plot(ffreq, 180 / np.pi * (phase[out1, in1]))

            axs[0, 0].set_xlabel('Frequency (Hz)')
            axs[0, 0].set_ylabel('Magnitude ')

            axs[0, 1].set_xlabel('Frequency (Hz)')
            axs[0, 1].set_ylabel('Magnitude ')

            axs[1, 0].set_xlabel('Frequency (Hz)')
            axs[1, 0].set_ylabel('Phase (deg)')

            axs[1, 1].set_xlabel('Frequency (Hz)')
            axs[1, 1].set_ylabel('Phase (deg)')

            axs[2, 0].set_xlabel('Frequency (Hz)')
            axs[2, 0].set_ylabel('Magnitude ')

            axs[2, 1].set_xlabel('Frequency (Hz)')
            axs[2, 1].set_ylabel('Magnitude ')

            axs[3, 0].set_xlabel('Frequency (Hz)')
            axs[3, 0].set_ylabel('Phase (deg)')

            axs[3, 1].set_xlabel('Frequency (Hz)')
            axs[3, 1].set_ylabel('Phase (deg)')


        axs[0, 0].set_title('Yqq')
        axs[0, 1].set_title('Yqd')
        axs[2, 0].set_title('Ydq')
        axs[2, 1].set_title('Ydd')

        axs[1, 0].set_ylim([-180, 180])
        axs[1, 1].set_ylim([-180, 180])
        axs[3, 1].set_ylim([-180, 180])
        axs[3, 1].set_ylim([-180, 180])

        plt.show()

        return ()

    def eigenval_YZ(ss_class, f_ini=0, f_fin=3, name_in=[], name_out=[], n_p=1000, invert = False, type_plot = 're_im'):
        '''
        Eigenvalues plot of a 2x2 system

        :param ss_class: class with the space state, the inputs and the outputs
        :param lim_ini: log of the initial frequency. For instance, -1 represents 10^(-1) Hz
        :param lim_fin: log of the final frequency. For instance, 4 represents 10^(4) Hz
        :param name_in: name of the 2 inputs
        :param name_out: name of the 2 outputs
        :param n_p: number of points to represent. For instance, 1000
        :param invert: divide in / out instead of out / in
        :param type_plot: string to identify if plot in re/im or mag/phase...
        :return: nothing, it just plots
        '''
        # initial definitions
        n_points = n_p
        wfreq = np.logspace(f_ini, f_fin, num=n_points) * 2 * np.pi
        ffreq = np.logspace(f_ini, f_fin, num=n_points)
        (mag, phase, freq) = ss_class.ssm.freqresp(wfreq)

        # print(ss_class.outputs.index('vqx_0'))
        ii0 = ss_class.inputs.index(name_in[0])
        ii1 = ss_class.inputs.index(name_in[1])
        oo0 = ss_class.outputs.index(name_out[0])
        oo1 = ss_class.outputs.index(name_out[1])

        # extract indices for inputs/outputs
        if invert is False:
            in0 = ii0
            in1 = ii1
            out0 = oo0
            out1 = oo1
        else:
            in0 = oo0
            in1 = oo1
            out0 = ii0
            out1 = ii1


        # for each frequency, 2x2 matrix, diagonalize, generate eigen and plot them
        def calc_eig(mag, phase, in0, in1, out0, out1):
            """
            Calculate the eigenvalues of the 2x2 matrix

            :param mag: matrix of magnitudes
            :param phase: matrix of phases
            :return: matrix of the eigenvalues
            """
            lam0vec = []
            lam1vec = []
            for ll in range(n_points):
                # print(mag[0, 0])
                Yqq = mag[out0, in0][ll] * np.exp(1j * phase[out0, in0][ll])
                Yqd = mag[out0, in1][ll] * np.exp(1j * phase[out0, in1][ll])
                Ydq = mag[out1, in0][ll] * np.exp(1j * phase[out1, in0][ll])
                Ydd = mag[out1, in1][ll] * np.exp(1j * phase[out1, in1][ll])
                meig = np.array([[Yqq, Yqd], [Ydq, Ydd]])

                w, v = np.linalg.eig(meig)
                lam0 = w[0]
                lam1 = w[1]

                lam0vec.append(lam0)
                lam1vec.append(lam1)

            return np.array(lam0vec), np.array(lam1vec)


        lam0vec, lam1vec = calc_eig(mag, phase, in0, in1, out0, out1)

        # plot
        fig, axs = plt.subplots(2, 1)

        if type_plot == 're_im':
            # one plot for real, one for imaginary
            axs[0].plot(ffreq, np.real(lam0vec))
            axs[0].plot(ffreq, np.real(lam1vec))
            axs[0].set_xlabel('Frequency (Hz)')
            axs[0].set_ylabel('Magnitude')
            axs[0].set_title('Real')
            axs[0].legend(['lam1', 'lam2'])
            axs[0].axhline(y=0.0, color='r', linestyle='-')

            axs[1].plot(ffreq, np.imag(lam0vec))
            axs[1].plot(ffreq, np.imag(lam1vec))
            axs[1].set_xlabel('Frequency (Hz)')
            axs[1].set_ylabel('Magnitude')
            axs[1].set_title('Imag')
            axs[1].legend(['lam1', 'lam2'])
            axs[1].axhline(y=0.0, color='r', linestyle='-')

        elif type_plot == 'mag_ph':
            # one plot for magnitude, one for phase
            axs[0].plot(ffreq, np.abs(lam0vec))
            axs[0].plot(ffreq, np.abs(lam1vec))
            axs[0].set_xlabel('Frequency (Hz)')
            axs[0].set_ylabel('Magnitude')
            axs[0].set_title('Mag')
            axs[0].legend(['lam1', 'lam2'])
            # axs[0].axhline(y=0.0, color='r', linestyle='-')

            axs[1].plot(ffreq, np.angle(lam0vec) * 90 / (np.pi / 2))
            axs[1].plot(ffreq, np.angle(lam1vec) * 90 / (np.pi / 2))
            axs[1].set_xlabel('Frequency (Hz)')
            axs[1].set_ylabel('Phase')
            axs[1].set_title('Ph')
            axs[1].legend(['lam1', 'lam2'])
            # axs[1].axhline(y=0.0, color='r', linestyle='-')

        plt.show()

        return ()


    def eigen(ss_class, plot=False, prnt=False):
        """
        Graphically show the eigenvalues and print them
        :param ss_class: class from where to extract the ss
        :param plot: if true, plots the eigenvalues map
        :param prnt: if true, prints the eigenvalues
        :return: print eigenvalues
        """

        if prnt is True:
            damp(ss_class.ss)

        if plot is True:
            pp = pole(ss_class.ss)
            pp_re = [ele.real for ele in pp]
            pp_im = [ele.imag for ele in pp]
            plt.scatter(pp_re, pp_im)
            plt.ylabel('Imaginary')
            plt.xlabel('Real')
            plt.show()

        return ()


    def nyquist_YZ(ss_class_act, ss_class_psv, f_ini=0, f_fin=3, name_in=[], name_out=[], n_p=1000, n_arrows=10, invert = False):
        '''
        Nyquist plot with the eigenvalues for a 2x2 system

        :param ss_class_act: active class with the space state, the inputs and the outputs
        :param ss_class_psv: passive class with the space state, the inputs and the outputs
        :param lim_ini: log of the initial frequency. For instance, -1 represents 10^(-1) Hz
        :param lim_fin: log of the final frequency. For instance, 4 represents 10^(4) Hz
        :param name_in: name of the 2 inputs
        :param name_out: name of the 2 outputs
        :param n_p: number of points to represent. For instance, 1000
        :param n_arrows: number of arrows indicating the direction
        :param invert: divide in / out instead of out / in
        :return: nothing, it just plots
        '''
        # initial definitions
        n_points = n_p
        wfreq = np.logspace(f_ini, f_fin, num=n_points, base=10.0) * 2 * np.pi
        ffreq = np.logspace(f_ini, f_fin, num=n_points, base=10.0)
        (mag_act, phase_act, freq) = ss_class_act.ssm.freqresp(wfreq)
        (mag_psv, phase_psv, freq) = ss_class_psv.ssm.freqresp(wfreq)

        # print(ss_class.outputs.index('vqx_0'))
        ii0_act = ss_class_act.inputs.index(name_in[0])
        ii1_act = ss_class_act.inputs.index(name_in[1])
        oo0_act = ss_class_act.outputs.index(name_out[0])
        oo1_act = ss_class_act.outputs.index(name_out[1])

        ii0_psv = ss_class_psv.inputs.index(name_out[0])
        ii1_psv = ss_class_psv.inputs.index(name_out[1])
        oo0_psv = ss_class_psv.outputs.index(name_in[0])
        oo1_psv = ss_class_psv.outputs.index(name_in[1])


        # for each frequency, 2x2 matrix, diagonalize, generate eigen and plot them
        def calc_eig(mag_act, phase_act, mag_psv, phase_psv, in0_act, in1_act, out0_act, out1_act, in0_psv, in1_psv, out0_psv, out1_psv):
            """
            Calculate the eigenvalues of the 2x2 matrix

            :param mag: matrix of magnitudes
            :param phase: matrix of phases
            :return: matrix of the eigenvalues
            """
            lam0vec = []
            lam1vec = []
            lam0_sub2 = 0
            lam0_sub1 = 0
            lam1_sub2 = 0  # 2 previous lambda
            lam1_sub1 = 0  # previous lambda
            for ll in range(n_points):
                # print(mag[0, 0])
                Yqq = mag_act[out0_act, in0_act][ll] * np.exp(1j * phase_act[out0_act, in0_act][ll])
                Yqd = mag_act[out0_act, in1_act][ll] * np.exp(1j * phase_act[out0_act, in1_act][ll])
                Ydq = mag_act[out1_act, in0_act][ll] * np.exp(1j * phase_act[out1_act, in0_act][ll])
                Ydd = mag_act[out1_act, in1_act][ll] * np.exp(1j * phase_act[out1_act, in1_act][ll])

                Zqq = mag_psv[out0_psv, in0_psv][ll] * np.exp(1j * phase_psv[out0_psv, in0_psv][ll])
                Zqd = mag_psv[out0_psv, in1_psv][ll] * np.exp(1j * phase_psv[out0_psv, in1_psv][ll])
                Zdq = mag_psv[out1_psv, in0_psv][ll] * np.exp(1j * phase_psv[out1_psv, in0_psv][ll])
                Zdd = mag_psv[out1_psv, in1_psv][ll] * np.exp(1j * phase_psv[out1_psv, in1_psv][ll])

                mY = np.array([[Yqq, Yqd], [Ydq, Ydd]])
                mZ = np.array([[Zqq, Zqd], [Zdq, Zdd]])
                # mMat = np.multiply(mZ, mY)
                # mMat = mZ@mY
                mMat = np.dot(mZ,mY)

                # print(mZ)
                # print(mY)
                # print(mMat)

                w, v = np.linalg.eig(mMat)
                lam0 = w[0]
                lam1 = w[1]

                tol = 0.01
                tol_ang = np.pi / 100  # for instance, 30 degrees
                factt = 2

                if ll > 1:
                    ang0_prev = (np.imag(lam0_sub1) - np.imag(lam0_sub2)) / (np.real(lam0_sub1) - np.real(lam0_sub2))
                    ang1_prev = (np.imag(lam1_sub1) - np.imag(lam1_sub2)) / (np.real(lam1_sub1) - np.real(lam1_sub2))
                    ang0 = (np.imag(lam0) - np.imag(lam0_sub1)) / (np.real(lam0) - np.real(lam0_sub1))
                    ang1 = (np.imag(lam1) - np.imag(lam1_sub1)) / (np.real(lam1) - np.real(lam1_sub1))

                    Ax0_prev = np.real(lam0_sub1) - np.real(lam0_sub2)
                    Ay0_prev = np.imag(lam0_sub1) - np.imag(lam0_sub2)

                    Ax1_prev = np.real(lam1_sub1) - np.real(lam1_sub2)
                    Ay1_prev = np.imag(lam1_sub1) - np.imag(lam1_sub2)

                    Ax0 = np.real(lam0) - np.real(lam0_sub1)
                    Ay0 = np.imag(lam0) - np.imag(lam0_sub1)

                    Ax1 = np.real(lam1) - np.real(lam1_sub1)
                    Ay1 = np.imag(lam1) - np.imag(lam1_sub1)

                    ang0_prev = Ay0_prev / Ax0_prev
                    ang1_prev = Ay1_prev / Ax1_prev

                    ang0 = np.arctan(Ay0 / Ax0)
                    ang1 = np.arctan(Ay1 / Ax1)

                    abs0 = abs(lam0)
                    abs1 = abs(lam1)
                    abs0_prev = abs(lam0_sub1)
                    abs1_prev = abs(lam1_sub1)

                    condition = abs(abs0 - abs0_prev) > tol and abs(abs1 - abs1_prev) > tol
                    # condition = abs(abs0 - abs0_prev) > tol and abs(abs1 - abs1_prev) > tol

                    # condition = abs(Ax0 - Ax0_prev) > tol or abs(Ay0 - Ay0_prev) > tol
                    # condition = False
                    # if abs(ang0 - ang0_prev) > tol_ang and abs(ang1 - ang1_prev) > tol_ang:
                    # if abs(ang0 - ang0_prev) > tol and abs(ang1 - ang1_prev) > tol:
                    # if abs(ang0 - ang0_prev) > abs(ang1 - ang0_prev) and abs(ang1 - ang1_prev) > abs(ang0 - ang1_prev):
                    # if abs(ang0 - ang0_prev) > tol_ang and abs(ang1 - ang1_prev) > tol_ang:
                    # if abs(ang0 - ang0_prev) > abs(ang0 - ang1_prev) and abs(ang1 - ang1_prev) > abs(ang1 - ang0_prev):

                    # if condition is True:
                    # if abs(abs0 - abs0_prev) > tol and abs(abs1 - abs1_prev) > tol:
                    # if abs(abs0 - abs0_prev) > abs(abs0 - abs1_prev) and abs(abs1 - abs1_prev) > abs(abs1 - abs0_prev):
                    # if abs(abs0 - abs0_prev) > abs(abs0 - abs1_prev) and abs(abs1 - abs1_prev) > abs(abs1 - abs0_prev):
                    if abs(abs0 - abs0_prev) + tol > abs(abs0 - abs1_prev):
                        # print(condition)
                        lam_aux0 = lam0
                        lam0 = lam1
                        lam1 = lam_aux0
                    else:
                        pass

                # update previous
                lam0_sub2 = lam0_sub1
                lam0_sub1 = lam0

                lam1_sub2 = lam1_sub1
                lam1_sub1 = lam1

                lam0vec.append(lam0)
                lam1vec.append(lam1)

            return np.real(np.array(lam0vec)), np.imag(np.array(lam0vec)), np.real(np.array(lam1vec)), np.imag(np.array(lam1vec))


        lam0_re, lam0_im ,lam1_re, lam1_im = calc_eig(mag_act, phase_act, mag_psv, phase_psv, ii0_act, ii1_act, oo0_act, oo1_act, ii0_psv, ii1_psv, oo0_psv, oo1_psv)

        # plot
        # fig, axs = plt.subplots(2, 1)
        # axs[0].plot(ffreq, np.real(lam0vec))
        # axs[0].plot(ffreq, np.imag(lam0vec))
        # axs[0].set_xlabel('Frequency (Hz)')
        # axs[0].set_ylabel('Magnitude')
        # axs[0].set_title('lam 1')
        # axs[0].legend(['Re', 'Im'])
        # axs[0].axhline(y=0.0, color='r', linestyle='-')

        # axs[1].plot(ffreq, np.real(lam1vec))
        # axs[1].plot(ffreq, np.imag(lam1vec))
        # axs[1].set_xlabel('Frequency (Hz)')
        # axs[1].set_ylabel('Magnitude')
        # axs[1].set_title('lam 2')
        # axs[1].legend(['Re', 'Im'])
        # axs[1].axhline(y=0.0, color='r', linestyle='-')

        plt.plot(lam0_re, lam0_im)
        plt.plot(lam1_re, lam1_im)

        u0 = np.diff(lam0_re)
        v0 = np.diff(lam0_im)
        pos_x0 = lam0_re[:-1] + u0 / 2
        pos_y0 = lam0_im[:-1] + v0 / 2
        norm0 = np.sqrt(u0 ** 2 + v0 ** 2)
        stp = int(n_points / n_arrows)
        indx_med = int(len(lam0_re) / 1.5)
        # plt.quiver(pos_x0[0::stp], pos_y0[0::stp], u0[0::stp] / norm0[0::stp], v0[0::stp] / norm0[0::stp], angles="xy", zorder=5, pivot="mid", linewidth=0.1, width=0.01, headwidth=2, headlength=4, headaxislength=4, minlength=0.5, color='blue')
        plt.quiver(pos_x0[indx_med], pos_y0[indx_med], u0[indx_med] / norm0[indx_med], v0[indx_med] / norm0[indx_med], angles="xy", zorder=5, pivot="mid", linewidth=0.1, width=0.01, headwidth=2, headlength=4, headaxislength=4, minlength=0.5, color='blue')

        u1 = np.diff(lam1_re)
        v1 = np.diff(lam1_im)
        pos_x1 = lam1_re[:-1] + u1 / 2
        pos_y1 = lam1_im[:-1] + v1 / 2
        norm1 = np.sqrt(u1 ** 2 + v1 ** 2)
        stp = int(n_points / n_arrows)
        indx_med = int(len(lam0_re) / 1.5)
        plt.quiver(pos_x1[indx_med], pos_y1[indx_med], u1[indx_med] / norm1[indx_med], v1[indx_med] / norm1[indx_med], angles="xy", zorder=5, pivot="mid", linewidth=0.1, width=0.01, headwidth=2, headlength=4, headaxislength=4, minlength=0.5, color='orange')
        # plt.quiver(pos_x1[0::stp], pos_y1[0::stp], u1[0::stp] / norm1[0::stp], v1[0::stp] / norm1[0::stp], angles="xy", zorder=5, pivot="mid", linewidth=0.1, width=0.01, headwidth=2, headlength=4, headaxislength=4, minlength=0.5, color='orange')

        plt.scatter(x=-1, y=0, c='r')

        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.legend(['lam1', 'lam2'])

        plt.show()

        return ()


def check_eigen_py_mt(path_mt, ss_class, f_ini=0, f_fin=3, name_in=[], name_out=[], n_p=1000, invert = False, type_plot='re_im'):
    '''
    Check eigenvalues plot of a 2x2 system

    :param path_mt: path of the .csv file with the matlab data, real and imag
    :param ss_class: class with the space state, the inputs and the outputs
    :param lim_ini: log of the initial frequency. For instance, -1 represents 10^(-1) Hz
    :param lim_fin: log of the final frequency. For instance, 4 represents 10^(4) Hz
    :param name_in: name of the 2 inputs
    :param name_out: name of the 2 outputs
    :param n_p: number of points to represent. For instance, 1000
    :param invert: divide in / out instead of out / in
    :param type_plot: if re/im or mag/ph
    :return: nothing, it just plots
    '''
    # initial definitions
    n_points = n_p
    wfreq = np.logspace(f_ini, f_fin, num=n_points) * 2 * np.pi
    ffreq = np.logspace(f_ini, f_fin, num=n_points)
    (mag, phase, freq) = ss_class.ssm.freqresp(wfreq)

    # print(ss_class.outputs.index('vqx_0'))
    ii0 = ss_class.inputs.index(name_in[0])
    ii1 = ss_class.inputs.index(name_in[1])
    oo0 = ss_class.outputs.index(name_out[0])
    oo1 = ss_class.outputs.index(name_out[1])

    # extract indices for inputs/outputs
    if invert is False:
        in0 = ii0
        in1 = ii1
        out0 = oo0
        out1 = oo1
    else:
        in0 = oo0
        in1 = oo1
        out0 = ii0
        out1 = ii1


    # for each frequency, 2x2 matrix, diagonalize, generate eigen and plot them
    def calc_eig(mag, phase, in0, in1, out0, out1):
        """
        Calculate the eigenvalues of the 2x2 matrix

        :param mag: matrix of magnitudes
        :param phase: matrix of phases
        :return: matrix of the eigenvalues
        """
        lam0vec = []
        lam1vec = []
        for ll in range(n_points):
            # print(mag[0, 0])
            Yqq = mag[out0, in0][ll] * np.exp(1j * phase[out0, in0][ll])
            Yqd = mag[out0, in1][ll] * np.exp(1j * phase[out0, in1][ll])
            Ydq = mag[out1, in0][ll] * np.exp(1j * phase[out1, in0][ll])
            Ydd = mag[out1, in1][ll] * np.exp(1j * phase[out1, in1][ll])
            meig = np.array([[Yqq, Yqd], [Ydq, Ydd]])

            w, v = np.linalg.eig(meig)
            lam0 = w[0]
            lam1 = w[1]

            lam0vec.append(lam0)
            lam1vec.append(lam1)

        return np.array(lam0vec), np.array(lam1vec)


    lam0vec, lam1vec = calc_eig(mag, phase, in0, in1, out0, out1)

    # plot python
    fig, axs = plt.subplots(2, 1)

    # one plot for real, one for imaginary
    if type_plot == 're_im':
        axs[0].plot(ffreq, np.real(lam0vec))
        axs[0].plot(ffreq, np.real(lam1vec))

        axs[1].plot(ffreq, np.imag(lam0vec))
        axs[1].plot(ffreq, np.imag(lam1vec))

        # plot matlab
        mt_mat = pd.read_csv(path_mt)
        freq_mt = mt_mat['f']
        y1_re = mt_mat['y1re']
        y2_re = mt_mat['y2re']
        y1_im = mt_mat['y1im']
        y2_im = mt_mat['y2im']

        axs[0].plot(freq_mt, y1_re, '-.')
        axs[0].plot(freq_mt, y2_re, '-.')

        axs[1].plot(freq_mt, y1_im, '-.')
        axs[1].plot(freq_mt, y2_im, '-.')

        # final edit
        axs[0].set_xlabel('Frequency (Hz)')
        axs[0].set_ylabel('Magnitude')
        axs[0].set_title('Real')
        axs[0].legend(['lam1_py', 'lam2_py', 'lam1_mt', 'lam2_mt'])
        axs[0].axhline(y=0.0, color='r', linestyle='-')

        axs[1].set_xlabel('Frequency (Hz)')
        axs[1].set_ylabel('Magnitude')
        axs[1].set_title('Imag')
        axs[1].legend(['lam1_py', 'lam2_py', 'lam1_mt', 'lam2_mt'])
        axs[1].axhline(y=0.0, color='r', linestyle='-')


    elif type_plot == 'mag_ph':
        axs[0].plot(ffreq, np.abs(lam0vec))
        axs[0].plot(ffreq, np.abs(lam1vec))

        axs[1].plot(ffreq, np.angle(lam0vec) * 90 / (np.pi / 2))
        axs[1].plot(ffreq, np.angle(lam1vec) * 90 / (np.pi / 2))

        # plot matlab
        mt_mat = pd.read_csv(path_mt)
        freq_mt = mt_mat['f']
        y1_abs = mt_mat['y1abs']
        y2_abs = mt_mat['y2abs']
        y1_ph = mt_mat['y1ph']
        y2_ph = mt_mat['y2ph']

        axs[0].plot(freq_mt, y1_abs, '-.')
        axs[0].plot(freq_mt, y2_abs, '-.')

        axs[1].plot(freq_mt, y1_ph, '-.')
        axs[1].plot(freq_mt, y2_ph, '-.')

        # final edit
        axs[0].set_xlabel('Frequency (Hz)')
        axs[0].set_ylabel('Magnitude')
        axs[0].set_title('Mag')
        axs[0].legend(['lam1_py', 'lam2_py', 'lam1_mt', 'lam2_mt'])
        # axs[0].axhline(y=0.0, color='r', linestyle='-')

        axs[1].set_xlabel('Frequency (Hz)')
        axs[1].set_ylabel('Angle')
        axs[1].set_title('Ang')
        axs[1].legend(['lam1_py', 'lam2_py', 'lam1_mt', 'lam2_mt'])
        # axs[1].axhline(y=0.0, color='r', linestyle='-')

    plt.show()

    return ()


def merge_all_minus1(excel_file, RLs, Cs, VSCs, ISum, Xdivs):
    """
    Merges all elements except 1 VSC

    :param RLs: RL list of dataframes
    :param Cs: C list of dataframes
    :param VSCs: VSC list of dataframes
    :param ISum: D matrices for sum(current) = 0
    :param Xdivs: division of repeated names
    :return: nothing, focus on Nyquist plot
    """

    xlsx = pd.ExcelFile(excel_file)
    df_ext_inputs = pd.read_excel(xlsx, 'External_inputs')
    df_ext_outputs = pd.read_excel(xlsx, 'External_outputs')

    # 1 side: VSCs[0]
    side1 = VSCs[0]
    # print(side1.inputs)
    # print(side1.outputs)

    # 2 side: all except VSCs[0]
    full_inputs, full_outputs, full_states = all_names(RLs, Cs, VSCs[1:], ISum)  # merge all ss up to this point
    full_inputs, full_outputs, Xdivs = adapt_in_outs(full_inputs, full_outputs)  # where Xdivs is a class, to manage repeated names

    # 3. final connect
    all_classes = [RLs, Cs, VSCs[1:], ISum, Xdivs]  # unify everything. Use the same order as before!
    ext_inputs, ext_outputs = names_ext_in_outs(df_ext_inputs, df_ext_outputs)

    # add inputs/outputs from VSC[1] manually
    # ext_inputs += VSCs[1].ext_inputs
    ext_inputs += VSCs[0].ext_outputs
    # ext_outputs += VSCs[1].ext_outputs

    net_full = Net(RLs, Cs)  # not important

    # add the external from others, for full2
    # ext_inputs = ext_inputs + other_ext_inputs
    # ext_outputs = ext_outputs + other_ext_outputs

    # full system with appends
    ss_complete = []
    for cl in all_classes:
        for sub_cl in cl:
            ss_complete = append(ss_complete, sub_cl.ssm)

    dic_inputs, dic_outputs, dic_states = dics_in_out_sts(full_inputs, full_outputs, full_states)

    Qq, list_indx_x, list_indx_in, list_indx_out, list_name_x, list_name_in, list_name_out = Qvec_builder_full(ext_inputs, ext_outputs, dic_inputs, dic_outputs, dic_states)

    ss_side2 = connect(ss_complete, Qq, list_indx_in, list_indx_out)

    dfA, dfB, dfC, dfD = FPrinter(ss_side2, list_name_x, list_name_in, list_name_out, prnt=False)  # to nicely print

    class Ss_side2:
        def __init__(self, ss_side2, inputs, outputs):
            self.ssm = ss_side2
            self.ss = ss_side2
            self.inputs = inputs
            self.outputs = outputs

    side2 = Ss_side2(ss_side2, list_name_in, list_name_out)

    # nyquist
    Stability_Analysis.nyquist_YZ(ss_class_act=VSCs[0], ss_class_psv=side2, f_ini=1.0, f_fin=3.0, name_in=['vq_1', 'vd_1'], name_out=['iqxv_1', 'idxv_1'], n_p=10000, n_arrows=5, invert=False)


    # debug
    # print(VSCs[0].ss.A)
    dfA = pd.DataFrame(side2.ss.A)
    dfB = pd.DataFrame(side2.ss.B)
    dfC = pd.DataFrame(side2.ss.C)
    dfD = pd.DataFrame(side2.ss.D)
    writer = pd.ExcelWriter('results/solution.xlsx')
    dfA.to_excel(writer, 'A')
    dfB.to_excel(writer, 'B')
    dfC.to_excel(writer, 'C')
    dfD.to_excel(writer, 'D')
    writer.save()

    return ()


def check_nyq_py_mt(mtlb_file, excel_file, RLs, Cs, VSCs, ISum, Xdivs):
    """
    Merges all elements except 1 VSC

    :param RLs: RL list of dataframes
    :param Cs: C list of dataframes
    :param VSCs: VSC list of dataframes
    :param ISum: D matrices for sum(current) = 0
    :param Xdivs: division of repeated names
    :return: nothing, focus on Nyquist plot
    """

    def nyquist_YZ_py_mt(file_mtlb, ss_class_act, ss_class_psv, f_ini=0, f_fin=3, name_in=[], name_out=[], n_p=1000, n_arrows=10, invert = False):
        '''
        Nyquist plot with the eigenvalues for a 2x2 system

        :param ss_class_act: active class with the space state, the inputs and the outputs
        :param ss_class_psv: passive class with the space state, the inputs and the outputs
        :param lim_ini: log of the initial frequency. For instance, -1 represents 10^(-1) Hz
        :param lim_fin: log of the final frequency. For instance, 4 represents 10^(4) Hz
        :param name_in: name of the 2 inputs
        :param name_out: name of the 2 outputs
        :param n_p: number of points to represent. For instance, 1000
        :param n_arrows: number of arrows indicating the direction
        :param invert: divide in / out instead of out / in
        :return: nothing, it just plots
        '''
        # initial definitions
        n_points = n_p
        wfreq = np.logspace(f_ini, f_fin, num=n_points, base=10.0) * 2 * np.pi
        ffreq = np.logspace(f_ini, f_fin, num=n_points, base=10.0)
        (mag_act, phase_act, freq) = ss_class_act.ssm.freqresp(wfreq)
        (mag_psv, phase_psv, freq) = ss_class_psv.ssm.freqresp(wfreq)

        # print(ss_class.outputs.index('vqx_0'))
        ii0_act = ss_class_act.inputs.index(name_in[0])
        ii1_act = ss_class_act.inputs.index(name_in[1])
        oo0_act = ss_class_act.outputs.index(name_out[0])
        oo1_act = ss_class_act.outputs.index(name_out[1])

        ii0_psv = ss_class_psv.inputs.index(name_out[0])
        ii1_psv = ss_class_psv.inputs.index(name_out[1])
        oo0_psv = ss_class_psv.outputs.index(name_in[0])
        oo1_psv = ss_class_psv.outputs.index(name_in[1])


        # for each frequency, 2x2 matrix, diagonalize, generate eigen and plot them
        def calc_eig(mag_act, phase_act, mag_psv, phase_psv, in0_act, in1_act, out0_act, out1_act, in0_psv, in1_psv, out0_psv, out1_psv):
            """
            Calculate the eigenvalues of the 2x2 matrix

            :param mag: matrix of magnitudes
            :param phase: matrix of phases
            :return: matrix of the eigenvalues
            """
            lam0vec = []
            lam1vec = []
            lam0_sub2 = 0
            lam0_sub1 = 0
            lam1_sub2 = 0  # 2 previous lambda
            lam1_sub1 = 0  # previous lambda
            for ll in range(n_points):
                # print(mag[0, 0])
                Yqq = mag_act[out0_act, in0_act][ll] * np.exp(1j * phase_act[out0_act, in0_act][ll])
                Yqd = mag_act[out0_act, in1_act][ll] * np.exp(1j * phase_act[out0_act, in1_act][ll])
                Ydq = mag_act[out1_act, in0_act][ll] * np.exp(1j * phase_act[out1_act, in0_act][ll])
                Ydd = mag_act[out1_act, in1_act][ll] * np.exp(1j * phase_act[out1_act, in1_act][ll])

                Zqq = mag_psv[out0_psv, in0_psv][ll] * np.exp(1j * phase_psv[out0_psv, in0_psv][ll])
                Zqd = mag_psv[out0_psv, in1_psv][ll] * np.exp(1j * phase_psv[out0_psv, in1_psv][ll])
                Zdq = mag_psv[out1_psv, in0_psv][ll] * np.exp(1j * phase_psv[out1_psv, in0_psv][ll])
                Zdd = mag_psv[out1_psv, in1_psv][ll] * np.exp(1j * phase_psv[out1_psv, in1_psv][ll])

                mY = np.array([[Yqq, Yqd], [Ydq, Ydd]])
                mZ = np.array([[Zqq, Zqd], [Zdq, Zdd]])
                # mMat = np.multiply(mZ, mY)
                # mMat = mZ@mY
                mMat = np.dot(mZ,mY)

                # print(mZ)
                # print(mY)
                # print(mMat)

                w, v = np.linalg.eig(mMat)
                lam0 = w[0]
                lam1 = w[1]

                tol = 0.01
                tol_ang = np.pi / 100  # for instance, 30 degrees
                factt = 2

                if ll > 1:
                    ang0_prev = (np.imag(lam0_sub1) - np.imag(lam0_sub2)) / (np.real(lam0_sub1) - np.real(lam0_sub2))
                    ang1_prev = (np.imag(lam1_sub1) - np.imag(lam1_sub2)) / (np.real(lam1_sub1) - np.real(lam1_sub2))
                    ang0 = (np.imag(lam0) - np.imag(lam0_sub1)) / (np.real(lam0) - np.real(lam0_sub1))
                    ang1 = (np.imag(lam1) - np.imag(lam1_sub1)) / (np.real(lam1) - np.real(lam1_sub1))

                    Ax0_prev = np.real(lam0_sub1) - np.real(lam0_sub2)
                    Ay0_prev = np.imag(lam0_sub1) - np.imag(lam0_sub2)

                    Ax1_prev = np.real(lam1_sub1) - np.real(lam1_sub2)
                    Ay1_prev = np.imag(lam1_sub1) - np.imag(lam1_sub2)

                    Ax0 = np.real(lam0) - np.real(lam0_sub1)
                    Ay0 = np.imag(lam0) - np.imag(lam0_sub1)

                    Ax1 = np.real(lam1) - np.real(lam1_sub1)
                    Ay1 = np.imag(lam1) - np.imag(lam1_sub1)

                    ang0_prev = Ay0_prev / Ax0_prev
                    ang1_prev = Ay1_prev / Ax1_prev

                    ang0 = np.arctan(Ay0 / Ax0)
                    ang1 = np.arctan(Ay1 / Ax1)

                    abs0 = abs(lam0)
                    abs1 = abs(lam1)
                    abs0_prev = abs(lam0_sub1)
                    abs1_prev = abs(lam1_sub1)

                    condition = abs(abs0 - abs0_prev) > tol and abs(abs1 - abs1_prev) > tol
                    # condition = abs(abs0 - abs0_prev) > tol and abs(abs1 - abs1_prev) > tol

                    if abs(abs0 - abs0_prev) + tol > abs(abs0 - abs1_prev):
                        # print(condition)
                        lam_aux0 = lam0
                        lam0 = lam1
                        lam1 = lam_aux0
                    else:
                        pass

                # update previous
                lam0_sub2 = lam0_sub1
                lam0_sub1 = lam0

                lam1_sub2 = lam1_sub1
                lam1_sub1 = lam1

                lam0vec.append(lam0)
                lam1vec.append(lam1)

            return np.real(np.array(lam0vec)), np.imag(np.array(lam0vec)), np.real(np.array(lam1vec)), np.imag(np.array(lam1vec))


        lam0_re, lam0_im ,lam1_re, lam1_im = calc_eig(mag_act, phase_act, mag_psv, phase_psv, ii0_act, ii1_act, oo0_act, oo1_act, ii0_psv, ii1_psv, oo0_psv, oo1_psv)

        plt.plot(lam0_re, lam0_im)
        plt.plot(lam1_re, lam1_im)

        u0 = np.diff(lam0_re)
        v0 = np.diff(lam0_im)
        pos_x0 = lam0_re[:-1] + u0 / 2
        pos_y0 = lam0_im[:-1] + v0 / 2
        norm0 = np.sqrt(u0 ** 2 + v0 ** 2)
        stp = int(n_points / n_arrows)
        indx_med = int(len(lam0_re) / 1.5)
        # plt.quiver(pos_x0[0::stp], pos_y0[0::stp], u0[0::stp] / norm0[0::stp], v0[0::stp] / norm0[0::stp], angles="xy", zorder=5, pivot="mid", linewidth=0.1, width=0.01, headwidth=2, headlength=4, headaxislength=4, minlength=0.5, color='blue')
        plt.quiver(pos_x0[indx_med], pos_y0[indx_med], u0[indx_med] / norm0[indx_med], v0[indx_med] / norm0[indx_med], angles="xy", zorder=5, pivot="mid", linewidth=0.1, width=0.01, headwidth=2, headlength=4, headaxislength=4, minlength=0.5, color='blue')

        u1 = np.diff(lam1_re)
        v1 = np.diff(lam1_im)
        pos_x1 = lam1_re[:-1] + u1 / 2
        pos_y1 = lam1_im[:-1] + v1 / 2
        norm1 = np.sqrt(u1 ** 2 + v1 ** 2)
        stp = int(n_points / n_arrows)
        indx_med = int(len(lam0_re) / 1.5)
        plt.quiver(pos_x1[indx_med], pos_y1[indx_med], u1[indx_med] / norm1[indx_med], v1[indx_med] / norm1[indx_med], angles="xy", zorder=5, pivot="mid", linewidth=0.1, width=0.01, headwidth=2, headlength=4, headaxislength=4, minlength=0.5, color='orange')

        plt.scatter(x=-1, y=0, c='r')

        plt.xlabel('Real')
        plt.ylabel('Imaginary')


        # plot matlab
        # plt.plot(file_mtlb['1re'], file_mtlb['1im'], '--')
        # plt.plot(file_mtlb['2re'], file_mtlb['2im'], '--')
        # print(file_mtlb['1re'])

        # sort matlab
        lam0vec = []
        lam1vec = []
        lam0_sub2 = 0
        lam0_sub1 = 0
        lam1_sub2 = 0  # 2 previous lambda
        lam1_sub1 = 0  # previous lambda
        tol = 0.01

        for ll in range(len(file_mtlb['1re'])):
            lam0_mt = file_mtlb['1re'][ll] + 1j * file_mtlb['1im'][ll]
            lam1_mt = file_mtlb['2re'][ll] + 1j * file_mtlb['2im'][ll]

            if ll > 1:
                abs0 = abs(lam0_mt)
                abs1 = abs(lam1_mt)
                abs0_prev = abs(lam0_sub1)
                abs1_prev = abs(lam1_sub1)

                if abs(abs0 - abs0_prev) + tol > abs(abs0 - abs1_prev):
                    lam_aux0 = lam0_mt
                    lam0_mt = lam1_mt
                    lam1_mt = lam_aux0
                else:
                    pass

            # update previous
            lam0_sub2 = lam0_sub1
            lam0_sub1 = lam0_mt

            lam1_sub2 = lam1_sub1
            lam1_sub1 = lam1_mt

            lam0vec.append(lam0_mt)
            lam1vec.append(lam1_mt)



        plt.plot(lam0_re, lam0_im, 'k-.')
        plt.plot(lam1_re, lam1_im, '-.')



        plt.legend(['lam1_py', 'lam2_py', 'lam1_mt', 'lam2_mt'])

        plt.show()

        return ()



    mtlb_filex = pd.read_csv(mtlb_file)


    xlsx = pd.ExcelFile(excel_file)
    df_ext_inputs = pd.read_excel(xlsx, 'External_inputs')
    df_ext_outputs = pd.read_excel(xlsx, 'External_outputs')

    # 1 side: VSCs[0]
    side1 = VSCs[0]

    # 2 side: all except VSCs[0]
    full_inputs, full_outputs, full_states = all_names(RLs, Cs, VSCs[1:], ISum)  # merge all ss up to this point
    full_inputs, full_outputs, Xdivs = adapt_in_outs(full_inputs, full_outputs)  # where Xdivs is a class, to manage repeated names

    # 3. final connect
    all_classes = [RLs, Cs, VSCs[1:], ISum, Xdivs]  # unify everything. Use the same order as before!
    ext_inputs, ext_outputs = names_ext_in_outs(df_ext_inputs, df_ext_outputs)

    # add inputs/outputs from VSC[1] manually
    ext_inputs += VSCs[0].ext_outputs

    net_full = Net(RLs, Cs)  # not important

    # full system with appends
    ss_complete = []
    for cl in all_classes:
        for sub_cl in cl:
            ss_complete = append(ss_complete, sub_cl.ssm)

    dic_inputs, dic_outputs, dic_states = dics_in_out_sts(full_inputs, full_outputs, full_states)

    Qq, list_indx_x, list_indx_in, list_indx_out, list_name_x, list_name_in, list_name_out = Qvec_builder_full(ext_inputs, ext_outputs, dic_inputs, dic_outputs, dic_states)

    ss_side2 = connect(ss_complete, Qq, list_indx_in, list_indx_out)

    dfA, dfB, dfC, dfD = FPrinter(ss_side2, list_name_x, list_name_in, list_name_out, prnt=False)  # to nicely print

    class Ss_side2:
        def __init__(self, ss_side2, inputs, outputs):
            self.ssm = ss_side2
            self.ss = ss_side2
            self.inputs = inputs
            self.outputs = outputs

    side2 = Ss_side2(ss_side2, list_name_in, list_name_out)

    # nyquist
    nyquist_YZ_py_mt(mtlb_filex, ss_class_act=VSCs[0], ss_class_psv=side2, f_ini=1.0, f_fin=3.0, name_in=['vq_1', 'vd_1'], name_out=['iqxv_1', 'idxv_1'], n_p=10000, n_arrows=5, invert=False)


    # debug
    # print(VSCs[0].ss.A)
    dfA = pd.DataFrame(side2.ss.A)
    dfB = pd.DataFrame(side2.ss.B)
    dfC = pd.DataFrame(side2.ss.C)
    dfD = pd.DataFrame(side2.ss.D)
    writer = pd.ExcelWriter('results/solution.xlsx')
    dfA.to_excel(writer, 'A')
    dfB.to_excel(writer, 'B')
    dfC.to_excel(writer, 'C')
    dfD.to_excel(writer, 'D')
    writer.save()








    return ()




