import bs4
import time
import sys
import datetime
import argparse
import json

from campussquare.util import split_packed_code, get_school_year
from .errors import CampusSquareFlowError
from .campussquare import CampusSquare
from . import parser


class Authenticator():
    def login(self) -> CampusSquare:
        '''
        use refresh() instead on exception
        '''
        pass

    def refresh(self) -> CampusSquare:
        '''
        refresh on CampusSquareFlowError
        '''
        pass


def output(path: str, message: str):
    if path:
        with open(path, 'wt', encoding='utf-8') as f:
            f.write(message)
    else:
        print(message)


def _default_handler(args, next_handler, *, authenticator: Authenticator):
    try:
        campussquare = authenticator.login()
    except:
        campussquare = authenticator.refresh()

    for _ in range(3):
        try:
            next_handler(args, campussquare)
            break
        except CampusSquareFlowError:
            if 'n' == input('refresh (Y/n)'):
                break
            campussquare = authenticator.refresh()


def _syllabus_search_handler(args, campussquare: CampusSquare):
    campussquare.goto_syllabus_search()

    res = campussquare.search_syllabus(
        year=args.year,
        subject=args.subject,
        day_of_week=args.dayofweek,
        period=args.period)
    if args.html:
        output(args.output, res.text)
    elif args.json:
        results = parser.parse_syllabus_search_result(res.text)
        output(args.output, json.dumps(
            results, ensure_ascii=False, indent=4))
    else:
        results = parser.parse_syllabus_search_result(res.text)
        table = parser.format_syllabus_search_result(results)
        output(args.output, table)


def _syllabus_get_handler(args, campussquare: CampusSquare):
    codes_count = len(args.codes)
    for i, code in enumerate(args.codes):
        triple = split_packed_code(code)

        campussquare.goto_syllabus_search()
        res = campussquare.syllabus_detail(*triple)
        if args.html:
            output(args.output, res.text)
        elif args.markdown:
            results = parser.parse_syllabus_detail(res.text)
            md = parser.format_syllabus_detail_markdown(results)
            output(args.output, md)
        else:
            results = parser.parse_syllabus_detail(res.text)
            output(args.output, json.dumps(
                results, ensure_ascii=False, indent=4))

        if i + 1 < codes_count:
            # if not last
            time.sleep(args.interval)
            print(args.delimiter, end='')


def _grades_handler(args, campussquare: CampusSquare):
    campussquare.goto_grades()
    if args.command == 'get':
        res = campussquare.grades_detail(args.year, args.semester)
        if args.html:
            output(args.output, res.text)
        elif args.json:
            results = parser.parse_grades_detail(res.text)
            output(args.output, json.dumps(
                results, ensure_ascii=False, indent=4))
        elif args.markdown:
            raise RuntimeError('cannot format to markdown')
        else:
            results = parser.parse_grades_detail(res.text)
            table = parser.format_grades_detail(results)
            output(args.output, table)


def _courses_handler(args, campussquare: CampusSquare):
    res = campussquare.goto_courses()

    if args.semester is not None:
        res = campussquare.courses_semester(args.semester)

    if args.html:
        output(args.output, res.text)
    elif args.json:
        courses = parser.parse_courses(res.text)
        output(args.output, json.dumps(courses, ensure_ascii=False, indent=4))
    else:
        courses = parser.parse_courses(res.text)
        result = []
        for course in courses:
            result.append(
                f"{course['year']}:{course['affiliation']}:{course['code']}")
        output(args.output, '\n'.join(result))


def _toppage_handler(args, campussquare: CampusSquare):
    res = campussquare.goto_toppage()
    res.encoding = 'shift_jis'
    if args.html:
        output(args.output, res.text)
    else:
        doc = bs4.BeautifulSoup(res.text, 'html.parser')
        output(args.output, doc.text)


def get_parser(*, authenticator: Authenticator):
    parser = argparse.ArgumentParser('campussquare')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--html', action='store_true')
    parser.add_argument('--markdown', '--md', action='store_true')
    parser.add_argument('--output', '-o', default='')
    subparser = parser.add_subparsers()

    syllabus = subparser.add_parser('syllabus')
    syllabus_subparsers = syllabus.add_subparsers()

    syllabus_search = syllabus_subparsers.add_parser('search')
    syllabus_search.add_argument('--year', type=int,
                                 default=get_school_year())
    syllabus_search.add_argument('--subject', '-s')
    syllabus_search.add_argument('--semester', type=int, choices=[1, 2])
    syllabus_search.add_argument('--dayofweek', type=int)
    syllabus_search.add_argument('--period', type=int)
    syllabus_search.set_defaults(handler=lambda args: _default_handler(
        args,
        _syllabus_search_handler,
        authenticator=authenticator
    ))

    syllabus_get = syllabus_subparsers.add_parser('get')
    syllabus_get.add_argument('--delimiter', '-d', default='\x00')
    syllabus_get.add_argument(
        '--interval', '-i', type=int, default=3, help='取得間隔。秒')
    syllabus_get.add_argument(
        'codes', nargs='+', help='「年度:所属コード:時間割コード」のフォーマット。複数指定可')

    syllabus_get.set_defaults(handler=lambda args: _default_handler(
        args,
        _syllabus_get_handler,
        authenticator=authenticator
    ))

    grades = subparser.add_parser('grades')
    grades.add_argument('command', choices=['get'])
    grades.add_argument('--year', type=int)
    grades.add_argument('--semester', type=int, choices=[1, 2])
    grades.set_defaults(handler=lambda args: _default_handler(
        args,
        _grades_handler,
        authenticator=authenticator
    ))

    courses = subparser.add_parser('courses')
    courses.add_argument('--semester', type=int, choices=[1, 2])
    courses.set_defaults(handler=lambda args: _default_handler(
        args,
        _courses_handler,
        authenticator=authenticator
    ))

    toppage = subparser.add_parser('top')
    toppage.set_defaults(handler=lambda args: _default_handler(
        args,
        _toppage_handler,
        authenticator=authenticator,
    ))
    return parser


def parse_args_with_handler(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
