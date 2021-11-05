from parser_libraries import functions as f
import os
from bs4 import BeautifulSoup
import logging
import logging.handlers


logging.basicConfig(format=f'%(module)s.{__name__}: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


URL = 'http://duma.gov.ru/duma/chairman/'
HOST = 'http://duma.gov.ru'

def parser():
    log.debug(f"The script {__name__} starts working")
    html = f.get_html(URL)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        name_block = soup.find('h2').find('span')
        name = name_block.get_text()
        for i in range(1, len(name)):
            if name[i].isupper():
                name = name[0: i] + ' ' + name[i:]
                break
        name = name.split()
        image = HOST + soup.find('picture').find('img').get('src')
        bday = soup.find('div', id='person-about').find('dl').find('dt').get_text().replace('\n', '').replace('  ', '')
        bday = f.get_dig_date(bday[0:bday.find(' года')])
        log.debug("The script stops working")
        return [
            {
                'image_link': image,
                'first_name': name[1],
                'middle_name': name[2],
                'last_name': name[0],
                'link': URL,
                'bday': bday['day'],
                'bmonth': bday['month'],
                'byear': bday['year'],
                'position_id': 16
            }
        ]
    else:
        return [{'code': 2, 'script': os.path.basename(__file__)}]

if __name__ == '__main__':
    print(parser())