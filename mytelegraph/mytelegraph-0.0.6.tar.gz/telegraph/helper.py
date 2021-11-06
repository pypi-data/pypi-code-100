import re
import argparse

def tag_it(tag: str, string: str):
	if tag == "img":
		value = f"<img src='{string}'></img>"
		return value
	if tag == "br":
		value = "<br>"
		return value
	if tag == "a":
		link = re.findall(r'\[(.*?)\]', string)
		if link:
			link = link[0]
			string = string.split('[')[0]
			value = f"<{tag} href='{link}'>{string}</{tag}>"
			return value
	else:
		value = f"<{tag}>{string}</{tag}>"
		return value

def main(filename: str):
	data = []
	with open(filename) as f:
		file_to_list = f.read().splitlines()
		
		for file_text in file_to_list:
			tag = file_text.split(':')[0]
			string = file_text.replace(tag + ":" , '')
			string = tag_it(tag, string)
			
			data.append(string)
			
		return data
		
if __name__=="__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filename', help='The file contains plain text you just wrote')
	args = parser.parse_args()
	if args.filename:
		filename = args.filename
	else:
		filename = input('filename: str -> ')
	data = main(filename)
	data = "\n".join([v for v in data])
	f = open(filename.split('.')[0] + ".html", "w")
	f.write(data)