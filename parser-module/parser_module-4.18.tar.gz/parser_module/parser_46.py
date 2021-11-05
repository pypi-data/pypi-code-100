import os
from parser_libraries import functions as f
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import logging
import logging.handlers

# Президиум ВАС РФ

logging.basicConfig(format=f'%(module)s.{__name__}: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


URL = "http://arbitr.ru/struct/judges/presidium/"
HOST = "http://arbitr.ru"


def get_person(a_row):
    link = HOST + a_row.get('href')
    name = a_row.get_text().split()
    html = f.get_html(link)
    http_enc = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    html_enc = EncodingDetector.find_declared_encoding(html.content, is_html=True)
    enc = html_enc or http_enc
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding=enc)

    try:
        name_pos_block = soup.find('h3').find_next_sibling('div').find('p').find_parent()
        pos_block = name_pos_block.find('p').find_next('em')

        for e in pos_block.find_all('br'):
            e.extract()

        pos = pos_block.get_text().replace('\r\n', ' ').replace('\n', '').lower()

        try:
            image_link = HOST + name_pos_block.find_all('img')[0].get('src')
        except:
            image_link = HOST + name_pos_block.find_parent().find_all('img')[0].get('src')
        try:
            bday_block = name_pos_block.find_all('p')[2]
        except:
            bday_block = name_pos_block.find_parent('td').find_all('p')[1]
        bday = bday_block.get_text()
        bday = f.get_dig_date(bday[bday.find(' ')+1 : bday.find(' года')])
        if bday == -1:
            try:
                bday_block = name_pos_block.find_all('p')[1]
                bday = bday_block.get_text()
                bday = f.get_dig_date(bday[bday.find(' ') + 1: bday.find(' года')])
            except:
                bday_block = name_pos_block.find_parent().find_all('p')[2]
                bday = bday_block.get_text()
                bday = f.get_dig_date(bday[bday.find(' ') + 1: bday.find(' года')])

        if pos.find('заместитель') != -1 or pos.find('судья') != -1 or pos.find('состава') != -1:
            pos = 47
        else:
            pos = 46

        return {
            'image_link': image_link,
            'first_name': name[1],
            'middle_name': name[2],
            'last_name': name[0],
            'link': link,
            'bday': bday['day'],
            'bmonth': bday['month'],
            'byear': bday['year'],
            'position_id': pos
        }
    except:
        return None


def parser():
    log.debug(f"The script {__name__} starts working")
    html = f.get_html(URL)
    if html.status_code == 200:
        http_enc = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
        html_enc = EncodingDetector.find_declared_encoding(html.content, is_html=True)
        enc = html_enc or http_enc
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding=enc)
        table = soup.find('blockquote')
        rows = table.find_all('a')
        people = []
        for row in rows:
            person = get_person(row)
            people.append(person)
        if people == 1:
            return [{'code': 1, 'script': os.path.basename(__file__)}]
        log.debug("The script stops working")
        return people
    else:
        return [{'code': 2, 'script': os.path.basename(__file__)}]

if __name__ == '__main__':
    print(parser())