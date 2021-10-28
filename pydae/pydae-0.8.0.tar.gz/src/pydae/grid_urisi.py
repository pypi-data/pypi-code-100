# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 13:47:07 2021

@author: jmmau
"""
import numpy as np
import sympy as sym
from pydgrid.pydgrid import grid
import json

def unb_ri_si(data):
    pydgrid_obj = grid()
    pydgrid_obj.read(data)  # Load data
    pydgrid_obj.pf()  # solve power flow
    
    pydgrid_obj.dae = urisi2dae(pydgrid_obj)
    
    if 'vscs' in pydgrid_obj.data:
        for vsc in pydgrid_obj.data['vscs']:
            if vsc['type'] == 'ac3ph3wvdcq':
                ac3ph3wvdcq(pydgrid_obj,vsc)
            if vsc['type'] == 'ac3ph3wpq':
                ac3ph3wpq(pydgrid_obj,vsc)
            if vsc['type'] == 'ac1ph2wpq':
                ac1ph2wpq(pydgrid_obj,vsc)
            
    return pydgrid_obj
    
    
def urisi2dae(grid):
    
    buses_name_list = [item['bus'] for item in grid.buses]
    nodes_list = grid.nodes
    I_node = grid.I_node
    V_node = grid.V_node
    Y_vv = grid.Y_vv
    Y_ii = grid.Y_ii.toarray()
    Y_iv = grid.Y_iv
    Y_vi = grid.Y_vi
    inv_Y_ii = np.linalg.inv(Y_ii)
    N_nz_nodes = grid.params_pf[0].N_nz_nodes
    N_v = grid.params_pf[0].N_nodes_v
    buses_list = [bus['bus'] for bus in grid.buses]
    
    N_v = Y_iv.shape[1]   # number of nodes with known voltages
    I_node_sym_list = []
    V_node_sym_list = []
    v_cplx_list = []
    v_list = []
    v_m_list = []
    i_list = []
    v_list_str = []
    i_list_str = []
    i_node = []
    v_num_list = []
    i_num_list = []
    h_v_m_dict = {}
    h_i_m_dict = {}
    xy_0_dict = {}
    params_dict = {}
    h_dict = {}
    
    n2a = {'1':'a','2':'b','3':'c','4':'n'}
    a2n = {'a':'1','b':'2','c':'3','n':'4'}

    # every voltage bus and current bus injection is generted as sympy symbol
    # the voltages ar named as v_{bus_name}_{n2a[phase]}_r
    # the currents ar named as i_{bus_name}_{n2a[phase]}_r
    inode = 0
    for node in nodes_list:
        bus_name,phase = node.split('.')
        i_real = sym.Symbol(f"i_{bus_name}_{n2a[phase]}_r", real=True)
        i_imag = sym.Symbol(f"i_{bus_name}_{n2a[phase]}_i", real=True)
        v_real = sym.Symbol(f"v_{bus_name}_{n2a[phase]}_r", real=True)
        v_imag = sym.Symbol(f"v_{bus_name}_{n2a[phase]}_i", real=True)    

        v_list += [v_real,v_imag] 
        v_cplx_list += [v_real+1j*v_imag]
        i_list += [i_real,i_imag]
        
        v_m = (v_real**2+v_imag**2)**0.5
        #i_m = (i_real**2+i_imag**2)**0.5

        
        h_v_m_dict.update({f"v_{bus_name}_{n2a[phase]}_m":v_m})
        #h_i_m_dict.update({f"i_{bus_name}_{n2a[phase]}_m":i_m})
    
        v_list_str += [str(v_real),str(v_imag)]
        i_list_str += [str(i_real),str(i_imag)]

        v_num_list += [V_node[inode].real[0],V_node[inode].imag[0]]
        i_num_list += [I_node[inode].real[0],I_node[inode].imag[0]]

        V_node_sym_list += [v_real+sym.I*v_imag]
        I_node_sym_list += [i_real+sym.I*i_imag]

        inode += 1
    
    # symbolic voltage and currents vectors (complex)
    V_known_sym = sym.Matrix(V_node_sym_list[:N_v])
    V_unknown_sym = sym.Matrix(V_node_sym_list[N_v:])
    I_known_sym = sym.Matrix(I_node_sym_list[N_v:])
    I_unknown_sym = sym.Matrix(I_node_sym_list[:N_v])
    
    inv_Y_ii_re = inv_Y_ii.real
    inv_Y_ii_im = inv_Y_ii.imag

    inv_Y_ii_re[np.abs(inv_Y_ii_re)<1e-8] = 0
    inv_Y_ii_im[np.abs(inv_Y_ii_im)<1e-8] = 0

    inv_Y_ii = inv_Y_ii_re+sym.I*inv_Y_ii_im

    #I_aux = ( I_known_sym - Y_iv @ V_known_sym)   # with current injections
    I_aux = (            - Y_iv @ V_known_sym)     # without current injections
    print(I_aux)
    #g_cplx = -V_unknown_sym + inv_Y_ii @ I_aux
    if I_aux.shape[1] == 0:
        g_cplx = -Y_ii @ V_unknown_sym 
    else:
        g_cplx = -Y_ii @ V_unknown_sym + I_aux
    
    
    g_list = []
    for item in g_cplx:
        g_list += [sym.re(item)]
        g_list += [sym.im(item)]

    f_list = []   
    x_list = []        
    x_0_list = []

    y_list   = v_list[2*N_v:]
    y_0_list = v_num_list[2*N_v:]
    
    for item_y,item_y_0 in zip(y_list,y_0_list):
        xy_0_dict.update({f'{item_y}':item_y_0})
    

    u_dict = dict(zip(v_list_str[:2*N_v],v_num_list[:2*N_v]))
    u_dict.update(dict(zip(i_list_str[2*N_v:],i_num_list[2*N_v:])))
    
    # to make grid former voltage input an output
    grid_formers = grid.grid_formers
    
    for gformer in grid_formers:
        if 'monitor' in gformer:
            if gformer['monitor']:
                bus_name = gformer['bus']
                for phase in ['a','b','c']:
                    v_real = sym.Symbol(f"v_{bus_name}_{phase}_r", real=True)
                    v_imag = sym.Symbol(f"v_{bus_name}_{phase}_i", real=True)    
        
                    h_dict.update({f'{v_real}':v_real})
                    h_dict.update({f'{v_imag}':v_imag})

    
    lines = grid.lines
    
    Y_primitive = grid.Y_primitive_sp.toarray()
    A_matrix = grid.A_sp.toarray()
    if V_known_sym.shape == (0,0):
        V_results = V_unknown_sym
    else:
        V_results = sym.Matrix([[V_known_sym],[V_unknown_sym]])
    I_lines = Y_primitive @ A_matrix.T @ V_results
    it_single_line = 0
    
    for trafo in grid.transformers:
        
        if 'conductors_j' in trafo: 
            cond_1 = trafo['conductors_j']
        else:
            cond_1 = trafo['conductors_1']
        if 'conductors_k' in trafo: 
            cond_2 = trafo['conductors_k']
        else:
            cond_2 = trafo['conductors_2']  
        
        I_1a = (I_lines[it_single_line,0])
        I_1b = (I_lines[it_single_line+1,0])
        I_1c = (I_lines[it_single_line+2,0])
        I_1n = (I_lines[it_single_line+3,0])
        
        I_2a = (I_lines[it_single_line+cond_1+0,0])
        I_2b = (I_lines[it_single_line+cond_1+1,0])
        I_2c = (I_lines[it_single_line+cond_1+2,0])

        if cond_1>3: I_1n = (I_lines[it_single_line+cond_1+3,0])
        if cond_2>3: I_2n = (I_lines[it_single_line+cond_2+3,0])

        #I_n = (I_lines[it_single_line+3,0])
        if cond_1 <=3:
            I_1n = I_1a+I_1b+I_1c
        if cond_2 <=3:
            I_2n = I_2a+I_2b+I_2c
            
        
        
        if 'monitor' in trafo:
            if trafo['monitor']:
                           
                bus_j_name = trafo['bus_j']
                bus_k_name = trafo['bus_k']
                i_t_a_r = sym.Symbol(f"i_t_{bus_j_name}_{bus_k_name}_a_r")
                i_t_a_i = sym.Symbol(f"i_t_{bus_j_name}_{bus_k_name}_a_i")
                i_t_b_r = sym.Symbol(f"i_t_{bus_j_name}_{bus_k_name}_b_r")
                i_t_b_i = sym.Symbol(f"i_t_{bus_j_name}_{bus_k_name}_b_i")
                i_t_c_r = sym.Symbol(f"i_t_{bus_j_name}_{bus_k_name}_c_r")
                i_t_c_i = sym.Symbol(f"i_t_{bus_j_name}_{bus_k_name}_c_i")
                g_list += [-i_t_a_r + sym.re(I_lines[it_single_line+0,0])]
                g_list += [-i_t_a_i + sym.im(I_lines[it_single_line+0,0])]
                g_list += [-i_t_b_r + sym.re(I_lines[it_single_line+1,0])]
                g_list += [-i_t_b_i + sym.im(I_lines[it_single_line+1,0])]
                g_list += [-i_t_c_r + sym.re(I_lines[it_single_line+2,0])]
                g_list += [-i_t_c_i + sym.im(I_lines[it_single_line+2,0])]
                y_list += [i_t_a_r]
                y_list += [i_t_a_i]
                y_list += [i_t_b_r]
                y_list += [i_t_b_i]
                y_list += [i_t_c_r]
                y_list += [i_t_c_i] 
                
        it_single_line += cond_1 + cond_2
        
    for line in lines:
        N_conductors = len(line['bus_j_nodes'])
        
        if N_conductors == 3:
            if 'monitor' in line:
                if line['monitor']:
                               
                    bus_j_name = line['bus_j']
                    bus_k_name = line['bus_k']
                    i_l_a_r = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_a_r")
                    i_l_a_i = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_a_i")
                    i_l_b_r = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_b_r")
                    i_l_b_i = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_b_i")
                    i_l_c_r = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_c_r")
                    i_l_c_i = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_c_i")
                    g_list += [-i_l_a_r + sym.re(I_lines[it_single_line+0,0])]
                    g_list += [-i_l_a_i + sym.im(I_lines[it_single_line+0,0])]
                    g_list += [-i_l_b_r + sym.re(I_lines[it_single_line+1,0])]
                    g_list += [-i_l_b_i + sym.im(I_lines[it_single_line+1,0])]
                    g_list += [-i_l_c_r + sym.re(I_lines[it_single_line+2,0])]
                    g_list += [-i_l_c_i + sym.im(I_lines[it_single_line+2,0])]
                    y_list += [i_l_a_r]
                    y_list += [i_l_a_i]
                    y_list += [i_l_b_r]
                    y_list += [i_l_b_i]
                    y_list += [i_l_c_r]
                    y_list += [i_l_c_i]    
            if line['type'] == 'z': it_single_line += N_conductors
            if line['type'] == 'pi': it_single_line += 3*N_conductors

        if N_conductors == 4:
            if 'monitor' in line:
                if line['monitor']:
                               
                    bus_j_name = line['bus_j']
                    bus_k_name = line['bus_k']
                    i_l_a_r = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_a_r")
                    i_l_a_i = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_a_i")
                    i_l_b_r = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_b_r")
                    i_l_b_i = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_b_i")
                    i_l_c_r = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_c_r")
                    i_l_c_i = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_c_i")
                    i_l_n_r = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_n_r")
                    i_l_n_i = sym.Symbol(f"i_l_{bus_j_name}_{bus_k_name}_n_i")
                    g_list += [-i_l_a_r + sym.re(I_lines[it_single_line+0,0])]
                    g_list += [-i_l_a_i + sym.im(I_lines[it_single_line+0,0])]
                    g_list += [-i_l_b_r + sym.re(I_lines[it_single_line+1,0])]
                    g_list += [-i_l_b_i + sym.im(I_lines[it_single_line+1,0])]
                    g_list += [-i_l_c_r + sym.re(I_lines[it_single_line+2,0])]
                    g_list += [-i_l_c_i + sym.im(I_lines[it_single_line+2,0])]
                    g_list += [-i_l_n_r + i_l_a_r + i_l_b_r + i_l_c_r ]
                    g_list += [-i_l_n_i + i_l_a_i + i_l_b_i + i_l_c_i ]
                    y_list += [i_l_a_r]
                    y_list += [i_l_a_i]
                    y_list += [i_l_b_r]
                    y_list += [i_l_b_i]
                    y_list += [i_l_c_r]
                    y_list += [i_l_c_i] 
                    y_list += [i_l_n_r]
                    y_list += [i_l_n_i]
            if line['type'] == 'z': it_single_line += N_conductors
            if line['type'] == 'pi': it_single_line += 3*N_conductors        

    if hasattr(grid,'loads'):
        loads = grid.loads
    else:
        loads = []
    
    for load in loads:
        if load['type'] == '1P+N':
            bus_name = load['bus']
            phase_1 = str(load['bus_nodes'][0])
            i_real_1 = sym.Symbol(f"i_load_{bus_name}_{n2a[phase_1]}_r", real=True)
            i_imag_1 = sym.Symbol(f"i_load_{bus_name}_{n2a[phase_1]}_i", real=True)
            v_real_1 = sym.Symbol(f"v_{bus_name}_{n2a[phase_1]}_r", real=True)
            v_imag_1 = sym.Symbol(f"v_{bus_name}_{n2a[phase_1]}_i", real=True)          
            i_1 = i_real_1 +1j*i_imag_1
            v_1 = v_real_1 +1j*v_imag_1

            phase_2 = str(load['bus_nodes'][1])
            i_real_2 = sym.Symbol(f"i_load_{bus_name}_{n2a[phase_2]}_r", real=True)
            i_imag_2 = sym.Symbol(f"i_load_{bus_name}_{n2a[phase_2]}_i", real=True)
            v_real_2 = sym.Symbol(f"v_{bus_name}_{n2a[phase_2]}_r", real=True)
            v_imag_2 = sym.Symbol(f"v_{bus_name}_{n2a[phase_2]}_i", real=True)          
            i_2 = i_real_2 +1j*i_imag_2
            v_2 = v_real_2 +1j*v_imag_2

            v_12 = v_1 - v_2

            s_1 = v_12*sym.conjugate(i_1)

            p_1,p_2 = sym.symbols(f'p_{bus_name}_1,p_{bus_name}_2', real=True)
            q_1,q_2 = sym.symbols(f'q_{bus_name}_1,q_{bus_name}_2', real=True)

            g_list += [-p_1 + sym.re(s_1)]
            g_list += [-q_1 + sym.im(s_1)]

            y_list += [i_real_1,i_imag_1]
            
            g_list += [sym.re(i_1+i_2)]
            g_list += [sym.im(i_1+i_2)]
            
            # add phase 1 current to g
            bus_idx = grid.nodes.index(f"{bus_name}.{load['bus_nodes'][0]}")
            g_idx = bus_idx - grid.N_nodes_v
            g_list[2*g_idx+0] += i_real_1
            g_list[2*g_idx+1] += i_imag_1    

            print(g_list[2*g_idx+0])
            print(i_real_1)
            print(g_list[2*g_idx+1])
            print(i_imag_1)
            
            # add phase 2 current to g
            bus_idx = grid.nodes.index(f"{bus_name}.{load['bus_nodes'][1]}")
            g_idx = bus_idx - grid.N_nodes_v
            g_list[2*g_idx+0] += i_real_2
            g_list[2*g_idx+1] += i_imag_2  
            
            print(g_list[2*g_idx+0])
            print(i_real_2)
            print(g_list[2*g_idx+1])
            print(i_imag_2)
            
            y_list += [i_real_2,i_imag_2]
            
            i_real,i_imag = sym.symbols(f'i_{bus_name}_{phase}_r,i_{bus_name}_{phase}_i', real=True)

            i_cplx_1 = I_node[grid.nodes.index(f'{bus_name}.{phase_1}')][0]
            y_0_list += [i_cplx_1.real,i_cplx_1.imag]
            i_cplx_2 = I_node[grid.nodes.index(f'{bus_name}.{phase_2}')][0]
            y_0_list += [i_cplx_2.real,i_cplx_2.imag]
            
            
            
            u_dict.pop(f'i_{bus_name}_{n2a[phase_1]}_r')
            u_dict.pop(f'i_{bus_name}_{n2a[phase_1]}_i')
            u_dict.pop(f'i_{bus_name}_{n2a[phase_2]}_r')
            u_dict.pop(f'i_{bus_name}_{n2a[phase_2]}_i')            
            
            p_value = grid.buses[buses_list.index(bus_name)][f'p_{n2a[phase_1]}']
            q_value = grid.buses[buses_list.index(bus_name)][f'q_{n2a[phase_1]}']
            u_dict.update({f'p_{bus_name}_{phase_1}':p_value})
            u_dict.update({f'q_{bus_name}_{phase_1}':q_value})
                
        if load['type'] == '3P+N':
            bus_name = load['bus']
            v_a = V_node_sym_list[nodes_list.index(f'{bus_name}.1')]
            v_b = V_node_sym_list[nodes_list.index(f'{bus_name}.2')]
            v_c = V_node_sym_list[nodes_list.index(f'{bus_name}.3')]
            v_n = V_node_sym_list[nodes_list.index(f'{bus_name}.4')]

            # i_a = I_node_sym_list[nodes_list.index(f'{bus_name}.1')]
            # i_b = I_node_sym_list[nodes_list.index(f'{bus_name}.2')]
            # i_c = I_node_sym_list[nodes_list.index(f'{bus_name}.3')]
            # i_n = I_node_sym_list[nodes_list.index(f'{bus_name}.4')]

            i_a_r,i_a_i = sym.symbols(f'i_load_{bus_name}_a_r,i_load_{bus_name}_a_i', real=True)
            i_b_r,i_b_i = sym.symbols(f'i_load_{bus_name}_b_r,i_load_{bus_name}_b_i', real=True)
            i_c_r,i_c_i = sym.symbols(f'i_load_{bus_name}_c_r,i_load_{bus_name}_c_i', real=True)
            i_n_r,i_n_i = sym.symbols(f'i_load_{bus_name}_n_r,i_load_{bus_name}_n_i', real=True)
            
            i_a = i_a_r + sym.I*i_a_i
            i_b = i_b_r + sym.I*i_b_i
            i_c = i_c_r + sym.I*i_c_i
            i_n = i_n_r + sym.I*i_n_i
            
            v_an = v_a - v_n
            v_bn = v_b - v_n
            v_cn = v_c - v_n

            s_a = v_an*sym.conjugate(i_a)
            s_b = v_bn*sym.conjugate(i_b)
            s_c = v_cn*sym.conjugate(i_c)

            s = s_a + s_b + s_c
            p_a,p_b,p_c = sym.symbols(f'p_{bus_name}_a,p_{bus_name}_b,p_{bus_name}_c', real=True)
            q_a,q_b,q_c = sym.symbols(f'q_{bus_name}_a,q_{bus_name}_b,q_{bus_name}_c', real=True)
            g_list += [-p_a + sym.re(s_a)]
            g_list += [-p_b + sym.re(s_b)]
            g_list += [-p_c + sym.re(s_c)]
            g_list += [-q_a + sym.im(s_a)]
            g_list += [-q_b + sym.im(s_b)]
            g_list += [-q_c + sym.im(s_c)]

            g_list += [sym.re(i_a+i_b+i_c+i_n)]
            g_list += [sym.im(i_a+i_b+i_c+i_n)]


            i_abc_list  = [i_a_r,i_a_i,i_b_r,i_b_i,i_c_r,i_c_i]
            for itg in [1,2,3]:
                 bus_idx = grid.nodes.index(f'{bus_name}.{itg}')
                 g_idx = bus_idx - grid.N_nodes_v
                 g_list[2*g_idx+0] += i_abc_list[2*(itg-1)  ]
                 g_list[2*g_idx+1] += i_abc_list[2*(itg-1)+1]           

            for phase in ['a','b','c']:
                i_real,i_imag = sym.symbols(f'i_load_{bus_name}_{phase}_r,i_load_{bus_name}_{phase}_i', real=True)
                y_list += [i_real,i_imag]
                i_cplx = I_node[grid.nodes.index(f'{bus_name}.{a2n[phase]}')][0]
                y_0_list += [i_cplx.real,i_cplx.imag]
                u_dict.pop(f'i_{bus_name}_{phase}_r')
                u_dict.pop(f'i_{bus_name}_{phase}_i')
                p_value = grid.buses[buses_list.index(bus_name)][f'p_{phase}']
                q_value = grid.buses[buses_list.index(bus_name)][f'q_{phase}']
                u_dict.update({f'p_{bus_name}_{phase}':p_value})
                u_dict.update({f'q_{bus_name}_{phase}':q_value})

                xy_0_dict.update({f'{i_real}':i_cplx.real,f'{i_imag}':i_cplx.imag})
            
            i_real,i_imag = sym.symbols(f'i_load_{bus_name}_n_r,i_load_{bus_name}_n_i', real=True)
            y_list += [i_real,i_imag]    
            i_cplx = I_node[grid.nodes.index(f'{bus_name}.{a2n["n"]}')][0]
            y_0_list += [i_cplx.real,i_cplx.imag]
            xy_0_dict.update({f'{i_real}':i_cplx.real,f'{i_imag}':i_cplx.imag})
            
            
    if hasattr(grid,'grid_feeders'):
        gfeeders = grid.grid_feeders
    else:
        gfeeders = []

    for gfeeder in gfeeders:
    
        bus_name = gfeeder['bus']
        
        v_a = V_node_sym_list[nodes_list.index(f'{bus_name}.1')]
        v_b = V_node_sym_list[nodes_list.index(f'{bus_name}.2')]
        v_c = V_node_sym_list[nodes_list.index(f'{bus_name}.3')]
        #v_n = V_node_sym_list[nodes_list.index(f'{bus_name}.4')]

        i_a = I_node_sym_list[nodes_list.index(f'{bus_name}.1')]
        i_b = I_node_sym_list[nodes_list.index(f'{bus_name}.2')]
        i_c = I_node_sym_list[nodes_list.index(f'{bus_name}.3')]
        #i_n = I_node_sym_list[nodes_list.index(f'{bus_name}.4')]

        #v_an = v_a - v_n
        #v_bn = v_b - v_n
        #v_cn = v_c - v_n

        s_a = v_a*sym.conjugate(i_a)
        s_b = v_b*sym.conjugate(i_b)
        s_c = v_c*sym.conjugate(i_c)

        #s = s_a + s_b + s_c
        p_a,p_b,p_c = sym.symbols(f'p_{bus_name}_a,p_{bus_name}_b,p_{bus_name}_c')
        q_a,q_b,q_c = sym.symbols(f'q_{bus_name}_a,q_{bus_name}_b,q_{bus_name}_c')
        g_list += [-p_a + sym.re(s_a)]
        g_list += [-p_b + sym.re(s_b)]
        g_list += [-p_c + sym.re(s_c)]
        g_list += [-q_a + sym.im(s_a)]
        g_list += [-q_b + sym.im(s_b)]
        g_list += [-q_c + sym.im(s_c)]

#        g_list += [sym.re(i_a+i_b+i_c+i_n)]
#        g_list += [sym.im(i_a+i_b+i_c+i_n)]

        p_total_value = 0.0
        q_total_value = 0.0
        for phase in ['a','b','c']:
            i_real,i_imag = sym.symbols(f'i_{bus_name}_{phase}_r,i_{bus_name}_{phase}_i', real=True)
            y_list += [i_real,i_imag]
            i_cplx = I_node[grid.nodes.index(f'{bus_name}.{a2n[phase]}')][0]
            y_0_list += [i_cplx.real,i_cplx.imag]
            xy_0_dict.update({f'{i_real}':i_cplx.real,f'{i_imag}':i_cplx.imag})
            u_dict.pop(f'i_{bus_name}_{phase}_r')
            u_dict.pop(f'i_{bus_name}_{phase}_i')
            p_value = grid.buses[buses_list.index(bus_name)][f'p_{phase}']
            q_value = grid.buses[buses_list.index(bus_name)][f'q_{phase}']
            p_total_value += p_value
            q_total_value += q_value
        
        
        if 'ctrl_mode' in gfeeder:
            
            if gfeeder['ctrl_mode'] == 'pq':    

                
                # Q control
                u_dict.update({f'p_ref_{bus_name}':p_total_value})
                u_dict.update({f'q_ref_{bus_name}':q_total_value})
                u_dict.update({f'T_pq_{bus_name}':0.2})
                p_ref,q_ref,T_pq = sym.symbols(f'p_ref_{bus_name},q_ref_{bus_name},T_pq_{bus_name}', real=True)

                f_list += [1/T_pq*(-p_a + p_ref/3)]
                f_list += [1/T_pq*(-p_b + p_ref/3)]
                f_list += [1/T_pq*(-p_c + p_ref/3)]
                
                f_list += [1/T_pq*(-q_a + q_ref/3)]
                f_list += [1/T_pq*(-q_b + q_ref/3)]
                f_list += [1/T_pq*(-q_c + q_ref/3)]
                
                x_list += [p_a]
                x_list += [p_b]
                x_list += [p_c]
                
                x_list += [q_a]
                x_list += [q_b]
                x_list += [q_c]
                
                x_0_list += [p_total_value/3]*3
                xy_0_dict.update({f'{p_a}':p_total_value/3,f'{p_b}':p_total_value/3,f'{p_c}':p_total_value/3})
                xy_0_dict.update({f'{q_a}':q_total_value/3,f'{q_b}':q_total_value/3,f'{q_c}':q_total_value/3})
                               

            
            if gfeeder['ctrl_mode'] == 'ctrl_4':    

                
                # Q control
                u_dict.update({f'p_ref_{bus_name}':p_total_value})
                u_dict.update({f'q_ref_{bus_name}':q_total_value})
                u_dict.update({f'T_pq_{bus_name}':0.2})
                p_ref,q_ref,T_pq = sym.symbols(f'p_ref_{bus_name},q_ref_{bus_name},T_pq_{bus_name}', real=True)

                f_list += [1/T_pq*(-p_a + p_ref/3)]
                f_list += [1/T_pq*(-p_b + p_ref/3)]
                f_list += [1/T_pq*(-p_c + p_ref/3)]
                
                f_list += [1/T_pq*(-q_a + q_ref/3)]
                f_list += [1/T_pq*(-q_b + q_ref/3)]
                f_list += [1/T_pq*(-q_c + q_ref/3)]
                
                x_list += [p_a]
                x_list += [p_b]
                x_list += [p_c]
                
                x_list += [q_a]
                x_list += [q_b]
                x_list += [q_c]
                
                x_0_list += [p_total_value/3]*3
                xy_0_dict.update({f'{p_a}':p_total_value/3,f'{p_b}':p_total_value/3,f'{p_c}':p_total_value/3})
                xy_0_dict.update({f'{q_a}':q_total_value/3,f'{q_b}':q_total_value/3,f'{q_c}':q_total_value/3})

                
                # V control
                
                ## compute voltage module
                bus_name_mv = gfeeder['vctrl_buses'][1]
                v_m_lv,v_m_mv = sym.symbols(f'v_m_{bus_name},v_m_{bus_name_mv}', real=True)
                V_base,V_base_mv,S_base = sym.symbols(f'V_base_{bus_name},V_base_{bus_name_mv},S_base_{bus_name}', real=True)
                u_ctrl_v = sym.Symbol(f'u_ctrl_v_{bus_name}', real=True)

                v_a_lv =   V_node_sym_list[nodes_list.index(f'{bus_name}.1')]
                g_list += [-v_m_lv + (sym.re(v_a_lv)**2 + sym.im(v_a_lv)**2)**0.5/V_base]
                y_list += [v_m_lv]
                xy_0_dict.update({f'{v_m_lv}':1.0})
                
                v_a_mv =   V_node_sym_list[nodes_list.index(f'{bus_name_mv}.1')]
                if not v_m_mv in y_list:
                    g_list += [-v_m_mv + (sym.re(v_a_mv)**2 + sym.im(v_a_mv)**2)**0.5/V_base_mv]
                    y_list += [v_m_mv]
                    xy_0_dict.update({f'{v_m_mv}':1.0})
                    
                
                params_dict.update({f'u_ctrl_v_{bus_name}':0.0})
                
                ## V -> q PI
                xi_v,K_p_v,K_i_v = sym.symbols(f'xi_v_{bus_name},K_p_v_{bus_name},K_p_v_{bus_name}', real=True)
                v_loc_ref,Dv_r,Dq_r = sym.symbols(f'v_loc_ref_{bus_name},Dv_r_{bus_name},Dq_r_{bus_name}', real=True)
                i_reac_ref,I_max = sym.symbols(f'i_reac_ref_{bus_name},I_max_{bus_name}', real=True)

                params_dict.update({f'K_p_v_{bus_name}':0.1,f'K_i_v_{bus_name}':0.1,})
                
                

                U_base_1 = grid.buses[buses_name_list.index(bus_name)]['U_kV']*1000
                U_base_2 = grid.buses[buses_name_list.index(bus_name_mv)]['U_kV']*1000

                params_dict.update({f'V_base_{bus_name}':U_base_1/np.sqrt(3),f'V_base_{bus_name_mv}':U_base_1/np.sqrt(3),f'S_base_{bus_name}':2e6,f'{I_max}':0.5})
                v_ref = v_loc_ref + Dv_r
                epsilon_v = v_ref - (v_m_lv*(1.0-u_ctrl_v) + v_m_mv*u_ctrl_v)
               # f_list += [epsilon_v]
               # x_list += [xi_v]  

                g_list += [-i_reac_ref + K_p_v*epsilon_v  + Dq_r] # + K_i_v*xi_v
                g_list += [-q_ref + S_base*sym.Piecewise((-I_max,i_reac_ref<-I_max),(I_max,i_reac_ref>I_max),(i_reac_ref,True))*v_m]
                y_list += [i_reac_ref]
                y_list += [q_ref]
                
                y_0_list += [0.0]                
                u_dict.update({f'v_loc_ref_{bus_name}':1,f'Dv_r_{bus_name}':0,f'Dq_r_{bus_name}':0})
                u_dict.pop(f'q_ref_{bus_name}')
                xy_0_dict.update({f'{xi_v}':0.0,f'{q_ref}':0.0})
        #i_real,i_imag = sym.symbols(f'i_{bus_name}_n_r,i_{bus_name}_n_i', real=True)
        #y_list += [i_real,i_imag]    
        #i_cplx = I_node[grid.nodes.index(f'{bus_name}.{a2n["n"]}')][0]
        #y_0_list += [i_cplx.real,i_cplx.imag]
            
            

    Y_ii = grid.Y_ii.toarray()
    Y_vv = grid.Y_vv
    Y_vi = grid.Y_vi
    inv_Y_ii = np.linalg.inv(Y_ii)
    N_nz_nodes = grid.params_pf[0].N_nz_nodes
    N_v = grid.params_pf[0].N_nodes_v
    nodes_list = grid.nodes
    Y_primitive = grid.Y_primitive_sp.toarray() 
    A_conect = grid.A_sp.toarray()
    node_sorter  = grid.node_sorter
    N_v = grid.N_nodes_v
    
    np.savez('matrices',Y_primitive=Y_primitive,A_conect=A_conect,nodes_list=nodes_list,
             node_sorter=node_sorter,N_v=N_v, Y_vv=Y_vv, Y_vi=Y_vi)
    
    
    with open("grid_data.json", "w") as fobj:
        json.dump(grid.data, fobj, indent=4, sort_keys=True)
    
    return {'g':g_list,'y':y_list,'f':f_list,'x':x_list,
            'params':params_dict,'xy_0_dict':xy_0_dict,
            'u':u_dict,'x_0_list':x_0_list,'y_0_list':y_0_list,'v_list':v_list,'v_m_list':v_m_list,'v_cplx_list':v_cplx_list,
            'h_dict':h_dict,'h_v_m_dict':h_v_m_dict}  


def ac3ph3wvdcq(grid,vsc_data):
    '''
    Converter type v_dc,q_ac 3 phase 3 wire
    
    '''
    
    bus_ac_name = vsc_data['bus_ac']
    bus_dc_name = vsc_data['bus_dc']  
    to_bus_dc_name = vsc_data['to_bus_dc']  
    a_value  = vsc_data['a']   
    b_value  = vsc_data['b']   
    c_value  = vsc_data['c']   
    
    g_vsc = []
    y_vsc = []
    
    ### AC-side
    p_ac,q_ac,p_dc,p_loss = sym.symbols(f'p_{bus_ac_name},q_{bus_ac_name},p_{bus_dc_name},p_loss_{bus_ac_name}',real=True)

    #### AC voltages:
    v_a_r,v_a_i = sym.symbols(f'v_{bus_ac_name}_a_r,v_{bus_ac_name}_a_i',real=True)
    v_b_r,v_b_i = sym.symbols(f'v_{bus_ac_name}_b_r,v_{bus_ac_name}_b_i',real=True)
    v_c_r,v_c_i = sym.symbols(f'v_{bus_ac_name}_c_r,v_{bus_ac_name}_c_i',real=True)
    v_n_r,v_n_i = sym.symbols(f'v_{bus_ac_name}_n_r,v_{bus_ac_name}_n_i',real=True)
    #### AC currents:
    i_a_r,i_a_i = sym.symbols(f'i_vsc_{bus_ac_name}_a_r,i_vsc_{bus_ac_name}_a_i',real=True)
    i_b_r,i_b_i = sym.symbols(f'i_vsc_{bus_ac_name}_b_r,i_vsc_{bus_ac_name}_b_i',real=True)
    i_c_r,i_c_i = sym.symbols(f'i_vsc_{bus_ac_name}_c_r,i_vsc_{bus_ac_name}_c_i',real=True)

    v_a = v_a_r + 1j*v_a_i
    v_b = v_b_r + 1j*v_b_i
    v_c = v_c_r + 1j*v_c_i
    v_n = v_n_r + 1j*v_n_i

    i_a = i_a_r + 1j*i_a_i
    i_b = i_b_r + 1j*i_b_i
    i_c = i_c_r + 1j*i_c_i

    s_a = (v_a - v_n) * sym.conjugate(i_a)
    s_b = (v_b - v_n) * sym.conjugate(i_b)
    s_c = (v_c - v_n) * sym.conjugate(i_c)

    eq_i_a_r =  sym.re(s_a) - p_ac/3
    eq_i_b_r =  sym.re(s_b) - p_ac/3
    eq_i_c_r =  sym.re(s_c) - p_ac/3
    eq_i_a_i =  sym.im(s_a) - q_ac/3
    eq_i_b_i =  sym.im(s_b) - q_ac/3
    eq_i_c_i =  sym.im(s_c) - q_ac/3

    grid.dae['g'] += [eq_i_a_r,eq_i_a_i,
                      eq_i_b_r,eq_i_b_i,
                      eq_i_c_r,eq_i_c_i]
    grid.dae['y'] += [   i_a_r,   i_a_i,
                         i_b_r,   i_b_i,
                         i_c_r,   i_c_i]
    
    i_abc_list  = [i_a_r,i_a_i,i_b_r,i_b_i,i_c_r,i_c_i]
    for itg in [1,2,3]:
        bus_idx = grid.nodes.index(f'{bus_ac_name}.{itg}')
        g_idx = bus_idx - grid.N_nodes_v
        grid.dae['g'][2*g_idx+0] += i_abc_list[2*(itg-1)  ]
        grid.dae['g'][2*g_idx+1] += i_abc_list[2*(itg-1)+1]
    
    a,b,c = sym.symbols(f'a_{bus_ac_name},b_{bus_ac_name},c_{bus_ac_name}',real=True)
    i_rms = sym.sqrt(i_a_r**2+i_a_i**2+0.1) 
    p_simple = a + b*i_rms + c*i_rms*i_rms

    p_vsc_loss = p_simple
    
    i_l_a_r,i_l_n_r = sym.symbols(f'i_l_{bus_dc_name}_{to_bus_dc_name}_a_r,i_l_{bus_dc_name}_{to_bus_dc_name}_n_r')   
    v_dc_a_r,v_dc_n_r  = sym.symbols(f'v_{bus_dc_name}_a_r,v_{bus_dc_name}_n_r')
    
    eq_p_loss = p_loss - p_vsc_loss
    eq_p_ac = p_ac + p_dc + sym.Piecewise((-p_loss, p_dc < 0), (p_loss, p_dc > 0),(p_loss, True))    
    eq_p_dc = -p_dc + i_l_a_r * v_dc_a_r + i_l_n_r * v_dc_n_r    
       
    grid.dae['g'] +=  [eq_p_ac,eq_p_dc, eq_p_loss]
    grid.dae['y'] +=  [   p_ac,   p_dc,    p_loss]  
    grid.dae['u'].update({f'v_dc_{bus_dc_name}':0.0,f'q_{bus_ac_name}':0.0}) 
    grid.dae['params'].update({f'a_{bus_ac_name}':a_value,f'b_{bus_ac_name}':b_value,f'c_{bus_ac_name}':c_value})

    #grid.dae['xy_0_dict'].update({f'v_{bus_dc_name}_a_r':800.0,f'v_{bus_dc_name}_n_r':10.0})

def ac3ph3wpq(grid,vsc_data):
    '''
    Converter type p_ac,q_ac 3 phase 3 wire
    
    '''
    
    ## Model data
    bus_ac_name = vsc_data['bus_ac']
    bus_dc_name = vsc_data['bus_dc']  
    a_value  = vsc_data['a']   
    b_value  = vsc_data['b']   
    c_value  = vsc_data['c']   
    
    ## Voltages:
    v_a_r,v_a_i = sym.symbols(f'v_{bus_ac_name}_a_r,v_{bus_ac_name}_a_i',real=True)
    v_b_r,v_b_i = sym.symbols(f'v_{bus_ac_name}_b_r,v_{bus_ac_name}_b_i',real=True)
    v_c_r,v_c_i = sym.symbols(f'v_{bus_ac_name}_c_r,v_{bus_ac_name}_c_i',real=True)
    v_n_r,v_n_i = sym.symbols(f'v_{bus_ac_name}_n_r,v_{bus_ac_name}_n_i',real=True)
    v_dc_a_r,v_dc_n_r = sym.symbols(f'v_{bus_dc_name}_a_r,v_{bus_dc_name}_n_r',real=True)

    ## Currents:
    i_a_r,i_a_i = sym.symbols(f'i_vsc_{bus_ac_name}_a_r,i_vsc_{bus_ac_name}_a_i',real=True)
    i_b_r,i_b_i = sym.symbols(f'i_vsc_{bus_ac_name}_b_r,i_vsc_{bus_ac_name}_b_i',real=True)
    i_c_r,i_c_i = sym.symbols(f'i_vsc_{bus_ac_name}_c_r,i_vsc_{bus_ac_name}_c_i',real=True) 
    i_dc_a_r,i_dc_n_r = sym.symbols(f'i_vsc_{bus_dc_name}_a_r,i_vsc_{bus_dc_name}_n_r',real=True)


    
    ## Body:
        
    ### AC-side
    p_ac,q_ac,p_dc,p_loss = sym.symbols(f'p_{bus_ac_name},q_{bus_ac_name},p_{bus_dc_name},p_loss_{bus_ac_name}',real=True)
    coef_a,coef_b,coef_c = sym.symbols(f'coef_a_{bus_ac_name},coef_b_{bus_ac_name},coef_c_{bus_ac_name}',real=True)
    
    v_a = v_a_r + 1j*v_a_i
    v_b = v_b_r + 1j*v_b_i
    v_c = v_c_r + 1j*v_c_i
    v_n = v_n_r + 1j*v_n_i

    i_a = i_a_r + 1j*i_a_i
    i_b = i_b_r + 1j*i_b_i
    i_c = i_c_r + 1j*i_c_i

    s_a = (v_a - v_n) * sym.conjugate(i_a)
    s_b = (v_b - v_n) * sym.conjugate(i_b)
    s_c = (v_c - v_n) * sym.conjugate(i_c)

    eq_i_a_r =  sym.re(s_a) - p_ac*coef_a
    eq_i_b_r =  sym.re(s_b) - p_ac*coef_b
    eq_i_c_r =  sym.re(s_c) - p_ac*coef_c
    eq_i_a_i =  sym.im(s_a) - q_ac*coef_a
    eq_i_b_i =  sym.im(s_b) - q_ac*coef_b
    eq_i_c_i =  sym.im(s_c) - q_ac*coef_c


    i_abc_list  = [i_a_r,i_a_i,i_b_r,i_b_i,i_c_r,i_c_i]
    for itg in [1,2,3]:
        bus_idx = grid.nodes.index(f'{bus_ac_name}.{itg}')
        g_idx = bus_idx - grid.N_nodes_v
        grid.dae['g'][2*g_idx+0] += i_abc_list[2*(itg-1)  ]
        grid.dae['g'][2*g_idx+1] += i_abc_list[2*(itg-1)+1]

    ### DC side
    a,b,c = sym.symbols(f'a_{bus_ac_name},b_{bus_ac_name},c_{bus_ac_name}',real=True)
    i_rms = sym.sqrt(i_a_r**2+i_a_i**2+0.1) 
    p_simple = a + b*i_rms + c*i_rms*i_rms

    p_vsc_loss = p_simple

    eq_p_loss = p_loss - p_vsc_loss
    eq_i_dc_a_r = i_dc_a_r + p_dc/(v_dc_a_r-v_dc_n_r+1e-8)
    eq_i_dc_n_r = i_dc_n_r + p_dc/(v_dc_n_r-v_dc_a_r+1e-8)
    eq_p_dc = p_dc - p_ac - sym.Piecewise((-p_loss, p_dc < 0), (p_loss, p_dc > 0),(p_loss, True))


    ## DAE system update
    grid.dae['g'] += [eq_i_a_r,eq_i_a_i,
                      eq_i_b_r,eq_i_b_i,
                      eq_i_c_r,eq_i_c_i]
    grid.dae['y'] += [   i_a_r,   i_a_i,
                         i_b_r,   i_b_i,
                         i_c_r,   i_c_i]

    grid.dae['g'] +=  [eq_i_dc_a_r,eq_i_dc_n_r,eq_p_dc,eq_p_loss]
    grid.dae['y'] +=  [   i_dc_a_r,   i_dc_n_r,   p_dc,   p_loss]  
    grid.dae['u'].update({f'p_{bus_ac_name}':0.0,f'q_{bus_ac_name}':0.0}) 
    grid.dae['xy_0_dict'].update({f'v_{bus_dc_name}_a_r':800.0,f'v_{bus_dc_name}_n_r':10.0})
    
    grid.dae['u'].pop(f'i_{bus_dc_name}_a_r')
    grid.dae['u'].pop(f'i_{bus_dc_name}_n_r')
    grid.dae['params'].update({f'a_{bus_ac_name}':a_value,f'b_{bus_ac_name}':b_value,f'c_{bus_ac_name}':c_value})
    grid.dae['params'].update({f'coef_a_{bus_ac_name}':1/3,f'coef_b_{bus_ac_name}':1/3,f'coef_c_{bus_ac_name}':1/3})

    ## Add current injections to grid equations:
    bus_idx = grid.nodes.index(f'{bus_dc_name}.{1}')
    g_idx = bus_idx - grid.N_nodes_v
    grid.dae['g'][2*g_idx+0] += i_dc_a_r
    grid.dae['g'][2*g_idx+1] += 0.0   

    bus_idx = grid.nodes.index(f'{bus_dc_name}.{4}')
    g_idx = bus_idx - grid.N_nodes_v
    grid.dae['g'][2*g_idx+0] += i_dc_n_r
    grid.dae['g'][2*g_idx+1] += 0.0  
    
    
def ac1ph2wpq(grid,vsc_data):
    '''
    Converter type p_ac,q_ac 1 phase 2 ac wire
    
    '''
    
    bus_ac_name = vsc_data['bus_ac']
    bus_dc_name = vsc_data['bus_dc']  
    a_value  = vsc_data['a']   
    b_value  = vsc_data['b']   
    c_value  = vsc_data['c'] 
    
    
    ### AC-side
    p_ac,q_ac,p_dc = sym.symbols(f'p_{bus_ac_name},q_{bus_ac_name},p_{bus_dc_name}',real=True)

    #### AC voltages:
    v_a_r,v_a_i = sym.symbols(f'v_{bus_ac_name}_a_r,v_{bus_ac_name}_a_i',real=True)
    v_b_r,v_b_i = sym.symbols(f'v_{bus_ac_name}_b_r,v_{bus_ac_name}_b_i',real=True)
    v_c_r,v_c_i = sym.symbols(f'v_{bus_ac_name}_c_r,v_{bus_ac_name}_c_i',real=True)
    v_n_r,v_n_i = sym.symbols(f'v_{bus_ac_name}_n_r,v_{bus_ac_name}_n_i',real=True)
    #### AC currents:
    i_a_r,i_a_i = sym.symbols(f'i_vsc_{bus_ac_name}_a_r,i_vsc_{bus_ac_name}_a_i',real=True)
    i_b_r,i_b_i = sym.symbols(f'i_vsc_{bus_ac_name}_b_r,i_vsc_{bus_ac_name}_b_i',real=True)
    i_c_r,i_c_i = sym.symbols(f'i_vsc_{bus_ac_name}_c_r,i_vsc_{bus_ac_name}_c_i',real=True)
    i_n_r,i_n_i = sym.symbols(f'i_vsc_{bus_ac_name}_n_r,i_vsc_{bus_ac_name}_n_i',real=True)
    
    coef_a,coef_b,coef_c = sym.symbols(f'coef_a_{bus_ac_name},coef_b_{bus_ac_name},coef_c_{bus_ac_name}',real=True)
    
    v_a = v_a_r + 1j*v_a_i
    v_b = v_b_r + 1j*v_b_i
    v_c = v_c_r + 1j*v_c_i
    v_n = v_n_r + 1j*v_n_i

    i_a = i_a_r + 1j*i_a_i
    i_b = i_b_r + 1j*i_b_i
    i_c = i_c_r + 1j*i_c_i

    s_a_g = (v_a-v_n) * sym.conjugate(i_a)
    s_b_g = (v_b-v_n) * sym.conjugate(i_b)
    s_c_g = (v_c-v_n) * sym.conjugate(i_c)

    eq_i_a_r =  sym.re(s_a_g) - p_ac*coef_a
    eq_i_b_r =  sym.re(s_b_g) - p_ac*coef_b
    eq_i_c_r =  sym.re(s_c_g) - p_ac*coef_c
    eq_i_a_i =  sym.im(s_a_g) - q_ac*coef_a
    eq_i_b_i =  sym.im(s_b_g) - q_ac*coef_b
    eq_i_c_i =  sym.im(s_c_g) - q_ac*coef_c
    eq_i_n_r =  i_n_r + i_a_r + i_b_r + i_c_r
    eq_i_n_i =  i_n_i + i_a_i + i_b_i + i_c_i

    grid.dae['g'] += [eq_i_a_r,eq_i_a_i,
                      eq_i_b_r,eq_i_b_i,
                      eq_i_c_r,eq_i_c_i,
                      eq_i_n_r,eq_i_n_i,]
    grid.dae['y'] += [   i_a_r,   i_a_i,
                         i_b_r,   i_b_i,
                         i_c_r,   i_c_i,
                         i_n_r,   i_n_i]

    i_abc_list  = [i_a_r,i_a_i,i_b_r,i_b_i,i_c_r,i_c_i,i_n_r,i_n_i]
    for itg in [1,2,3,4]:
        bus_idx = grid.nodes.index(f'{bus_ac_name}.{itg}')
        g_idx = bus_idx - grid.N_nodes_v
        grid.dae['g'][2*g_idx+0] += i_abc_list[2*(itg-1)  ]
        grid.dae['g'][2*g_idx+1] += i_abc_list[2*(itg-1)+1]

    ### DC side
    a,b,c = sym.symbols(f'a_{bus_ac_name},b_{bus_ac_name},c_{bus_ac_name}',real=True)
    i_rms = sym.sqrt(i_a_r**2+i_a_i**2+0.1) 
    p_vsc_loss = a + b*i_rms + c*i_rms*i_rms

    v_dc_a_r,v_dc_n_r = sym.symbols(f'v_{bus_dc_name}_a_r,v_{bus_dc_name}_n_r',real=True)

    i_dc_a_r,i_dc_n_r = sym.symbols(f'i_vsc_{bus_dc_name}_a_r,i_vsc_{bus_dc_name}_n_r',real=True)

    eq_i_dc_a_r = i_dc_a_r + p_dc/(v_dc_a_r-v_dc_n_r+1e-8)
    eq_i_dc_n_r = i_dc_n_r + p_dc/(v_dc_n_r-v_dc_a_r+1e-8)
    eq_p_dc = p_dc - p_ac + sym.Piecewise((p_vsc_loss, p_dc < 0), (-p_vsc_loss, p_dc > 0),(p_vsc_loss, True))
   
    grid.dae['g'] +=  [eq_i_dc_a_r,eq_i_dc_n_r,eq_p_dc]
    grid.dae['y'] +=  [   i_dc_a_r,   i_dc_n_r,   p_dc]  
    grid.dae['u'].update({f'p_{bus_ac_name}':0.0,f'q_{bus_ac_name}':0.0}) 
    grid.dae['xy_0_dict'].update({f'v_{bus_dc_name}_a_r':800.0,f'v_{bus_dc_name}_n_r':10.0})
    
    grid.dae['u'].pop(f'i_{bus_dc_name}_a_r')
    grid.dae['u'].pop(f'i_{bus_dc_name}_n_r')
    grid.dae['params'].update({f'a_{bus_ac_name}':a_value,f'b_{bus_ac_name}':b_value,f'c_{bus_ac_name}':c_value})
    grid.dae['params'].update({f'coef_a_{bus_ac_name}':1/3,f'coef_b_{bus_ac_name}':1/3,f'coef_c_{bus_ac_name}':1/3})
    

    bus_idx = grid.nodes.index(f'{bus_dc_name}.{1}')
    g_idx = bus_idx - grid.N_nodes_v
    grid.dae['g'][2*g_idx+0] += i_dc_a_r
    grid.dae['g'][2*g_idx+1] += 0.0   

    bus_idx = grid.nodes.index(f'{bus_dc_name}.{4}')
    g_idx = bus_idx - grid.N_nodes_v
    grid.dae['g'][2*g_idx+0] += i_dc_n_r
    grid.dae['g'][2*g_idx+1] += 0.0   

if __name__ == "__main__":

    data = {
            "buses":[
                     {"bus": "B1",  "pos_x":   0, "pos_y":  0, "units": "m", "U_kV":0.4},
                     {"bus": "B2",  "pos_x":  20, "pos_y":  0, "units": "m", "U_kV":0.4},
                     {"bus": "B3",  "pos_x": 120, "pos_y":  0, "units": "m", "U_kV":0.4},
                     {"bus": "B4",  "pos_x": 140, "pos_y":  0, "units": "m", "U_kV":0.4}
                    ],
            "grid_formers":[
                           # {"bus": "B1",
                           # "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
                           # "kV": [0.231, 0.231, 0.231]},
                           # {"bus": "B4",
                           # "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
                           # "kV": [0.231, 0.231, 0.231]}
                           ],
            "lines":[
                     {"bus_j": "B1",  "bus_k": "B2",  "code": "lv_cu_150", "m":  20.0},
                     {"bus_j": "B2",  "bus_k": "B3",  "code": "lv_cu_150", "m": 100.0},
                     {"bus_j": "B3",  "bus_k": "B4",  "code": "lv_cu_150", "m":  20.0},
                    ],
            "loads":[
                     {"bus": "B2" , "kVA": [30.0,30.0,30.0], "pf":[ 1]*3,"type":"3P+N"},
                     {"bus": "B3" , "kVA": [10.0,10.0,70.0], "pf":[ 1]*3,"type":"3P+N"}
                    ],
            "shunts":[
                     {"bus": "B1" , "R": 0.001, "X": 0.0, "bus_nodes": [4,0]},
                     {"bus": "B4" , "R": 0.001, "X": 0.0, "bus_nodes": [4,0]}
                     ],
            "line_codes":
                {"lv_cu_150":  {"Rph":0.167,"Xph":0.08, "Rn":0.167, "Xn": 0.08}
                }
           }
        

    grid_dae = unb_ri_si(data)



