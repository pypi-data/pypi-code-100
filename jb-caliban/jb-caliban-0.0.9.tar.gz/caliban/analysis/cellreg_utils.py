# -*- coding: utf-8 -*-
"""
Functions for merging calcium imaging data from different sessions that have
been aligned using CellReg (https://github.com/zivlab/CellReg).

@author: Jack Berry
"""

import os
import glob
import copy
import h5py
import pandas as pd
import numpy as np


def read_cellreg(cellreg_folder, mousename, sessions):
    """
    Loads important data from the CellReg folder. Currently, the only object
    returned is the cell_to_index_map array that is stored in the cellRegistered
    struct.

    Inputs:
        cellreg_folder: str
            Path to the folder containing the output from CellReg. The folder
            structure is assumed to be of the following format:
                cellreg_folder/mouse_name/CellRegfolder_session1_session2/
            Note that the session names must be in the name of the CellReg output
            folder, and the order of the sessions indicates the order used by
            CellReg

        mousename: str
            Name of the mouse

        sessions: list of str
            List of the session names. These names must be in the CellReg output
            folder name.

    Returns:
        cell_df: pandas DataFrame
            DataFrame in which the index (named reg) indicates the registered
            neuron IDs, and the columns (named by session) indicate the original
            neuron IDs for that session.

    """

    folder = os.path.join(cellreg_folder, mousename)
    
    #Get the mouse subfolder containing all CellRegs for that mouse
    cell_regs = next(os.walk(folder))[1]
    
    #Get the CellReg folder for the specified sessions
    cell_reg=''
    for d in cell_regs:
        if all(s in d for s in sessions):
            cell_reg = d
    cellregpath = os.path.join(folder, cell_reg)

    #Read in the cell_to_index_map and rename the index and columns
    filename = glob.glob(os.path.join(cellregpath, 'cellRegistered*'))
    if not filename:
        return None
    f = h5py.File(filename[0], 'r')
    cell_df = pd.DataFrame(np.array(f['cell_registered_struct']['cell_to_index_map'])).T.astype(int)
    cell_df.columns = [s for s in sessions]
    cell_df.index = [x+1 for x in cell_df.index]
    cell_df.index.name = 'Reg'
    return cell_df

def session_to_reg(cell_df, session, neuron):
    """
    Translates the session neuron ID to the registered neuron ID

    Inputs:
        cell_df: pandas DataFrame
            Dataframe representing the cells_to_index_map, ie the return of
            read_CellReg
        session: str
            The session in which the neuron was identified
        neuron: int
            The neuron ID in the session

    Returns:
        n_reg: int
            The registered neuron ID
    """

    n_reg = cell_df.index[cell_df[session] == neuron].item()
    return n_reg

def reg_to_session(cell_df, session, neuron):
    """
    Translates the registered neuron ID to the session neuron ID

    Inputs:
        cell_df: pandas DataFrame
            Dataframe representing the cells_to_index_map, ie the return of
            read_CellReg
        session: str
            The session in which the neuron was identified
        neuron: int
            The registered neuron ID

    Returns:
        n_session: int
            The session neuron ID
    """
    n_session = cell_df.loc[neuron, session]
    return n_session

def reorder_cols(df):
     df1 = df.reindex(sorted(df.columns), axis=1)   
     return df1
     
def register_mouse(mouse, cell_df, session=None):
    """
    Creates a new mouse object in which neuron IDs are given as the registered
    ID instead of the session ID.

    Inputs:
        mouse: Mouse object

        cell_df: pandas DataFrame
            Dataframe representing the cells_to_index_map, ie the return of
            read_CellReg

        session: str
            The session of the mouse object. If none is given, the session
            stored in the mouse object (mouse.session) will be used

    """

    session_neurons = mouse.spikes.columns
    if session is None:
        session = mouse.session
        if session is None:
            print('Error: No session given')
            return None
    reg_n = [session_to_reg(cell_df, session, n) for n in session_neurons]
    reg_mouse = copy.deepcopy(mouse)
    reg_mouse.spikes.columns = reg_n
    reg_mouse.cell_transients.columns = reg_n
    reg_mouse.raw.columns = reg_n
    
    #add silent neurons for all neurons that were not identified in the session
    silent_neuron = np.zeros(len(mouse.spikes))
    silent_ids = cell_df.index[cell_df[session] == 0].tolist()
    silent_df = pd.DataFrame({k:silent_neuron for k in silent_ids})
    
    reg_mouse.spikes = pd.concat([reg_mouse.spikes, silent_df], axis=1)
    reg_mouse.cell_transients = pd.concat([reg_mouse.cell_transients, silent_df], axis=1)
    reg_mouse.raw = pd.concat([reg_mouse.raw, silent_df], axis=1)
    
    #sort columns so that they are in increasing order
    reg_mouse.spikes = reorder_cols(reg_mouse.spikes)
    reg_mouse.cell_transients= reorder_cols(reg_mouse.cell_transients)
    reg_mouse.raw = reorder_cols(reg_mouse.raw)
    
    reg_mouse.spikes_and_beh = pd.concat([reg_mouse.spikes, reg_mouse.behavior],axis=1)

    return reg_mouse
