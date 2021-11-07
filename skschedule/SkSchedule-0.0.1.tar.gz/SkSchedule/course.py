# coding: utf-8
import requests
import time
import pandas as pd
import json


class Course:

    session = requests.Session()
    headers = {
        "Host": "aic.hbswkj.com:8080",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
    }

    def __init__(self, username: str, password: str, weeks: int = 2):

        self.session.headers.update(self.headers)
        self.session.get("http://aic.hbswkj.com:8080/jedu/")

        res = self.session.post(
            "http://aic.hbswkj.com:8080/jedu/login.do",
            {"username": username, "password": password},
        ).json()

        if res["success"]:
            self.session.cookies.set("username", username)
            time.sleep(0.2)
            self.session.get("http://aic.hbswkj.com:8080/jedu/index.do")
        else:
            raise ValueError("请检查账号和密码!")

        self.__get_all(weeks)

    def print_time(f):
        def _(self, *args, **kwargs):
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print("current time：" + now_time)
            f(self, *args, **kwargs)
            return None

        return _

    @print_time
    def __get_all(self, weeks: int = 2) -> None:
        url = "http://aic.hbswkj.com:8080/jedu/edu/core/eduScheduleInfo/getStudentWeekSchedule.do?week=%s&semId="
        res = self.session.get(url % (weeks))
        df = pd.read_json(json.dumps(res.json()["data"]["schedule"]))

        if df.empty:
            raise Exception("查询无数据,请检查week参数。")

        drop_items = [
            "createTime",
            "updateTime",
            "createBy",
            "updateBy",
            "tenantId",
            "scheInfoId",
            "teacherId",
            "tclassId",
            "courseId",
            "taskId",
            "placeId",
            "semId",
            "lessonId",
            "isScheAuto",
            "schoolZoneId",
            "status",
            "detailType",
            "checkStatus",
            "whetherMain",
            "arrangeType",
            "remarks",
            "whetherTeacherLog",
            "practiceFlag",
            "createType",
            "isNormal",
            "exceMsg",
            "appId",
            "eduTimeSchedule",
            "oldTeacherId",
            "identifyLabel",
            "pkId",
            "week",
        ]

        self.__data = df.drop(drop_items, axis=1)

        self.__data.columns = ["教师", "班级名称", "课程名称", "时间", "星期", "地点"]

        self.__data["星期"] = self.__data["星期"].map(
            {
                "mon": "周一",
                "tue": "周二",
                "wed": "周三",
                "thu": "周四",
                "fri": "周五",
                "sat": "周六",
                "sun": "周天",
            }
        )

        return self


    def query(self, week="周一", teacher: str = None):

        if isinstance(week, str) and isinstance(teacher, str):
            data = self.__data[
                (self.__data["星期"] == week) & ((self.__data["教师"] == teacher))
            ]
            if not data.empty:
                return data
            else:
                return "查询无结果"

        elif isinstance(week, str):
            data = self.__data[self.__data["星期"] == week]
            if not data.empty:
                return data
            else:
                return "查询无结果"

        elif isinstance(week, list):
            data = self.__data[self.__data["星期"].isin(week)]
            if not data.empty:
                return data
            else:
                return "查询无结果"
        else:
            raise ValueError("参数错误,请检查。")

    def fetch(self):
        return self.__data

    def to_excel(self, path):
        self.__data.to_excel(path, index=False)

if __name__=="__main__":
    print(Course("2002060242", "2002060242a",8).query('周三'))
