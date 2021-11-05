# Generated from anltr/RuleParser.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3D")
        buf.write("\u00ad\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\3\2\6\2\"\n\2\r\2\16\2#\3\3")
        buf.write("\3\3\5\3(\n\3\3\3\3\3\3\3\7\3-\n\3\f\3\16\3\60\13\3\3")
        buf.write("\3\3\3\3\4\3\4\3\4\5\4\67\n\4\3\4\5\4:\n\4\3\4\5\4=\n")
        buf.write("\4\5\4?\n\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3")
        buf.write("\6\3\7\3\7\3\7\3\7\3\b\3\b\3\b\6\bS\n\b\r\b\16\bT\3\b")
        buf.write("\3\b\3\b\3\t\3\t\3\t\5\t]\n\t\3\t\3\t\3\t\3\t\3\t\5\t")
        buf.write("d\n\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13")
        buf.write("\3\13\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3")
        buf.write("\r\3\r\5\r\177\n\r\3\r\3\r\3\r\3\r\3\r\3\r\7\r\u0087\n")
        buf.write("\r\f\r\16\r\u008a\13\r\3\16\3\16\3\17\3\17\3\17\3\17\3")
        buf.write("\17\5\17\u0093\n\17\3\20\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\20\3\20\5\20\u00a0\n\20\3\20\3\20\3\20\3")
        buf.write("\20\3\20\3\20\7\20\u00a8\n\20\f\20\16\20\u00ab\13\20\3")
        buf.write("\20\2\4\30\36\21\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36")
        buf.write("\2\6\4\2\60\6099\3\2\66\67\4\2\5\6<<\4\2))+.\2\u00b6\2")
        buf.write("!\3\2\2\2\4%\3\2\2\2\6\63\3\2\2\2\bC\3\2\2\2\nG\3\2\2")
        buf.write("\2\fK\3\2\2\2\16O\3\2\2\2\20\\\3\2\2\2\22e\3\2\2\2\24")
        buf.write("l\3\2\2\2\26s\3\2\2\2\30~\3\2\2\2\32\u008b\3\2\2\2\34")
        buf.write("\u008d\3\2\2\2\36\u009f\3\2\2\2 \"\5\4\3\2! \3\2\2\2\"")
        buf.write("#\3\2\2\2#!\3\2\2\2#$\3\2\2\2$\3\3\2\2\2%\'\7\3\2\2&(")
        buf.write("\7<\2\2\'&\3\2\2\2\'(\3\2\2\2()\3\2\2\2).\7\27\2\2*+\7")
        buf.write("\"\2\2+-\7\27\2\2,*\3\2\2\2-\60\3\2\2\2.,\3\2\2\2./\3")
        buf.write("\2\2\2/\61\3\2\2\2\60.\3\2\2\2\61\62\5\6\4\2\62\5\3\2")
        buf.write("\2\2\63>\7\32\2\2\64\66\7\13\2\2\65\67\5\b\5\2\66\65\3")
        buf.write("\2\2\2\66\67\3\2\2\2\679\3\2\2\28:\5\n\6\298\3\2\2\29")
        buf.write(":\3\2\2\2:<\3\2\2\2;=\5\f\7\2<;\3\2\2\2<=\3\2\2\2=?\3")
        buf.write("\2\2\2>\64\3\2\2\2>?\3\2\2\2?@\3\2\2\2@A\5\16\b\2AB\7")
        buf.write("\33\2\2B\7\3\2\2\2CD\7\f\2\2DE\7\36\2\2EF\7\24\2\2F\t")
        buf.write("\3\2\2\2GH\7\r\2\2HI\7\36\2\2IJ\7\24\2\2J\13\3\2\2\2K")
        buf.write("L\7\16\2\2LM\7\36\2\2MN\7\24\2\2N\r\3\2\2\2OR\7\17\2\2")
        buf.write("PS\5\20\t\2QS\5\26\f\2RP\3\2\2\2RQ\3\2\2\2ST\3\2\2\2T")
        buf.write("R\3\2\2\2TU\3\2\2\2UV\3\2\2\2VW\7\20\2\2WX\5\32\16\2X")
        buf.write("\17\3\2\2\2YZ\7\27\2\2Z]\7\36\2\2[]\3\2\2\2\\Y\3\2\2\2")
        buf.write("\\[\3\2\2\2]c\3\2\2\2^d\7\24\2\2_d\7\23\2\2`d\5\30\r\2")
        buf.write("ad\5\22\n\2bd\5\24\13\2c^\3\2\2\2c_\3\2\2\2c`\3\2\2\2")
        buf.write("ca\3\2\2\2cb\3\2\2\2d\21\3\2\2\2ef\7\21\2\2fg\7\30\2\2")
        buf.write("gh\7\24\2\2hi\7\37\2\2ij\7\24\2\2jk\7\31\2\2k\23\3\2\2")
        buf.write("\2lm\7\22\2\2mn\7\30\2\2no\7\24\2\2op\7\37\2\2pq\7\23")
        buf.write("\2\2qr\7\31\2\2r\25\3\2\2\2st\7\t\2\2tu\7\27\2\2u\27\3")
        buf.write("\2\2\2vw\b\r\1\2w\177\7<\2\2x\177\7?\2\2y\177\7\27\2\2")
        buf.write("z{\7\30\2\2{|\5\30\r\2|}\7\31\2\2}\177\3\2\2\2~v\3\2\2")
        buf.write("\2~x\3\2\2\2~y\3\2\2\2~z\3\2\2\2\177\u0088\3\2\2\2\u0080")
        buf.write("\u0081\f\b\2\2\u0081\u0082\t\2\2\2\u0082\u0087\5\30\r")
        buf.write("\t\u0083\u0084\f\7\2\2\u0084\u0085\t\3\2\2\u0085\u0087")
        buf.write("\5\30\r\b\u0086\u0080\3\2\2\2\u0086\u0083\3\2\2\2\u0087")
        buf.write("\u008a\3\2\2\2\u0088\u0086\3\2\2\2\u0088\u0089\3\2\2\2")
        buf.write("\u0089\31\3\2\2\2\u008a\u0088\3\2\2\2\u008b\u008c\5\36")
        buf.write("\20\2\u008c\33\3\2\2\2\u008d\u008e\t\4\2\2\u008e\u0092")
        buf.write("\7\7\2\2\u008f\u0090\7\27\2\2\u0090\u0093\7\n\2\2\u0091")
        buf.write("\u0093\7\b\2\2\u0092\u008f\3\2\2\2\u0092\u0091\3\2\2\2")
        buf.write("\u0093\35\3\2\2\2\u0094\u0095\b\20\1\2\u0095\u00a0\7\27")
        buf.write("\2\2\u0096\u00a0\5\34\17\2\u0097\u0098\5\30\r\2\u0098")
        buf.write("\u0099\t\5\2\2\u0099\u009a\5\30\r\2\u009a\u00a0\3\2\2")
        buf.write("\2\u009b\u009c\7\30\2\2\u009c\u009d\5\36\20\2\u009d\u009e")
        buf.write("\7\31\2\2\u009e\u00a0\3\2\2\2\u009f\u0094\3\2\2\2\u009f")
        buf.write("\u0096\3\2\2\2\u009f\u0097\3\2\2\2\u009f\u009b\3\2\2\2")
        buf.write("\u00a0\u00a9\3\2\2\2\u00a1\u00a2\f\4\2\2\u00a2\u00a3\7")
        buf.write("(\2\2\u00a3\u00a8\5\36\20\5\u00a4\u00a5\f\3\2\2\u00a5")
        buf.write("\u00a6\7\'\2\2\u00a6\u00a8\5\36\20\4\u00a7\u00a1\3\2\2")
        buf.write("\2\u00a7\u00a4\3\2\2\2\u00a8\u00ab\3\2\2\2\u00a9\u00a7")
        buf.write("\3\2\2\2\u00a9\u00aa\3\2\2\2\u00aa\37\3\2\2\2\u00ab\u00a9")
        buf.write("\3\2\2\2\24#\'.\669<>RT\\c~\u0086\u0088\u0092\u009f\u00a7")
        buf.write("\u00a9")
        return buf.getvalue()


