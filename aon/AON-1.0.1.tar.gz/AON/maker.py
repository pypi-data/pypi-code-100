import os
import shutil
import tempo

def make(path):
	n=[i for i in path.split("/")]
	empty('tempo.py')
	file=open(n[-1],'r')
	content=file.read()

	fc=open('tempo.py','w')
	fc.seek(0)
	fc.write('tempo='+content)
	fc.close()

def load():
	t=tempo.tempo
	return t

def empty(path):
	fc=open(path,'w')
	fc.write('')
	fc.close()
	
