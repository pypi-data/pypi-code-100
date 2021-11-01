#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:05:58 2021

@author: grat05
"""


import tkinter as tk
from tkinter import filedialog
import yaml

from .. import settings

class ConfigureRunWidget(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title('Fibrosis Quantification Settup')
        self.protocol("WM_DELETE_WINDOW", self.quitAction)
       
        #Add directory filepaths input
        self.filepaths = []
        self.image_files_text = tk.Text(self, height = 8)
        self.image_files_text.config(state='disabled')
        self.image_files_text.grid(sticky="WE", row=1, column=0, columnspan=2)
        image_files_button = tk.Button(self, text='Choose Images', 
                                       command=self.getImagesAction)
        image_files_button.grid(row=1, column=2)
        
        #Add CSV filepath input
        self.save_filepath = ''
        self.save_file_text = tk.Text(self, height = 1)
        self.save_file_text.config(state='disabled')
        self.save_file_text.grid(sticky="WE", row=2, column=0, columnspan=2)
        save_file_button = tk.Button(self, text='Choose Save File', 
                                     command=self.getSaveFileAction)
        save_file_button.grid(row=2, column=2)
        
        #Add directory path for saving images
        self.save_dirpath = ''
        self.save_directory_text = tk.Text(self, height = 1)
        self.save_directory_text.config(state='disabled')
        self.save_directory_text.grid(sticky="WE", row=3, column=0, columnspan=2)
        save_directory_button = tk.Button(self, text='Choose Save Directory', 
                                          command=self.getSaveDirAction)
        save_directory_button.grid(row=3, column=2)
        
        #Add color rules filepath
        self.color_rules_filepath = ''
        self.color_rules_text = tk.Text(self, height = 1)
        self.color_rules_text.insert(0.,'<Default>')
        #The <Default> is AFAT.color_rules_default
        self.color_rules_text.config(state='disabled')
        self.color_rules_text.grid(sticky="WE", row=4, column=0, columnspan=1)
        color_rules_reset_button = tk.Button(self, text='Reset',
                                       command=self.resetColorRulesAction)
        color_rules_reset_button.grid(row=4, column=1)
        color_rules_button = tk.Button(self, text='Color Rules File', 
                                       command=self.getColorRulesAction)
        color_rules_button.grid(row=4, column=2)
        
        #Add settings filepath
        self.settings_filepath = ''
        self.settings_text = tk.Text(self, height = 1)
        self.settings_text.insert(0.,'<Default>')
        #The <Default> is AFAT.settings
        self.settings_text.config(state='disabled')
        self.settings_text.grid(sticky="WE", row=5, column=0, columnspan=1)
        settings_reset_button = tk.Button(self, text='Reset',
                                       command=self.resetSettingsAction)
        settings_reset_button.grid(row=5, column=1)
        settings_button = tk.Button(self, text='Settings File', 
                                       command=self.getSettingsAction)
        settings_button.grid(row=5, column=2)
        
        #Add checkboxes for ploting and saving images
        self.save_images_var = tk.BooleanVar(self, value=settings['save_images'])
        save_images_check = tk.Checkbutton(self, text="Save Images", 
                                           variable=self.save_images_var)
        save_images_check.grid(row=6,column=0)
        
        self.show_images_var = tk.BooleanVar(self, value=settings['show_images'])
        show_images_check = tk.Checkbutton(self, text="Show Images", 
                                           variable=self.show_images_var)
        show_images_check.grid(row=7,column=0)
        
        self.save_settings_var = tk.BooleanVar(self, value=settings['save_settings'])
        save_settings_check = tk.Checkbutton(self, text="Save Settings", 
                                           variable=self.save_settings_var)
        save_settings_check.grid(row=8,column=0)
        
        #Add close button
        # This will update run_analysis to true so that we can tell this
        # button was used to close the gui vs the X button
        self.run_analysis = False
        run_button = tk.Button(self, text='Run Analysis', 
                               command=self.closeAction)
        run_button.grid(row=8, column=2)

    def getImagesAction(self, event=None):
        self.filepaths = filedialog.askopenfilenames(title='Select Files for Fibrosis')
        self.filepaths = [] if self.filepaths == '' else self.filepaths
        self.image_files_text.config(state='normal')
        self.image_files_text.delete(1., "end")
        self.image_files_text.insert(1., ';\n'.join(self.filepaths))
        self.image_files_text.config(state='disabled')
    
    def getSaveFileAction(self, event=None):
        save_filepath = filedialog.asksaveasfilename(title='Save Analysis to csv',
                                        defaultextension='.csv',
                                        filetypes=[('csv files', '.csv')])
        if not save_filepath is None and save_filepath != '':
            self.save_filepath = save_filepath
            self.save_file_text.config(state='normal')
            self.save_file_text.delete(1., "end")
            self.save_file_text.insert(1., self.save_filepath)
            self.save_file_text.config(state='disabled')
    
    def getSaveDirAction(self, event=None):
        save_dirpath = filedialog.askdirectory(title='Directory to save images')
        if not save_dirpath is None and save_dirpath != '':
            self.save_dirpath = save_dirpath
            self.save_directory_text.config(state='normal')
            self.save_directory_text.delete(1., "end")
            self.save_directory_text.insert(1., self.save_dirpath)
            self.save_directory_text.config(state='disabled')
        
    def resetColorRulesAction(self, event=None):
        self.color_rules_filepath = ''
        self.color_rules_text.config(state='normal')
        self.color_rules_text.delete(1., "end")
        self.color_rules_text.insert(1., '<Default>')
        self.color_rules_text.config(state='disabled')
        
    def getColorRulesAction(self, event=None):
        color_rules_filepath = filedialog.askopenfilename(title='Select Color rules file to use',
                                                  filetypes=[("Color rules file (.yaml)",'.yaml')])
        if not color_rules_filepath is None and color_rules_filepath != '':
            self.color_rules_filepath = color_rules_filepath
            self.color_rules_text.config(state='normal')
            self.color_rules_text.delete(1., "end")
            self.color_rules_text.insert(1., self.color_rules_filepath)
            self.color_rules_text.config(state='disabled')
            
    def resetSettingsAction(self, event=None):
        self.settings_filepath = ''
        self.settings_text.config(state='normal')
        self.settings_text.delete(1., "end")
        self.settings_text.insert(1., '<Default>')
        self.settings_text.config(state='disabled')
        
    def getSettingsAction(self, event=None):
        settings_filepath = filedialog.askopenfilename(title='Select settings file to use',
                                                  filetypes=[("Settings file (.yaml)",'.yaml')])
        if not settings_filepath is None and settings_filepath != '':
            self.settings_filepath = settings_filepath
            self.settings_text.config(state='normal')
            self.settings_text.delete(1., "end")
            self.settings_text.insert(1., self.settings_filepath)
            self.settings_text.config(state='disabled')
            
    def closeAction(self, event=None):
        if self.settings_filepath != '':
            with open(self.settings_filepath, 'r') as stream:
                new_settings = yaml.safe_load(stream)
                settings.update(new_settings)
        
        settings['save_images'] = self.save_images_var.get()
        settings['show_images'] = self.show_images_var.get()
        settings['save_settings'] = self.save_settings_var.get()
        if self.color_rules_filepath == '':
            self.color_rules_filepath = None
        self.run_analysis = True
        
        self.destroy()
        self.quit()
        
    def quitAction(self, event=None):
        self.destroy()
        self.quit()
