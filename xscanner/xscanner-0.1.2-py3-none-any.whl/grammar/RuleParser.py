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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3B")
        buf.write("\u00a0\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\3\2\6\2\36\n\2\r\2\16\2\37\3\3\3\3\5\3$\n\3\3\3")
        buf.write("\3\3\3\3\7\3)\n\3\f\3\16\3,\13\3\3\3\3\3\3\4\3\4\3\4\5")
        buf.write("\4\63\n\4\3\4\5\4\66\n\4\3\4\5\49\n\4\5\4;\n\4\3\4\3\4")
        buf.write("\3\4\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3")
        buf.write("\b\3\b\6\bN\n\b\r\b\16\bO\3\b\3\b\3\b\3\t\3\t\3\t\5\t")
        buf.write("X\n\t\3\t\3\t\5\t\\\n\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\5")
        buf.write("\te\n\t\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\13")
        buf.write("\3\13\5\13r\n\13\3\13\3\13\3\13\3\13\3\13\3\13\7\13z\n")
        buf.write("\13\f\13\16\13}\13\13\3\f\3\f\3\r\3\r\3\r\3\r\3\r\5\r")
        buf.write("\u0086\n\r\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16")
        buf.write("\3\16\3\16\5\16\u0093\n\16\3\16\3\16\3\16\3\16\3\16\3")
        buf.write("\16\7\16\u009b\n\16\f\16\16\16\u009e\13\16\3\16\2\4\24")
        buf.write("\32\17\2\4\6\b\n\f\16\20\22\24\26\30\32\2\6\4\2..\67\67")
        buf.write("\3\2\64\65\4\2\5\6::\4\2\'\'),\2\u00aa\2\35\3\2\2\2\4")
        buf.write("!\3\2\2\2\6/\3\2\2\2\b?\3\2\2\2\nC\3\2\2\2\fG\3\2\2\2")
        buf.write("\16K\3\2\2\2\20d\3\2\2\2\22f\3\2\2\2\24q\3\2\2\2\26~\3")
        buf.write("\2\2\2\30\u0080\3\2\2\2\32\u0092\3\2\2\2\34\36\5\4\3\2")
        buf.write("\35\34\3\2\2\2\36\37\3\2\2\2\37\35\3\2\2\2\37 \3\2\2\2")
        buf.write(" \3\3\2\2\2!#\7\3\2\2\"$\7:\2\2#\"\3\2\2\2#$\3\2\2\2$")
        buf.write("%\3\2\2\2%*\7\25\2\2&\'\7 \2\2\')\7\25\2\2(&\3\2\2\2)")
        buf.write(",\3\2\2\2*(\3\2\2\2*+\3\2\2\2+-\3\2\2\2,*\3\2\2\2-.\5")
        buf.write("\6\4\2.\5\3\2\2\2/:\7\30\2\2\60\62\7\13\2\2\61\63\5\b")
        buf.write("\5\2\62\61\3\2\2\2\62\63\3\2\2\2\63\65\3\2\2\2\64\66\5")
        buf.write("\n\6\2\65\64\3\2\2\2\65\66\3\2\2\2\668\3\2\2\2\679\5\f")
        buf.write("\7\28\67\3\2\2\289\3\2\2\29;\3\2\2\2:\60\3\2\2\2:;\3\2")
        buf.write("\2\2;<\3\2\2\2<=\5\16\b\2=>\7\31\2\2>\7\3\2\2\2?@\7\f")
        buf.write("\2\2@A\7\34\2\2AB\7\22\2\2B\t\3\2\2\2CD\7\r\2\2DE\7\34")
        buf.write("\2\2EF\7\22\2\2F\13\3\2\2\2GH\7\16\2\2HI\7\34\2\2IJ\7")
        buf.write("\22\2\2J\r\3\2\2\2KM\7\17\2\2LN\5\20\t\2ML\3\2\2\2NO\3")
        buf.write("\2\2\2OM\3\2\2\2OP\3\2\2\2PQ\3\2\2\2QR\7\20\2\2RS\5\26")
        buf.write("\f\2S\17\3\2\2\2TU\7\25\2\2UX\7\34\2\2VX\3\2\2\2WT\3\2")
        buf.write("\2\2WV\3\2\2\2XY\3\2\2\2Y[\7\22\2\2Z\\\7\24\2\2[Z\3\2")
        buf.write("\2\2[\\\3\2\2\2\\e\3\2\2\2]^\7\25\2\2^_\7\34\2\2_e\7\21")
        buf.write("\2\2`a\7\25\2\2ab\7\34\2\2be\5\24\13\2ce\5\22\n\2dW\3")
        buf.write("\2\2\2d]\3\2\2\2d`\3\2\2\2dc\3\2\2\2e\21\3\2\2\2fg\7\t")
        buf.write("\2\2gh\7\25\2\2h\23\3\2\2\2ij\b\13\1\2jr\7:\2\2kr\7=\2")
        buf.write("\2lr\7\25\2\2mn\7\26\2\2no\5\24\13\2op\7\27\2\2pr\3\2")
        buf.write("\2\2qi\3\2\2\2qk\3\2\2\2ql\3\2\2\2qm\3\2\2\2r{\3\2\2\2")
        buf.write("st\f\b\2\2tu\t\2\2\2uz\5\24\13\tvw\f\7\2\2wx\t\3\2\2x")
        buf.write("z\5\24\13\bys\3\2\2\2yv\3\2\2\2z}\3\2\2\2{y\3\2\2\2{|")
        buf.write("\3\2\2\2|\25\3\2\2\2}{\3\2\2\2~\177\5\32\16\2\177\27\3")
        buf.write("\2\2\2\u0080\u0081\t\4\2\2\u0081\u0085\7\7\2\2\u0082\u0083")
        buf.write("\7\25\2\2\u0083\u0086\7\n\2\2\u0084\u0086\7\b\2\2\u0085")
        buf.write("\u0082\3\2\2\2\u0085\u0084\3\2\2\2\u0086\31\3\2\2\2\u0087")
        buf.write("\u0088\b\16\1\2\u0088\u0093\7\25\2\2\u0089\u0093\5\30")
        buf.write("\r\2\u008a\u008b\5\24\13\2\u008b\u008c\t\5\2\2\u008c\u008d")
        buf.write("\5\24\13\2\u008d\u0093\3\2\2\2\u008e\u008f\7\26\2\2\u008f")
        buf.write("\u0090\5\32\16\2\u0090\u0091\7\27\2\2\u0091\u0093\3\2")
        buf.write("\2\2\u0092\u0087\3\2\2\2\u0092\u0089\3\2\2\2\u0092\u008a")
        buf.write("\3\2\2\2\u0092\u008e\3\2\2\2\u0093\u009c\3\2\2\2\u0094")
        buf.write("\u0095\f\4\2\2\u0095\u0096\7&\2\2\u0096\u009b\5\32\16")
        buf.write("\5\u0097\u0098\f\3\2\2\u0098\u0099\7%\2\2\u0099\u009b")
        buf.write("\5\32\16\4\u009a\u0094\3\2\2\2\u009a\u0097\3\2\2\2\u009b")
        buf.write("\u009e\3\2\2\2\u009c\u009a\3\2\2\2\u009c\u009d\3\2\2\2")
        buf.write("\u009d\33\3\2\2\2\u009e\u009c\3\2\2\2\24\37#*\62\658:")
        buf.write("OW[dqy{\u0085\u0092\u009a\u009c")
        return buf.getvalue()


