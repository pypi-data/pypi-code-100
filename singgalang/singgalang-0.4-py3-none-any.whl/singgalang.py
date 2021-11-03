import requests
import bs4

def main():
	base_url = "https://hariansinggalang.co.id"
	r = requests.get(base_url)
	assert r.status_code == 200, ""
	
	text = r.text
	soup = bs4.BeautifulSoup(text, 'html.parser')
	header_tag = soup.find_all('h3')
	contents = []
	for tag in header_tag:
		text = tag.text
		new_tag = str(tag.extract())
		contents.append(new_tag)
		
		
	string = '\n'.join([v for v in contents])
	soup = bs4.BeautifulSoup(string, 'html.parser')
	a = soup.find_all('a')
	contents = []
	for tag in a:
		href = tag.get('href')
		title = href.split('/')[-2]
		title = title.replace('-',' ')
		data = {'title':title, 'url':href}
		contents.append(data)
	return contents