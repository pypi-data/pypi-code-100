from __future__ import absolute_import

import os

import antlr4
import pyftype

from xscanner import modules
from xscanner.grammar import RuleLexer, RuleParser, visitor
from xscanner.modules import anything, zip


def get_file_object(path):
    # TODO 类型检测
    # 根据类型，初始化文件数据
    # 返回数据对象
    return modules.anything.Anything(path)


class ScanResult(object):
    def __init__(self):
        self.__names = []
        self.__main_result = None
        self.__path = None
        self.__sub_results = []

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def main(self):
        return self.__main_result

    @main.setter
    def main(self, value: visitor.Result):
        self.__main_result = value

        for item in self.__main_result:
            self.__names.append(item.name)

    @property
    def names(self):
        return self.__names

    @property
    def subs(self):
        return self.__sub_results

    def add_sub(self, result):
        self.__sub_results.append(result)


class Scanner:
    def __init__(self, path):
        self.path = path  # 规则路径
        self._init_rules()

    def _init_rules(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError()

        # TODO 全部读取出来，组合成一个大的字符串
        content = ""
        if os.path.isdir(self.path):
            for path in os.listdir(self.path):
                print(path)
        else:
            with open(self.path) as f:
                content = f.read()

        lex = RuleLexer.RuleLexer(antlr4.InputStream(content))
        parser = RuleParser.RuleParser(antlr4.CommonTokenStream(lex))

        # TODO parser.removeErrorListeners()

        self.rules = parser.rules()

    def scan(self, path):
        # TODO 文件类型检测，根据文件类型，初始化目标文件数据。
        # TODO 传入visitor，进行处理
        # TODO 规则可以指定类型，如果不指定，则默认扫描任意文件。
        kind = pyftype.guess(path)
        datas = []
        # m_result = None
        # s_result = []

        # 先扫描主包

        scan_result = ScanResult()

        if kind.EXTENSION == "zip":
            d = modules.zip.ZipData()
            d.from_path(path)

            scan_result.path = path
            scan_result.main = self.scan_data(d)

            # TODO zip 中还有zip的情况呢？
            for data in d.get_datas():
                sr = ScanResult()
                sr.path = data.path
                sr.main = self.scan_data(data)
                scan_result.add_sub(sr)
        else:
            d = anything.AnyData()
            d.from_path(path)
            scan_result.path = path
            scan_result.main = self.scan_data(d)

        return scan_result

    def scan_data(self, data):
        v = visitor.VisitorImp(data)
        v.visit(self.rules)

        return v.get_result()

    def scan_mem(self, bytes):
        pass