class RuleParser ( Parser ):

    grammarFileName = "RuleParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'rule'", "'raw'", "'any'", "'all'", "'of'", 
                     "'them'", "'print'", "'$'", "'meta:'", "'type'", "'url'", 
                     "'description'", "'strings:'", "'condition:'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'nocase'", "<INVALID>", 
                     "'('", "')'", "'{'", "'}'", "'['", "']'", "'='", "','", 
                     "';'", "':'", "'.'", "'++'", "'--'", "':='", "'...'", 
                     "'||'", "'&&'", "'=='", "'!='", "'<'", "'<='", "'>'", 
                     "'>='", "'|'", "'/'", "'%'", "'<<'", "'>>'", "'&^'", 
                     "'!'", "'+'", "'-'", "'^'", "'*'", "'&'", "'<-'" ]

    symbolicNames = [ "<INVALID>", "RULE", "RAW", "ANY", "ALL", "OF", "THEM", 
                      "PRINT", "DOLLAR", "META", "TYPE", "URL", "DESCRIPTION", 
                      "STRINGS", "CONDITION", "HEX_STRING_LIT", "INTERPRETED_STRING_LIT", 
                      "REGEXP", "NOCASE", "IDENTIFIER", "L_PAREN", "R_PAREN", 
                      "L_CURLY", "R_CURLY", "L_BRACKET", "R_BRACKET", "ASSIGN", 
                      "COMMA", "SEMI", "COLON", "DOT", "PLUS_PLUS", "MINUS_MINUS", 
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
    RULE_printExpression = 8
    RULE_arithmeticExpression = 9
    RULE_logicalExpression = 10
    RULE_ofExpression = 11
    RULE_expression = 12

    ruleNames =  [ "rules", "ruleDec", "body", "typeExpression", "urlExpression", 
                   "descExpression", "mainExpression", "assignExpression", 
                   "printExpression", "arithmeticExpression", "logicalExpression", 
                   "ofExpression", "expression" ]

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
    HEX_STRING_LIT=15
    INTERPRETED_STRING_LIT=16
    REGEXP=17
    NOCASE=18
    IDENTIFIER=19
    L_PAREN=20
    R_PAREN=21
    L_CURLY=22
    R_CURLY=23
    L_BRACKET=24
    R_BRACKET=25
    ASSIGN=26
    COMMA=27
    SEMI=28
    COLON=29
    DOT=30
    PLUS_PLUS=31
    MINUS_MINUS=32
    DECLARE_ASSIGN=33
    ELLIPSIS=34
    LOGICAL_OR=35
    LOGICAL_AND=36
    EQUALS=37
    NOT_EQUALS=38
    LESS=39
    LESS_OR_EQUALS=40
    GREATER=41
    GREATER_OR_EQUALS=42
    OR_OP=43
    DIV=44
    MOD=45
    LSHIFT=46
    RSHIFT=47
    BIT_CLEAR=48
    EXCLAMATION=49
    PLUS=50
    MINUS=51
    CARET=52
    STAR=53
    AMPERSAND=54
    RECEIVE=55
    DECIMAL_LIT=56
    OCTAL_LIT=57
    HEX_LIT=58
    FLOAT_LIT=59
    IMAGINARY_LIT=60
    WS=61
    COMMENT=62
    TERMINATOR=63
    LINE_COMMENT=64

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
            self.state = 27 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 26
                self.ruleDec()
                self.state = 29 
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
            self.state = 31
            self.match(RuleParser.RULE)
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==RuleParser.DECIMAL_LIT:
                self.state = 32
                self.match(RuleParser.DECIMAL_LIT)


            self.state = 35
            self.match(RuleParser.IDENTIFIER)
            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==RuleParser.DOT:
                self.state = 36
                self.match(RuleParser.DOT)
                self.state = 37
                self.match(RuleParser.IDENTIFIER)
                self.state = 42
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 43
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
            self.state = 45
            self.match(RuleParser.L_CURLY)
            self.state = 56
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==RuleParser.META:
                self.state = 46
                self.match(RuleParser.META)
                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==RuleParser.TYPE:
                    self.state = 47
                    self.typeExpression()


                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==RuleParser.URL:
                    self.state = 50
                    self.urlExpression()


                self.state = 54
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==RuleParser.DESCRIPTION:
                    self.state = 53
                    self.descExpression()




            self.state = 58
            self.mainExpression()
            self.state = 59
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
            self.state = 61
            self.match(RuleParser.TYPE)
            self.state = 62
            self.match(RuleParser.ASSIGN)
            self.state = 63
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
            self.state = 65
            self.match(RuleParser.URL)
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
            self.state = 69
            self.match(RuleParser.DESCRIPTION)
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
            self.state = 73
            self.match(RuleParser.STRINGS)
            self.state = 75 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 74
                self.assignExpression()
                self.state = 77 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << RuleParser.PRINT) | (1 << RuleParser.INTERPRETED_STRING_LIT) | (1 << RuleParser.IDENTIFIER))) != 0)):
                    break

            self.state = 79
            self.match(RuleParser.CONDITION)
            self.state = 80
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

        def INTERPRETED_STRING_LIT(self):
            return self.getToken(RuleParser.INTERPRETED_STRING_LIT, 0)

        def IDENTIFIER(self):
            return self.getToken(RuleParser.IDENTIFIER, 0)

        def ASSIGN(self):
            return self.getToken(RuleParser.ASSIGN, 0)

        def NOCASE(self):
            return self.getToken(RuleParser.NOCASE, 0)

        def HEX_STRING_LIT(self):
            return self.getToken(RuleParser.HEX_STRING_LIT, 0)

        def arithmeticExpression(self):
            return self.getTypedRuleContext(RuleParser.ArithmeticExpressionContext,0)


        def printExpression(self):
            return self.getTypedRuleContext(RuleParser.PrintExpressionContext,0)


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
        self._la = 0 # Token type
        try:
            self.state = 98
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 85
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [RuleParser.IDENTIFIER]:
                    self.state = 82
                    self.match(RuleParser.IDENTIFIER)
                    self.state = 83
                    self.match(RuleParser.ASSIGN)
                    pass
                elif token in [RuleParser.INTERPRETED_STRING_LIT]:
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 87
                self.match(RuleParser.INTERPRETED_STRING_LIT)
                self.state = 89
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==RuleParser.NOCASE:
                    self.state = 88
                    self.match(RuleParser.NOCASE)


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 91
                self.match(RuleParser.IDENTIFIER)
                self.state = 92
                self.match(RuleParser.ASSIGN)
                self.state = 93
                self.match(RuleParser.HEX_STRING_LIT)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 94
                self.match(RuleParser.IDENTIFIER)
                self.state = 95
                self.match(RuleParser.ASSIGN)
                self.state = 96
                self.arithmeticExpression(0)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 97
                self.printExpression()
                pass


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
        self.enterRule(localctx, 16, self.RULE_printExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.match(RuleParser.PRINT)
            self.state = 101
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
        _startState = 18
        self.enterRecursionRule(localctx, 18, self.RULE_arithmeticExpression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RuleParser.DECIMAL_LIT]:
                self.state = 104
                self.match(RuleParser.DECIMAL_LIT)
                pass
            elif token in [RuleParser.FLOAT_LIT]:
                self.state = 105
                self.match(RuleParser.FLOAT_LIT)
                pass
            elif token in [RuleParser.IDENTIFIER]:
                self.state = 106
                self.match(RuleParser.IDENTIFIER)
                pass
            elif token in [RuleParser.L_PAREN]:
                self.state = 107
                self.match(RuleParser.L_PAREN)
                self.state = 108
                self.arithmeticExpression(0)
                self.state = 109
                self.match(RuleParser.R_PAREN)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 121
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,13,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 119
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
                    if la_ == 1:
                        localctx = RuleParser.ArithmeticExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_arithmeticExpression)
                        self.state = 113
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 114
                        _la = self._input.LA(1)
                        if not(_la==RuleParser.DIV or _la==RuleParser.STAR):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 115
                        self.arithmeticExpression(7)
                        pass

                    elif la_ == 2:
                        localctx = RuleParser.ArithmeticExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_arithmeticExpression)
                        self.state = 116
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 117
                        _la = self._input.LA(1)
                        if not(_la==RuleParser.PLUS or _la==RuleParser.MINUS):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 118
                        self.arithmeticExpression(6)
                        pass

             
                self.state = 123
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
        self.enterRule(localctx, 20, self.RULE_logicalExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
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
        self.enterRule(localctx, 22, self.RULE_ofExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << RuleParser.ANY) | (1 << RuleParser.ALL) | (1 << RuleParser.DECIMAL_LIT))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 127
            self.match(RuleParser.OF)
            self.state = 131
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RuleParser.IDENTIFIER]:
                self.state = 128
                self.match(RuleParser.IDENTIFIER)
                self.state = 129
                self.match(RuleParser.DOLLAR)
                pass
            elif token in [RuleParser.THEM]:
                self.state = 130
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
        _startState = 24
        self.enterRecursionRule(localctx, 24, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.state = 134
                self.match(RuleParser.IDENTIFIER)
                pass

            elif la_ == 2:
                self.state = 135
                self.ofExpression()
                pass

            elif la_ == 3:
                self.state = 136
                self.arithmeticExpression(0)
                self.state = 137
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << RuleParser.EQUALS) | (1 << RuleParser.LESS) | (1 << RuleParser.LESS_OR_EQUALS) | (1 << RuleParser.GREATER) | (1 << RuleParser.GREATER_OR_EQUALS))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 138
                self.arithmeticExpression(0)
                pass

            elif la_ == 4:
                self.state = 140
                self.match(RuleParser.L_PAREN)
                self.state = 141
                self.expression(0)
                self.state = 142
                self.match(RuleParser.R_PAREN)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 154
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 152
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
                    if la_ == 1:
                        localctx = RuleParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 146
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 147
                        self.match(RuleParser.LOGICAL_AND)
                        self.state = 148
                        self.expression(3)
                        pass

                    elif la_ == 2:
                        localctx = RuleParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 149
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 150
                        self.match(RuleParser.LOGICAL_OR)
                        self.state = 151
                        self.expression(2)
                        pass

             
                self.state = 156
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
        self._predicates[9] = self.arithmeticExpression_sempred
        self._predicates[12] = self.expression_sempred
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
         




