#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 12:31:00 2021

@author: grat05
"""

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import yaml
from copy import deepcopy

from .. import settings
from ..tools import openImage
from .color_entry_widgets import HSVEntryWidget
from .plot_masked_images import MaskShowTool, ComputeMasks, plotImage


class ConfigureColorsWidget(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        #User created color rules
        #Start from default
        self.color_rules = dict(color_rules=deepcopy(settings['color_rules']))
        self.rulesChanged = False
        
        #Create main window
#        self.root = tk.Tk()
        self.title('Color Rules Setup')
        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        
        #Setup image plot window
        self.masks = ComputeMasks(color_rules=self.color_rules['color_rules'])
        with plt.rc_context({'toolbar':'toolmanager'}):
            self.im_fig, self.im_ax = plt.subplots()
            self.im_fig.show()
            #Add toggles for showing masks
            toolmanager = self.im_fig.canvas.manager.toolmanager
            toolbar = self.im_fig.canvas.manager.toolbar
            toolmanager.add_tool('Show Stain', 
                                 MaskShowTool,
                                 mask_name='stain',
                                 masks=self.masks)
            toolbar.add_tool('Show Stain', 'show_masks')
            toolmanager.add_tool('Show Tissue', 
                                 MaskShowTool,
                                 mask_name='tissue',
                                 masks=self.masks)
            toolbar.add_tool('Show Tissue', 'show_masks')
            toolmanager.add_tool('Show Background', 
                                 MaskShowTool,
                                 mask_name='background',
                                 masks=self.masks)
            toolbar.add_tool('Show Background', 'show_masks')
            toolmanager.add_tool('Show Other', 
                                 MaskShowTool,
                                 mask_name='other',
                                 masks=self.masks)
            toolbar.add_tool('Show Other', 'show_masks')
        
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        
        #Add image open
        file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=file_menu)
            
        self.im = None
        self.HSV = None
        self.im_show = None
        self.image_filepath = ''
        self.save_filepath = ''
        self.rules_filepath = ''
        file_menu.add_command(label='Open Image',
                              command=self.openImageAction)
        file_menu.add_command(label='Open Color Rules',
                              command=self.openColorRulesAction)
        file_menu.add_command(label='Save Color Rules',
                              command=self.saveAction)
        file_menu.add_command(label='Save As Color Rules',
                              command=lambda event=None: \
                                  self.saveAction(event=event, saveAs=True))
        
        #Display Color rules
        rules = self.color_rules['color_rules']
        self.background_rules = HSVEntryWidget(self,
                                               'Background',
                                               data=rules['background'])
        self.background_rules.pack(side=tk.TOP)
        self.background_rules.setCallback(lambda data: \
                                          self.onUpdate(data, 'background'))
        
        self.tissue_rules = HSVEntryWidget(self, 
                                           'Tissue',
                                           data=rules['tissue'])
        self.tissue_rules.pack(side=tk.TOP)        
        self.tissue_rules.setCallback(lambda data: \
                                      self.onUpdate(data, 'tissue'))
        
        self.stain_rules = HSVEntryWidget(self, 
                                          'Stain',
                                          data=rules['stain'])
        self.stain_rules.pack(side=tk.TOP)
        self.stain_rules.setCallback(lambda data: \
                                     self.onUpdate(data, 'stain'))
            
        self.statusbar = tk.Label(self,
                                  text="",
                                  bd=1,
                                  relief=tk.SUNKEN,
                                  anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
#        self.root.mainloop()
        
    def onClosing(self):
        if self.rulesChanged: 
            res =  messagebox.askyesnocancel("Quit", 
                                          ("There are unsaved changes."
                                           "Are you sure want to quit?"))
            if res is None:
                return
            elif not res:
                self.saveAction(saveAs=True)
        plt.close(self.im_fig)
        self.destroy()
        self.quit()

    def openImageAction(self, event=None):
        image_filepath = filedialog.askopenfilename(title='Image file')
        if not image_filepath is None and image_filepath != '':
            self.image_filepath = image_filepath
            try:
                self.im = openImage(self.image_filepath)
                self.HSV = np.asarray(self.im.convert('HSV'))
                self.im_show = plotImage(self.im, 
                                         self.HSV,
                                         self.masks,
                                         ax=self.im_ax, 
                                         imshow=self.im_show)
                self.im_fig.show()
                self.masks.setHSV(self.HSV)
                self.masks.computeMasks()
            except(MemoryError):
                self.image_filepath = ''
                self.im = None
                self.HSV = None
                messagebox.showerror(title="Can't Open Image", 
                                     message='Image is too large to process')
            self.im_fig.canvas.draw()
            self.setStatusbar('New image loaded')
                
    def openColorRulesAction(self, event=None):
        rules_filepath = filedialog.askopenfilename(title='Color Rules file',
                                                defaultextension='.yaml',
                                                filetypes=[('color files (.yaml)', '.yaml')])
        if not rules_filepath is None and rules_filepath != '':
            self.rules_filepath = rules_filepath
            with open(self.rules_filepath, 'r') as file:
                self.color_rules = yaml.safe_load(file)
                self.masks.setColorRules(self.color_rules['color_rules'])
                self.resetRuleWidgets()
                self.setStatusbar('Color rules loaded!')
            
    def getSaveFileAction(self, event=None):
        save_filepath = filedialog.asksaveasfilename(title='Save Analysis to csv',
                                        defaultextension='.yaml',
                                        filetypes=[('color files (.yaml)', '.yaml')])
        if not save_filepath is None and save_filepath != '':
            self.save_filepath = save_filepath
    
    def saveAction(self, event=None, saveAs=False):
        if self.save_filepath == '' or saveAs:
            self.getSaveFileAction()
        if self.save_filepath != '':
            self.removeNullColorRules()
            self.rulesChanged = False
            with open(self.save_filepath, 'w') as file:
                yaml.dump(self.color_rules, file)
            self.setStatusbar('Color rules saved')
                
    def resetRuleWidgets(self):
        rules = self.color_rules['color_rules']
        self.background_rules.setData(rules['background'])
        self.tissue_rules.setData(rules['tissue'])
        self.stain_rules.setData(rules['stain'])
                
    def onUpdate(self, data, rule_grp):
        rule = self.color_rules['color_rules'][rule_grp]
        data = {
                    channel: rules 
                    for channel, rules in data.items() 
                    if len(rules) > 0
                }
        if rule != data:
            self.rulesChanged = True
            rule.update(data)
            self.masks.setColorRules(self.color_rules['color_rules'])
            self.setStatusbar(rule_grp+' rules changed!')

    def resetStatusbar(self):
        self.statusbar.configure(text="")
        
    def setStatusbar(self, text):
        self.statusbar.configure(text=text)
        self.after_cancel(self.resetStatusbar)
        self.after(3000, self.resetStatusbar)
        
    def removeNullColorRules(self):
        self.color_rules['color_rules'] =\
            {
                rule_grp: {
                    channel: rules 
                    for channel, rules in hsv_rules.items() 
                    if len(rules) > 0
                    } 
                for rule_grp, hsv_rules in self.color_rules['color_rules'].items()}