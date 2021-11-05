from __future__ import absolute_import

import importlib
import os
import sys

import antlr4
import pyftype

from xscanner import modules
from xscanner.grammar import RuleLexer, RuleParser, visitor
from xscanner.modules import zip as zip_module


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
        self._init_modules()

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

    def _init_modules(self):
        self._modules = {}

        modules_path = os.path.join(os.path.dirname(__file__), "modules")
        for root, dirs, files in os.walk(modules_path):
            for f in files:
                if "__" in f:
                    continue
                if f.endswith(".pyc"):
                    continue

                name = os.path.basename(f[:-3])
                location = os.path.join(root, f)
                spec = importlib.util.spec_from_file_location(name, location)
                module = importlib.util.module_from_spec(spec)
                sys.modules[name] = module
                spec.loader.exec_module(module)

                for item in dir(module):
                    if item == "Data":
                        continue
                    t = getattr(module, item)
                    if isinstance(t, type):
                        self._modules[t()._mime] = t

    def scan(self, path):
        kind = pyftype.guess(path)

        scan_result = ScanResult()
        # 通过MIME自动调用指定模块进行扫描
        if kind.MIME in self._modules:
            d = self._modules[kind.MIME]()
            d.from_path(path)
            scan_result.path = path
            scan_result.main = self.scan_data(d)
            
            if hasattr(d, "get_datas"):
                for data in d.get_datas():
                    sr = ScanResult()
                    sr.path = data.path
                    sr.main = self.scan_data(data)
                    scan_result.add_sub(sr)
        else: # 其他情况，一律以any类型处理
            d = modules.Data()
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
