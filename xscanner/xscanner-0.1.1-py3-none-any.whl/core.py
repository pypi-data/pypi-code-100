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


class Scanner:
    def __init__(self, path):
        self.path = path  # 规则路径
        self._init_rules()

    def _init_rules(self):
        if not os.path.exists(self.path):
            return

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
        # print(type(self.rules))

    def scan(self, path):
        # TODO 文件类型检测，根据文件类型，初始化目标文件数据。
        # TODO 传入visitor，进行处理
        # TODO 规则可以指定类型，如果不指定，则默认扫描任意文件。
        kind = pyftype.guess(path)
        datas = []
        m_result = None
        s_result = []

        # 先扫描主包
        if kind.EXTENSION == 'zip':
            d = modules.zip.ZipData()
            d.from_path(path)
            m_result = self.scan_data(d)

            # TODO zip 中还有zip的情况呢？
            for data in d.get_datas():
                s_result.append(self.scan_data(data))
        else:
            d = anything.AnyData()
            d.from_path(path)
            m_result = self.scan_data(d)

        return m_result, s_result

    def scan_data(self, data):
        v = visitor.VisitorImp(data)
        v.visit(self.rules)

        return (data.path, v.get_result())

    def scan_mem(self, bytes):
        pass
