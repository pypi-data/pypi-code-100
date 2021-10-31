import http.cookiejar
from .session import CampusSquareSession


class CampusSquare():
    def __init__(self,
                 campussquare_url: str,
                 initial_flow_execution_key: str,
                 cookies: http.cookiejar.CookieJar,
                 credential_path: str = None,
                 debug: bool = False
                 ) -> None:
        self.campussquare_url = campussquare_url
        self.session = CampusSquareSession(campussquare_url,
                                           initial_flow_execution_key,
                                           cookies,
                                           credential_path=credential_path,
                                           debug=debug)

    def goto_toppage(self):
        url = f'{self.campussquare_url}?_flowId=USW0009500-flow'
        return self.session.do_get(url, namespace='toppage')

    def goto_syllabus_search(self):
        return self.session.do({
            '_flowId': 'SYW0001000-flow'
        })

    def search_syllabus(self,
                        year: int = '',
                        subject: str = '',
                        day_of_week: str = '',
                        period: str = '',
                        display_count: int = 100,
                        ):
        return self.session.do({
            's_no': '0',
            '_flowExecutionKey': self.session.get_flow_execution_key(),
            '_eventId': 'search',
            'nendo': year,
            'jikanwariShozokuCode': '',
            'gakkiKubunCode': '',
            'kyokannm': '',
            'kaikoKamokunm': subject,
            'numberingcd': '',
            'keyword': '',
            'nenji': '',
            'yobi': day_of_week,
            'jigen': period,
            'jitsumuKbn': '',
            '_displayCount': display_count,
        })

    def syllabus_detail(self,
                        year: int,
                        affiliation_code: int,
                        timetable_code: int,
                        locale: str = 'ja_JP'):
        return self.session.do({
            '_flowExecutionKey': self.session.get_flow_execution_key(),
            '_eventId': 'byCode',
            'nendo': year,
            'backTo': 'input',
            'jikanwariShozokuCodeForKettei': affiliation_code,
            'jikanwaricd': timetable_code,
        })

    def goto_grades(self):
        return self.session.do({
            '_flowId': 'SIW0001300-flow'
        })

    def grades_detail(self,
                      year: int = '',
                      semester: int = ''):
        return self.session.do({
            '_flowExecutionKey': self.session.get_flow_execution_key(),
            '_eventId': 'display',
            'dummy': '',
            'spanType': '1' if year and semester else '0',
            'nendo': year,
            'gakkiKbnCd': semester,
        })

    def goto_courses(self):
        return self.session.do({
            '_flowId': 'RSW0001000-flow'
        })

    def courses_semester(self, semester: int):
        return self.session.do({
            '_flowExecutionKey': self.session.get_flow_execution_key(),
            '_eventId': 'search',
            'gakkiKbnCode': semester,
        })
