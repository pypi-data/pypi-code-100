from pprint import pprint
from typing import Dict, List
import bs4
import re
import sys
from prettytable import PrettyTable


def normarize(src: str, allow_space: bool = False):
    src = src.strip()
    src = re.sub(r'(\r|\n|\t|\u3000)', '', src)
    if not allow_space:
        src = src.replace(' ', '')
    return src


def parse_syllabus_detail(html: str):
    result = {}
    doc = bs4.BeautifulSoup(html, 'html.parser')
    ths = doc.select('th')
    for th in ths:
        key = th.text.strip()
        value = th.find_next_sibling().decode_contents(formatter='html').strip()
        result[key] = value
    return result


def parse_syllabus_search_result(html: str):
    result = []
    doc = bs4.BeautifulSoup(html, 'html.parser')
    trs = doc.select('table.normal tbody tr')
    for tr in trs:
        try:
            tds = tr.select('td')
            _src = tds[7].select_one('input[type=button]').get('onclick')
            _regex = re.compile(
                r"refer\('(?P<year>\d+)','(?P<affiliation_code>\d+)','(?P<timetable_code>\d+)','(?P<locale>\w+)',\d+\);")
            _match = _regex.match(_src)
            # semester = normarize(tds[1].text)
            result.append({
                'semester': normarize(tds[2].text),
                'periods': normarize(tds[3].text),
                'timetable_code': normarize(tds[4].text),
                'subject': normarize(tds[5].text),
                'teachers': normarize(tds[6].text, allow_space=True),
                'year': normarize(_match.group('year')),
                'affiliation_code': normarize(_match.group('affiliation_code')),
                # 'timetable_code': normarize(_match.group('timetable_code')),
                'locale': normarize(_match.group('locale')),
            })
        except:
            print('Failed to parse row', file=sys.stderr)
    return result


def clip_string(string, width: int = -1, suffix: str = '...') -> str:
    if len(string) <= width:
        return string
    else:
        return string[0:width-len(suffix)] + suffix


def format_syllabus_search_result(results: List[Dict],
                                  columns: List[str] = ['year', 'semester', 'periods', 'subject', 'teachers', 'affiliation_code', 'timetable_code']) -> PrettyTable:
    rows = []
    for result in results:
        row = []
        for column in columns:
            cell = result[column]
            if column == 'teachers':
                cell = clip_string(cell, 10)
            row.append(cell)
        rows.append(row)

    table = PrettyTable(columns)
    table.add_rows(rows)
    table.align = 'l'
    return table


def format_syllabus_detail_markdown(result: Dict):
    strings = []
    for key, value in result.items():
        strings.append(f"# {key}")
        strings.append(value)
    return '\n\n'.join(strings)


def parse_grades_detail(html: str):
    result = []
    doc = bs4.BeautifulSoup(html, 'html.parser')
    trs = doc.select('table')[2].select('tbody tr')
    for tr in trs:
        tds = tr.select('td')
        result.append({
            'large_class': normarize(tds[1].text),
            'middle_class': normarize(tds[2].text),
            'small_class': normarize(tds[3].text),
            'subject': normarize(tds[4].text),
            'teacher': normarize(tds[5].text),
            'units': normarize(tds[6].text),
            'year': normarize(tds[7].text),
            'semester': normarize(tds[8].text),
            'grade': normarize(tds[9].text),
            'ok': normarize(tds[10].text),
        })
    return result


def format_grades_detail(results: List[Dict],
                         columns: List[str] = ['large_class', 'middle_class', 'small_class', 'subject', 'teacher', 'units', 'year', 'semester', 'grade', 'ok']) -> PrettyTable:
    rows = []
    for result in results:
        row = []
        for column in columns:
            cell = result[column]
            row.append(cell)
        rows.append(row)

    table = PrettyTable(columns)
    table.add_rows(rows)
    table.align = 'l'
    return table


def parse_courses(html: str):
    courses = []
    doc = bs4.BeautifulSoup(html, 'html.parser')
    tds = doc.select('table.rishu-koma table.rishu-koma-inner td')
    for td in tds:
        if a := td.select_one('a[onclick^="return Delete"]'):
            match = re.match(
                r"return DeleteCallA\('(?P<year>\d+)','(?P<affiliation>\d+)','(?P<code>\d+)','(?P<dayofweek>\d+)','(?P<period>\d+)'\)", a.get('onclick'))

            subject = td.select_one('a[onclick^="syllabusRefer"]').text.strip()

            courses.append({
                'subject': subject,
                'year': match.group('year'),
                'affiliation': match.group('affiliation'),
                'code': match.group('code'),
                'dayofweek': int(match.group('dayofweek')),
                'period': int(match.group('period')),
            })
    return courses


if __name__ == '__main__':
    with open('response.html', 'rt', encoding='utf-8') as f:
        html = f.read()

    table = parse_syllabus_detail(html)
    table.align = 'l'
    print(table)
