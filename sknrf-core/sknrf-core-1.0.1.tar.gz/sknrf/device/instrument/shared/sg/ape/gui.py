# -*- coding: utf-8 -*-
#!/usr/bin/env python

# #############################################################################
#  ATTENTION
# #############################################################################
#
#  This software is for guidance only. It is provided "as is".
#  It only aims at providing coding information to the customer in order for
#  them to save time. As a result no warranties, whether express, implied or
#  statutory, including, but not limited to implied warranties of
#  merchantability and fitness for a particular purpose apply to this software.
#  A·P·E Angewandte Physik und Elektronik GmbH shall not be held liable for any
#  direct, indirect or consequential damages with respect to any claims arising
#  from the content of such sourcecode and/or the use made by customers of the
#  coding information contained herein in connection with their products.
#
#  File Version: 1.0
#
#  Changelog:
#	1.0 - Initial Version
#
# #############################################################################

import sys
import os

class Control:
	# static instance member
	__instance = None
	
	# object member
	version = 0
	startedFromGui = False
	
	def __init__(self):
		Control.__instance = self
		self.version = 1
		guiControl = os.environ.get('QUANTIFLASH_GUI_CONTROL')
		self.startedFromGui = (guiControl is not None) and (guiControl=='ON')
	
	# create a singleton instance
	@staticmethod
	def instance():
		if Control.__instance is None:
			Control.__instance = Control()
		return Control.__instance
	
	def isStartedFromGui(self):
		return self.startedFromGui
	
	# print #task=text
	def task(self, text):
		if self.isStartedFromGui():
			print( "#task=" + text )
		else:
			print( "TASK: " + text )
	
	# print #progress=0-100
	def progress(self, value):
		if self.isStartedFromGui():
			print( "#progress=" + str(value) )
		else:
			print( "PROGRESS: " + str(value) )
	
	# print #input[=text]
	# wait for input()
	# open textfield popup with optional message or “Enter value:” and OK&Cancel
	# Cancel terminate the script
	# return: String value from Input-Popup
	def input(self, text = ''):
		if self.isStartedFromGui():
			line = "#input"
		else:
			line = "INPUT: "
		if text != '':
			line += "=" + text
		print(line)
		return input()
	
	# print #error=errormsg
	# terminate the script
	def error(self, errormsg, errorcode = 1):
		if self.isStartedFromGui():
			print("#error=" + errormsg)
		else:
			print("ERROR: " + errormsg)
		sys.exit(errorcode)
	
	# print #console=hide/show
	def consoleVisible(self, visible):
		if self.isStartedFromGui():
			if visible:
				print("#console=show")
			else:
				print("#console=hide")
		else:
			print("GUI CONSOLE NOT AVAILABLE!")
		
	# print #open=file_path
	# open file with OS assigned app
	def openFile(self, path):
		if self.isStartedFromGui():
			print("#open=" + path)
		else:
			print("GUI OPENER NOT AVAILABLE!")
	
	# print #confirm=text[|btn1[|…]]
	# wait for input()
	# open popup with OK&Cancel or user selected list of buttons
	# return: String value from clicked button (label)
	def confirm(self, text, *args, **kwargs):
		buttons = ""
		for ar in args:
			button += "|" + ar
		if self.isStartedFromGui():
			print("#confirm=" + text + buttons)
		else:
			print("CONFIRM (input one label): " + buttons)
		return input()
	
	# print #var <varname>=<value>
	def setGlobalVar(self, varname, value):
		if self.isStartedFromGui():
			line = "#var "
		else:
			line = "VAR: "
		line += varname + "=" + value
		print(line)
	
	# print #var <varname>
	def getGlobalVar(self, varname):
		if self.isStartedFromGui():
			line = "#var "
		else:
			line = "VAR: "
		line += varname
		print(line)
		return input()
