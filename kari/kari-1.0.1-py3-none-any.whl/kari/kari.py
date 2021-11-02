'''
Find the number
'''

__author__ = 'kari'
__email__ = 'karthick.sundaram@hotmail.com'

import os, random

def start():
	allArray = []

	for _ in range(21):
		randomNumber = random.randint(10,100)
		while randomNumber in allArray:
			randomNumber = random.randint(10,100)
		allArray.append(randomNumber)

	os.system ('clear')

	print('Think of a number')
	print('    '.join(str(e) for e in allArray))

	input('Enter to continue ...')

	for i in range(3):
		set1 = []
		set2 = []
		set3 = []
		
		count = 1
		
		for i in allArray:
			if count == 1:
				set1.append(i)
			elif count == 2:
				set2.append (i)
			else:
				set3.append (i)
				count = 0
			count = count + 1
			
		os.system('clear')

		print('Set 1 : ' + '    '.join(str(e) for e in set1))
		print('Set 2 : ' + '    '.join(str(e) for e in set2))
		print('Set 3 : ' + '    '.join(str(e) for e in set3))

		userSelection = input('Enter the set number : ')
		if userSelection == '1':
			allArray = set2
			allArray.extend(set1)
			allArray.extend(set3)
		elif userSelection == '2':
			allArray = set1
			allArray.extend(set2)
			allArray.extend(set3)
		elif userSelection == '3':
			allArray = set1
			allArray.extend(set3)
			allArray.extend(set2)
			
	result = set1[3] if userSelection == '1' else set2[3] if userSelection == '2' else set3[3]

	os. system('clear')
	print ('Your number => [ %s ]' % result)