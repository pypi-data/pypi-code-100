#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:14:48 2021

@author: grat05
"""

import tkinter as tk
from tkinter import messagebox, ttk
from copy import deepcopy

class HSVEntryWidget(tk.Frame):
    def __init__(self, parent, label, data=None):
        tk.Frame.__init__(self, parent)
        self.callback = None
        
        self.data = deepcopy(data)
        if data is None:
            self.data = {}
        for channel in 'HSV':
            if channel not in self.data:
                self.data[channel] = []
        
        self.label = tk.LabelFrame(self, text=label)
        self.label.pack()
        
        self.H_widget = ListRangeEntryWidget(self.label, 'H', self.data['H'])
        self.H_widget.pack(side=tk.LEFT,
                           anchor='n')
        self.H_widget.setCallback(lambda data: self.onUpdate(data, 'H'))
        ttk.Separator(self.label, orient='vertical').pack(side=tk.LEFT,
                                                          padx=10, 
                                                          fill='y')
        
        self.S_widget = ListRangeEntryWidget(self.label, 'S', self.data['S'])
        self.S_widget.pack(side=tk.LEFT,
                           anchor='n')
        self.S_widget.setCallback(lambda data: self.onUpdate(data, 'S'))
        ttk.Separator(self.label, orient='vertical').pack(side=tk.LEFT,
                                                          padx=10,
                                                          fill='y')
        
        self.V_widget = ListRangeEntryWidget(self.label, 'V', self.data['V'])
        self.V_widget.pack(side=tk.LEFT,
                           anchor='n')
        self.V_widget.setCallback(lambda data: self.onUpdate(data, 'V'))
        
    def onUpdate(self, data, channel):
        self.data[channel] = data
        
        if self.callback is not None:
            self.callback(deepcopy(self.data))
        
    def setData(self, data):
        self.data = deepcopy(data)
        for channel in 'HSV':
            if channel not in self.data:
                self.data[channel] = []
        
        self.H_widget.setData(self.data['H'])
        self.S_widget.setData(self.data['S'])
        self.V_widget.setData(self.data['V'])
        
    def setCallback(self, callback):
        self.callback = callback 
        

class ListRangeEntryWidget(tk.Frame):
    def __init__(self, parent, label, data=None):
        tk.Frame.__init__(self, parent)

        if data is None:
            self.data = []
        else:
            self.data = deepcopy(data)
        self.callback = None
        
        label = tk.Label(self, text=label, anchor="w")
        label.grid(row=0, column=0)
        
        self._data = {}
        self._last = None
        for r in self.data:
            self.appendRange(data=r)
        self.appendRange()
        
    def onWrite(self, value, range_id):
        range_widget = self._data[range_id]
        index = range_widget.position
        if value is not None:
            if str(self._last) != range_id:
                self.data[index] = value
            else:
                self.data.append(value)
                self.appendRange()
        else:
            self.removeRange(range_id)
        if self.callback is not None:
            self.callback(deepcopy(self.data))
        
    def removeRange(self, range_id):
        if str(self._last) == range_id:
            return
        
        range_widget = self._data[range_id]
        index = range_widget.position
        del self._data[range_id]
        del self.data[index]
        for widget in self._data.values():
            if widget.position > index:
                widget.position -= 1
                widget.grid(row=widget.position+1, column=0)
        range_widget.destroy()
        
    def appendRange(self, data=None):
        index = len(self._data)
        range_widget = RangeEntryWidget(self, data=data)
        range_widget.setCallback(lambda value: self.onWrite(value, str(range_widget)))
        range_widget.grid(row=index+1, column=0)
        range_widget.position = index
        self._last = range_widget
        self._data[str(range_widget)] = range_widget
        return range_widget
    
    def setData(self, data):
        self.data = deepcopy(data)
        
        for widget in self._data.values():
            widget.destroy()
        self._data = {}
        self._last = None

        for r in self.data:
            self.appendRange(data=r)
        self.appendRange()
        
    def setCallback(self, callback):
        self.callback = callback 

class RangeEntryWidget(tk.Frame):
    def __init__(self, parent, data=None, valid_range=(0, 255)):
        tk.Frame.__init__(self, parent)
        self.callback = None
        self.callback_diff = None
        
        self.valid_range = valid_range
        
        if data is not None:
            min_val = data[0]# if self.onValidate(data[0]) else ''
            max_val = data[1]# if self.onValidate(data[1]) else ''
        else:
            min_val=''
            max_val=''
        
        vcmd = (self.register(self.onValidate), '%P')
        
        self.min_var = tk.IntVar(self, value=min_val)
        self.min_var.trace('w', self.onWrite)
        self.entry_min = tk.Entry(self, 
                                  textvariable=self.min_var,
                                  validate="key", 
                                  validatecommand=vcmd)
        self.entry_min.bind("<FocusOut>", self.onLostFocus)
        self.entry_min.grid(row=0, column=0)
        
        self.max_var = tk.IntVar(self, value=max_val)
        self.max_var.trace('w', self.onWrite)
        self.entry_max = tk.Entry(self,
                                  textvariable=self.max_var,
                                  validate="key", 
                                  validatecommand=vcmd)
        self.entry_max.bind("<FocusOut>", self.onLostFocus)
        self.entry_max.grid(row=0, column=1)
        
    def isRange(self):
        try:
            min_val = self.min_var.get()
            max_val = self.max_var.get()
            return (min_val >= self.valid_range[0] and
                    max_val <= self.valid_range[1] and
                    min_val < max_val)
        except(tk.TclError):
            return False
        
    def onValidate(self, value):
        if value == '':
            return True
        try:
            value = int(value)
        except(ValueError):
            return False
        return (value >= self.valid_range[0] and
                value <= self.valid_range[1])
       
    def onWrite(self, *_):
        if self.callback_diff is not None:
            self.callback_diff()
        
    def onLostFocus(self, event=None):
        names = {str(self.entry_min),
                         str(self.entry_max)}
        if (self.callback is not None and
            str(self.focus_displayof()) not in names):
            num_invalid = 0
            try:
                min_val = self.min_var.get()
            except(tk.TclError):
                num_invalid += 1
            try:
                max_val = self.max_var.get()
            except(tk.TclError):
                num_invalid += 1
            if self.callback is not None:
                if num_invalid == 2:
                    self.callback(None)
                elif num_invalid == 0:
                    self.callback([min_val, max_val])
    
    def setCallback(self, callback):
        self.callback = callback

    def setCallback_ondiff(self, callback):
        self.callback_diff = callback