class RuleParser ( Parser ):

    grammarFileName = "RuleParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'rule'", "'raw'", "'any'", "'all'", "'of'", 
                     "'them'", "'print'", "'$'", "'meta:'", "'type'", "'url'", 
                     "'description'", "'strings:'", "'condition:'", "'zip.file'", 
                     "'zip.file_hex'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'nocase'", "<INVALID>", "'('", "')'", "'{'", "'}'", 
                     "'['", "']'", "'='", "','", "';'", "':'", "'.'", "'++'", 
                     "'--'", "':='", "'...'", "'||'", "'&&'", "'=='", "'!='", 
                     "'<'", "'<='", "'>'", "'>='", "'|'", "'/'", "'%'", 
                     "'<<'", "'>>'", "'&^'", "'!'", "'+'", "'-'", "'^'", 
                     "'*'", "'&'", "'<-'" ]

    symbolicNames = [ "<INVALID>", "RULE", "RAW", "ANY", "ALL", "OF", "THEM", 
                      "PRINT", "DOLLAR", "META", "TYPE", "URL", "DESCRIPTION", 
                      "STRINGS", "CONDITION", "ZIP_FILE", "ZIP_FILE_HEX", 
                      "HEX_STRING_LIT", "INTERPRETED_STRING_LIT", "REGEXP", 
                      "NOCASE", "IDENTIFIER", "L_PAREN", "R_PAREN", "L_CURLY", 
                      "R_CURLY", "L_BRACKET", "R_BRACKET", "ASSIGN", "COMMA", 
                      "SEMI", "COLON", "DOT", "PLUS_PLUS", "MINUS_MINUS", 
                      "DECLARE_ASSIGN", "ELLIPSIS", "LOGICAL_OR", "LOGICAL_AND", 
                      "EQUALS", "NOT_EQUALS", "LESS", "LESS_OR_EQUALS", 
                      "GREATER", "GREATER_OR_EQUALS", "OR_OP", "DIV", "MOD", 
                      "LSHIFT", "RSHIFT", "BIT_CLEAR", "EXCLAMATION", "PLUS", 
                      "MINUS", "CARET", "STAR", "AMPERSAND", "RECEIVE", 
                      "DECIMAL_LIT", "OCTAL_LIT", "HEX_LIT", "FLOAT_LIT", 
                      "IMAGINARY_LIT", "WS", "COMMENT", "TERMINATOR", "LINE_COMMENT" ]

    RULE_rules = 0
    RULE_ruleDec = 1
    RULE_body = 2
    RULE_typeExpression = 3
    RULE_urlExpression = 4
    RULE_descExpression = 5
    RULE_mainExpression = 6
    RULE_assignExpression = 7
    RULE_zipExpression = 8
    RULE_zipHexExpression = 9
    RULE_printExpression = 10
    RULE_arithmeticExpression = 11
    RULE_logicalExpression = 12
    RULE_ofExpression = 13
    RULE_expression = 14

    ruleNames =  [ "rules", "ruleDec", "body", "typeExpression", "urlExpression", 
                   "descExpression", "mainExpression", "assignExpression", 
                   "zipExpression", "zipHexExpression", "printExpression", 
                   "arithmeticExpression", "logicalExpression", "ofExpression", 
                   "expression" ]

    EOF = Token.EOF
    RULE=1
    RAW=2
    ANY=3
    ALL=4
    OF=5
    THEM=6
    PRINT=7
    DOLLAR=8
    META=9
    TYPE=10
    URL=11
    DESCRIPTION=12
    STRINGS=13
    CONDITION=14
    ZIP_FILE=15
    ZIP_FILE_HEX=16
    HEX_STRING_LIT=17
    INTERPRETED_STRING_LIT=18
    REGEXP=19
    NOCASE=20
    IDENTIFIER=21
    L_PAREN=22
    R_PAREN=23
    L_CURLY=24
    R_CURLY=25
    L_BRACKET=26
    R_BRACKET=27
    ASSIGN=28
    COMMA=29
    SEMI=30
    COLON=31
    DOT=32
    PLUS_PLUS=33
    MINUS_MINUS=34
    DECLARE_ASSIGN=35
    ELLIPSIS=36
    LOGICAL_OR=37
    LOGICAL_AND=38
    EQUALS=39
    NOT_EQUALS=40
    LESS=41
    LESS_OR_EQUALS=42
    GREATER=43
    GREATER_OR_EQUALS=44
    OR_OP=45
    DIV=46
    MOD=47
    LSHIFT=48
    RSHIFT=49
    BIT_CLEAR=50
    EXCLAMATION=51
    PLUS=52
    MINUS=53
    CARET=54
    STAR=55
    AMPERSAND=56
    RECEIVE=57
    DECIMAL_LIT=58
    OCTAL_LIT=59
    HEX_LIT=60
    FLOAT_LIT=61
    IMAGINARY_LIT=62
    WS=63
    COMMENT=64
    TERMINATOR=65
    LINE_COMMENT=66

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RulesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ruleDec(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RuleParser.RuleDecContext)
            else:
                return self.getTypedRuleContext(RuleParser.RuleDecContext,i)


        def getRuleIndex(self):
            return RuleParser.RULE_rules

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRules" ):
                return visitor.visitRules(self)
            else:
                return visitor.visitChildren(self)




    def rules(self):

        localctx = RuleParser.RulesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_rules)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 30
                self.ruleDec()
                self.state = 33 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==RuleParser.RULE):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleDecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RULE(self):
            return self.getToken(RuleParser.RULE, 0)

        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(RuleParser.IDENTIFIER)
            else:
                return self.getToken(RuleParser.IDENTIFIER, i)

        def body(self):
            return self.getTypedRuleContext(RuleParser.BodyContext,0)


        def DECIMAL_LIT(self):
            return self.getToken(RuleParser.DECIMAL_LIT, 0)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(RuleParser.DOT)
            else:
                return self.getToken(RuleParser.DOT, i)

        def getRuleIndex(self):
            return RuleParser.RULE_ruleDec

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleDec" ):
                return visitor.visitRuleDec(self)
            else:
                return visitor.visitChildren(self)




    def ruleDec(self):

        localctx = RuleParser.RuleDecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_ruleDec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(RuleParser.RULE)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==RuleParser.DECIMAL_LIT:
                self.state = 36
                self.match(RuleParser.DECIMAL_LIT)


            self.state = 39
            self.match(RuleParser.IDENTIFIER)
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==RuleParser.DOT:
                self.state = 40
                self.match(RuleParser.DOT)
                self.state = 41
                self.match(RuleParser.IDENTIFIER)
                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 47
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_CURLY(self):
            return self.getToken(RuleParser.L_CURLY, 0)

        def mainExpression(self):
            return self.getTypedRuleContext(RuleParser.MainExpressionContext,0)


        def R_CURLY(self):
            return self.getToken(RuleParser.R_CURLY, 0)

        def META(self):
            return self.getToken(RuleParser.META, 0)

        def typeExpression(self):
            return self.getTypedRuleContext(RuleParser.TypeExpressionContext,0)


        def urlExpression(self):
            return self.getTypedRuleContext(RuleParser.UrlExpressionContext,0)


        def descExpression(self):
            return self.getTypedRuleContext(RuleParser.DescExpressionContext,0)


        def getRuleIndex(self):
            return RuleParser.RULE_body

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = RuleParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(RuleParser.L_CURLY)
            self.state = 60
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==RuleParser.META:
                self.state = 50
                self.match(RuleParser.META)
                self.state = 52
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==RuleParser.TYPE:
                    self.state = 51
                    self.typeExpression()


                self.state = 55
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==RuleParser.URL:
                    self.state = 54
                    self.urlExpression()


                self.state = 58
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==RuleParser.DESCRIPTION:
                    self.state = 57
                    self.descExpression()




            self.state = 62
            self.mainExpression()
            self.state = 63
            self.match(RuleParser.R_CURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TYPE(self):
            return self.getToken(RuleParser.TYPE, 0)

        def ASSIGN(self):
            return self.getToken(RuleParser.ASSIGN, 0)

        def INTERPRETED_STRING_LIT(self):
            return self.getToken(RuleParser.INTERPRETED_STRING_LIT, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_typeExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeExpression" ):
                return visitor.visitTypeExpression(self)
            else:
                return visitor.visitChildren(self)




    def typeExpression(self):

        localctx = RuleParser.TypeExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_typeExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self.match(RuleParser.TYPE)
            self.state = 66
            self.match(RuleParser.ASSIGN)
            self.state = 67
            self.match(RuleParser.INTERPRETED_STRING_LIT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UrlExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def URL(self):
            return self.getToken(RuleParser.URL, 0)

        def ASSIGN(self):
            return self.getToken(RuleParser.ASSIGN, 0)

        def INTERPRETED_STRING_LIT(self):
            return self.getToken(RuleParser.INTERPRETED_STRING_LIT, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_urlExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUrlExpression" ):
                return visitor.visitUrlExpression(self)
            else:
                return visitor.visitChildren(self)




    def urlExpression(self):

        localctx = RuleParser.UrlExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_urlExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(RuleParser.URL)
            self.state = 70
            self.match(RuleParser.ASSIGN)
            self.state = 71
            self.match(RuleParser.INTERPRETED_STRING_LIT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DescExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DESCRIPTION(self):
            return self.getToken(RuleParser.DESCRIPTION, 0)

        def ASSIGN(self):
            return self.getToken(RuleParser.ASSIGN, 0)

        def INTERPRETED_STRING_LIT(self):
            return self.getToken(RuleParser.INTERPRETED_STRING_LIT, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_descExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDescExpression" ):
                return visitor.visitDescExpression(self)
            else:
                return visitor.visitChildren(self)




    def descExpression(self):

        localctx = RuleParser.DescExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_descExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(RuleParser.DESCRIPTION)
            self.state = 74
            self.match(RuleParser.ASSIGN)
            self.state = 75
            self.match(RuleParser.INTERPRETED_STRING_LIT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MainExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRINGS(self):
            return self.getToken(RuleParser.STRINGS, 0)

        def CONDITION(self):
            return self.getToken(RuleParser.CONDITION, 0)

        def logicalExpression(self):
            return self.getTypedRuleContext(RuleParser.LogicalExpressionContext,0)


        def assignExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RuleParser.AssignExpressionContext)
            else:
                return self.getTypedRuleContext(RuleParser.AssignExpressionContext,i)


        def printExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RuleParser.PrintExpressionContext)
            else:
                return self.getTypedRuleContext(RuleParser.PrintExpressionContext,i)


        def getRuleIndex(self):
            return RuleParser.RULE_mainExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMainExpression" ):
                return visitor.visitMainExpression(self)
            else:
                return visitor.visitChildren(self)




    def mainExpression(self):

        localctx = RuleParser.MainExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_mainExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(RuleParser.STRINGS)
            self.state = 80 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 80
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [RuleParser.ZIP_FILE, RuleParser.ZIP_FILE_HEX, RuleParser.HEX_STRING_LIT, RuleParser.INTERPRETED_STRING_LIT, RuleParser.IDENTIFIER, RuleParser.L_PAREN, RuleParser.DECIMAL_LIT, RuleParser.FLOAT_LIT]:
                    self.state = 78
                    self.assignExpression()
                    pass
                elif token in [RuleParser.PRINT]:
                    self.state = 79
                    self.printExpression()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 82 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << RuleParser.PRINT) | (1 << RuleParser.ZIP_FILE) | (1 << RuleParser.ZIP_FILE_HEX) | (1 << RuleParser.HEX_STRING_LIT) | (1 << RuleParser.INTERPRETED_STRING_LIT) | (1 << RuleParser.IDENTIFIER) | (1 << RuleParser.L_PAREN) | (1 << RuleParser.DECIMAL_LIT) | (1 << RuleParser.FLOAT_LIT))) != 0)):
                    break

            self.state = 84
            self.match(RuleParser.CONDITION)
            self.state = 85
            self.logicalExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(RuleParser.IDENTIFIER, 0)

        def ASSIGN(self):
            return self.getToken(RuleParser.ASSIGN, 0)

        def INTERPRETED_STRING_LIT(self):
            return self.getToken(RuleParser.INTERPRETED_STRING_LIT, 0)

        def HEX_STRING_LIT(self):
            return self.getToken(RuleParser.HEX_STRING_LIT, 0)

        def arithmeticExpression(self):
            return self.getTypedRuleContext(RuleParser.ArithmeticExpressionContext,0)


        def zipExpression(self):
            return self.getTypedRuleContext(RuleParser.ZipExpressionContext,0)


        def zipHexExpression(self):
            return self.getTypedRuleContext(RuleParser.ZipHexExpressionContext,0)


        def getRuleIndex(self):
            return RuleParser.RULE_assignExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignExpression" ):
                return visitor.visitAssignExpression(self)
            else:
                return visitor.visitChildren(self)




    def assignExpression(self):

        localctx = RuleParser.AssignExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_assignExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 87
                self.match(RuleParser.IDENTIFIER)
                self.state = 88
                self.match(RuleParser.ASSIGN)
                pass

            elif la_ == 2:
                pass


            self.state = 97
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RuleParser.INTERPRETED_STRING_LIT]:
                self.state = 92
                self.match(RuleParser.INTERPRETED_STRING_LIT)
                pass
            elif token in [RuleParser.HEX_STRING_LIT]:
                self.state = 93
                self.match(RuleParser.HEX_STRING_LIT)
                pass
            elif token in [RuleParser.IDENTIFIER, RuleParser.L_PAREN, RuleParser.DECIMAL_LIT, RuleParser.FLOAT_LIT]:
                self.state = 94
                self.arithmeticExpression(0)
                pass
            elif token in [RuleParser.ZIP_FILE]:
                self.state = 95
                self.zipExpression()
                pass
            elif token in [RuleParser.ZIP_FILE_HEX]:
                self.state = 96
                self.zipHexExpression()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ZipExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ZIP_FILE(self):
            return self.getToken(RuleParser.ZIP_FILE, 0)

        def L_PAREN(self):
            return self.getToken(RuleParser.L_PAREN, 0)

        def INTERPRETED_STRING_LIT(self, i:int=None):
            if i is None:
                return self.getTokens(RuleParser.INTERPRETED_STRING_LIT)
            else:
                return self.getToken(RuleParser.INTERPRETED_STRING_LIT, i)

        def COMMA(self):
            return self.getToken(RuleParser.COMMA, 0)

        def R_PAREN(self):
            return self.getToken(RuleParser.R_PAREN, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_zipExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitZipExpression" ):
                return visitor.visitZipExpression(self)
            else:
                return visitor.visitChildren(self)




    def zipExpression(self):

        localctx = RuleParser.ZipExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_zipExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(RuleParser.ZIP_FILE)
            self.state = 100
            self.match(RuleParser.L_PAREN)
            self.state = 101
            self.match(RuleParser.INTERPRETED_STRING_LIT)
            self.state = 102
            self.match(RuleParser.COMMA)
            self.state = 103
            self.match(RuleParser.INTERPRETED_STRING_LIT)
            self.state = 104
            self.match(RuleParser.R_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ZipHexExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ZIP_FILE_HEX(self):
            return self.getToken(RuleParser.ZIP_FILE_HEX, 0)

        def L_PAREN(self):
            return self.getToken(RuleParser.L_PAREN, 0)

        def INTERPRETED_STRING_LIT(self):
            return self.getToken(RuleParser.INTERPRETED_STRING_LIT, 0)

        def COMMA(self):
            return self.getToken(RuleParser.COMMA, 0)

        def HEX_STRING_LIT(self):
            return self.getToken(RuleParser.HEX_STRING_LIT, 0)

        def R_PAREN(self):
            return self.getToken(RuleParser.R_PAREN, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_zipHexExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitZipHexExpression" ):
                return visitor.visitZipHexExpression(self)
            else:
                return visitor.visitChildren(self)




    def zipHexExpression(self):

        localctx = RuleParser.ZipHexExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_zipHexExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            self.match(RuleParser.ZIP_FILE_HEX)
            self.state = 107
            self.match(RuleParser.L_PAREN)
            self.state = 108
            self.match(RuleParser.INTERPRETED_STRING_LIT)
            self.state = 109
            self.match(RuleParser.COMMA)
            self.state = 110
            self.match(RuleParser.HEX_STRING_LIT)
            self.state = 111
            self.match(RuleParser.R_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINT(self):
            return self.getToken(RuleParser.PRINT, 0)

        def IDENTIFIER(self):
            return self.getToken(RuleParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_printExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintExpression" ):
                return visitor.visitPrintExpression(self)
            else:
                return visitor.visitChildren(self)




    def printExpression(self):

        localctx = RuleParser.PrintExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_printExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(RuleParser.PRINT)
            self.state = 114
            self.match(RuleParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL_LIT(self):
            return self.getToken(RuleParser.DECIMAL_LIT, 0)

        def FLOAT_LIT(self):
            return self.getToken(RuleParser.FLOAT_LIT, 0)

        def IDENTIFIER(self):
            return self.getToken(RuleParser.IDENTIFIER, 0)

        def L_PAREN(self):
            return self.getToken(RuleParser.L_PAREN, 0)

        def arithmeticExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RuleParser.ArithmeticExpressionContext)
            else:
                return self.getTypedRuleContext(RuleParser.ArithmeticExpressionContext,i)


        def R_PAREN(self):
            return self.getToken(RuleParser.R_PAREN, 0)

        def STAR(self):
            return self.getToken(RuleParser.STAR, 0)

        def DIV(self):
            return self.getToken(RuleParser.DIV, 0)

        def PLUS(self):
            return self.getToken(RuleParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(RuleParser.MINUS, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_arithmeticExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArithmeticExpression" ):
                return visitor.visitArithmeticExpression(self)
            else:
                return visitor.visitChildren(self)



    def arithmeticExpression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RuleParser.ArithmeticExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_arithmeticExpression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RuleParser.DECIMAL_LIT]:
                self.state = 117
                self.match(RuleParser.DECIMAL_LIT)
                pass
            elif token in [RuleParser.FLOAT_LIT]:
                self.state = 118
                self.match(RuleParser.FLOAT_LIT)
                pass
            elif token in [RuleParser.IDENTIFIER]:
                self.state = 119
                self.match(RuleParser.IDENTIFIER)
                pass
            elif token in [RuleParser.L_PAREN]:
                self.state = 120
                self.match(RuleParser.L_PAREN)
                self.state = 121
                self.arithmeticExpression(0)
                self.state = 122
                self.match(RuleParser.R_PAREN)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 134
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,13,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 132
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
                    if la_ == 1:
                        localctx = RuleParser.ArithmeticExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_arithmeticExpression)
                        self.state = 126
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 127
                        _la = self._input.LA(1)
                        if not(_la==RuleParser.DIV or _la==RuleParser.STAR):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 128
                        self.arithmeticExpression(7)
                        pass

                    elif la_ == 2:
                        localctx = RuleParser.ArithmeticExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_arithmeticExpression)
                        self.state = 129
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 130
                        _la = self._input.LA(1)
                        if not(_la==RuleParser.PLUS or _la==RuleParser.MINUS):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 131
                        self.arithmeticExpression(6)
                        pass

             
                self.state = 136
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,13,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class LogicalExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(RuleParser.ExpressionContext,0)


        def getRuleIndex(self):
            return RuleParser.RULE_logicalExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalExpression" ):
                return visitor.visitLogicalExpression(self)
            else:
                return visitor.visitChildren(self)




    def logicalExpression(self):

        localctx = RuleParser.LogicalExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_logicalExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OfExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OF(self):
            return self.getToken(RuleParser.OF, 0)

        def ANY(self):
            return self.getToken(RuleParser.ANY, 0)

        def ALL(self):
            return self.getToken(RuleParser.ALL, 0)

        def DECIMAL_LIT(self):
            return self.getToken(RuleParser.DECIMAL_LIT, 0)

        def IDENTIFIER(self):
            return self.getToken(RuleParser.IDENTIFIER, 0)

        def DOLLAR(self):
            return self.getToken(RuleParser.DOLLAR, 0)

        def THEM(self):
            return self.getToken(RuleParser.THEM, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_ofExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOfExpression" ):
                return visitor.visitOfExpression(self)
            else:
                return visitor.visitChildren(self)




    def ofExpression(self):

        localctx = RuleParser.OfExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_ofExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << RuleParser.ANY) | (1 << RuleParser.ALL) | (1 << RuleParser.DECIMAL_LIT))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 140
            self.match(RuleParser.OF)
            self.state = 144
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RuleParser.IDENTIFIER]:
                self.state = 141
                self.match(RuleParser.IDENTIFIER)
                self.state = 142
                self.match(RuleParser.DOLLAR)
                pass
            elif token in [RuleParser.THEM]:
                self.state = 143
                self.match(RuleParser.THEM)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(RuleParser.IDENTIFIER, 0)

        def ofExpression(self):
            return self.getTypedRuleContext(RuleParser.OfExpressionContext,0)


        def arithmeticExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RuleParser.ArithmeticExpressionContext)
            else:
                return self.getTypedRuleContext(RuleParser.ArithmeticExpressionContext,i)


        def GREATER(self):
            return self.getToken(RuleParser.GREATER, 0)

        def GREATER_OR_EQUALS(self):
            return self.getToken(RuleParser.GREATER_OR_EQUALS, 0)

        def EQUALS(self):
            return self.getToken(RuleParser.EQUALS, 0)

        def LESS(self):
            return self.getToken(RuleParser.LESS, 0)

        def LESS_OR_EQUALS(self):
            return self.getToken(RuleParser.LESS_OR_EQUALS, 0)

        def L_PAREN(self):
            return self.getToken(RuleParser.L_PAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RuleParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RuleParser.ExpressionContext,i)


        def R_PAREN(self):
            return self.getToken(RuleParser.R_PAREN, 0)

        def LOGICAL_AND(self):
            return self.getToken(RuleParser.LOGICAL_AND, 0)

        def LOGICAL_OR(self):
            return self.getToken(RuleParser.LOGICAL_OR, 0)

        def getRuleIndex(self):
            return RuleParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RuleParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 28
        self.enterRecursionRule(localctx, 28, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 157
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.state = 147
                self.match(RuleParser.IDENTIFIER)
                pass

            elif la_ == 2:
                self.state = 148
                self.ofExpression()
                pass

            elif la_ == 3:
                self.state = 149
                self.arithmeticExpression(0)
                self.state = 150
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << RuleParser.EQUALS) | (1 << RuleParser.LESS) | (1 << RuleParser.LESS_OR_EQUALS) | (1 << RuleParser.GREATER) | (1 << RuleParser.GREATER_OR_EQUALS))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 151
                self.arithmeticExpression(0)
                pass

            elif la_ == 4:
                self.state = 153
                self.match(RuleParser.L_PAREN)
                self.state = 154
                self.expression(0)
                self.state = 155
                self.match(RuleParser.R_PAREN)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 167
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 165
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
                    if la_ == 1:
                        localctx = RuleParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 159
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 160
                        self.match(RuleParser.LOGICAL_AND)
                        self.state = 161
                        self.expression(3)
                        pass

                    elif la_ == 2:
                        localctx = RuleParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 162
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 163
                        self.match(RuleParser.LOGICAL_OR)
                        self.state = 164
                        self.expression(2)
                        pass

             
                self.state = 169
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[11] = self.arithmeticExpression_sempred
        self._predicates[14] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def arithmeticExpression_sempred(self, localctx:ArithmeticExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 1)
         




