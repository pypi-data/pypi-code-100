# 重写rparserVisitor
from antlr4 import *
from xscanner.modules import Data
from xscanner.grammar.RuleLexer import RuleLexer
from xscanner.grammar.RuleParser import RuleParser

class Result:

    def __init__(self):
        self._name = '' # 规则名
        self._rid = '' # 规则ID = self.jls_extract_def()
        self._result = False # 表示是否命中
        self._detail = '' # 命中细节，哪个文件命中，哪个类命中。
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def rid(self):
        return self._rid
    
    @rid.setter
    def rid(self, value):
        self._rid = value

    @property
    def result(self):
        return self._result
    
    @result.setter
    def result(self, value):
        self._result = value

    @property
    def detail(self):
        return self._detail
    
    @detail.setter
    def detail(self, value):
        self._detail = value
    
    def __str__(self):
        return '{} {} {}'.format(self._name, self._rid, self._result)
    

class VisitorImp(ParseTreeVisitor):

    def __init__(self, data:Data):
        self.data = data

        self._results = {} # 存放结果 string:bool
        self._counter = {} # 存放计数器 string:int
        self._hits = 0 # 存放命中的数量
        self._total = 0 # 存放规则总数
        self._idents = [] # 存放变量名 _variables的key
        self._variables = {} # 存放变量的结果 string:bool

        self._is_skip = False # 类型不匹配，则跳过。

        self._results = []
        self._result = None
    
    def get_result(self):
        return self._results
    
    def has(self, name):
        return name in self._variables

    def get(self, name):
        return self._variables.get(name, None)
    
    def visit(self, ctx:RuleParser.RulesContext):
        ctx.accept(self)

    # Visit a parse tree produced by RuleParser#rules.
    def visitRules(self, ctx:RuleParser.RulesContext):
        self.visitChildren(ctx)

    # Visit a parse tree produced by RuleParser#ruleDec.
    def visitRuleDec(self, ctx:RuleParser.RuleDecContext):
        self._result = Result()
        self._hits = 0
        self._total = 0

        rid = ctx.DECIMAL_LIT()
        s = []
        for item in ctx.IDENTIFIER():
            s.append(item.getText())
        name = '.'.join(s)

        self._result.name = name
        self._result.rid = rid

        self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#typeExpression.
    def visitTypeExpression(self, ctx:RuleParser.TypeExpressionContext):
        t = 'any'
        if x := ctx.INTERPRETED_STRING_LIT():
            t = x.getText()[1:-1]

        if t == 'any':
            return

        self._is_skip = t != self.data.type


    def visitMainExpression(self, ctx:RuleParser.MainExpressionContext):
        if self._is_skip:
            return
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RuleParser#assignExpression.
    def visitAssignExpression(self, ctx:RuleParser.AssignExpressionContext):
        self._total += 1

        # print(ctx.NOCASE()) # nocase标志符，还可以用其他符号

        result = False
        if x := ctx.INTERPRETED_STRING_LIT():
            result = self.data.match(x.getText()[1:-1])
        elif x:=ctx.HEX_STRING_LIT():
            result = self.data.match_hex(x.getText()[1:-1])

        if result:
            self._hits += 1 # 命中

        ident = ctx.IDENTIFIER()
        if ident:
            self._idents.append(ident)
            self._variables[ident] = result

        return self.visitChildren(ctx)

    # Visit a parse tree produced by RuleParser#printExpression.
    def visitPrintExpression(self, ctx:RuleParser.PrintExpressionContext):
        print("visitPrintExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#arithmeticExpression.
    def visitArithmeticExpression(self, ctx:RuleParser.ArithmeticExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RuleParser#logicalExpression.
    def visitLogicalExpression(self, ctx:RuleParser.LogicalExpressionContext):
        if self._is_skip:
            return
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#ofExpression.
    def visitOfExpression(self, ctx:RuleParser.OfExpressionContext):
        hits = 0 # 命中数
        total = 0 # 总数

        if x := ctx.THEM():
            hits = self._hits
            total = self._total
        else:
            pass
        
        result = False
        if ctx.ANY():
            result = hits > 0
        elif ctx.ALL():
            result = hits == total
        else:
            # TODO 需要完善语法
            num = int(ctx.DECIMAL_LIT().getText())
            result = hits >= num
        
        self._result.result = result

        if result:
            self._results.append(self._result)

    # def visitExpression(self, ctx:RuleParser.ExpressionContext):
    #     return self.visitChildren(ctx)
