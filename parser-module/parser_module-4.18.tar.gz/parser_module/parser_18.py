from parser_libraries import functions as f
import os
from bs4 import BeautifulSoup
import logging
import logging.handlers


logging.basicConfig(format=f'%(module)s.{__name__}: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


URL = 'http://duma.gov.ru/duma/factions/'
HOST = 'http://duma.gov.ru'

def get_person(url):
    html = f.get_html(HOST + url)
    soup = BeautifulSoup(html.text, 'html.parser')
    name = soup.find('h1').get_text()
    for i in range(1, len(name)):
        if name[i].isupper():
            name = name[0: i] + ' ' + name[i:]
            break
    name = name.split()

    image = HOST + soup.find('picture', class_='person__image-wrapper').find('img').get('src')
    bday = soup.find('div', class_='content--s').find('div').find('p').get_text()
    bday = f.get_dig_date(bday[bday.find(': ') + 1 : bday.find(' года')])
    return {
        'image_link': image,
        'first_name': name[1],
        'middle_name': name[2],
        'last_name': name[0],
        'link': HOST + url,
        'bday': bday['day'],
        'bmonth': bday['month'],
        'byear': bday['year'],
        'position_id': 18
    }

def parser():
    log.debug(f"The script {__name__} starts working")
    html = f.get_html(URL)
    people = []
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        people_blocks = soup.find('ul', class_='objects-list').find_all('li')

        for person_block in people_blocks:
            try:
                description_block = person_block.find('div', class_='object__description').find_all('div', class_='object__description__col')[1]
                if description_block.find('span', class_='list_small__caption--light').get_text().lower().find(
                        'руководитель') != -1:
                    people.append(get_person(description_block.find('a').get('href')))
            except:
                pass
        log.debug("The script stops working")
        return people
    else:
        return [{'code': 2, 'script': os.path.basename(__file__)}]

if __name__ == '__main__':
    print(parser())
