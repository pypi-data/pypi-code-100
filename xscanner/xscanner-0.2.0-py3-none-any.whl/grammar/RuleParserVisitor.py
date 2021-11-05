# Generated from anltr/RuleParser.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .RuleParser import RuleParser
else:
    from RuleParser import RuleParser

# This class defines a complete generic visitor for a parse tree produced by RuleParser.

class RuleParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RuleParser#rules.
    def visitRules(self, ctx:RuleParser.RulesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#ruleDec.
    def visitRuleDec(self, ctx:RuleParser.RuleDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#body.
    def visitBody(self, ctx:RuleParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#typeExpression.
    def visitTypeExpression(self, ctx:RuleParser.TypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#urlExpression.
    def visitUrlExpression(self, ctx:RuleParser.UrlExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#descExpression.
    def visitDescExpression(self, ctx:RuleParser.DescExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#mainExpression.
    def visitMainExpression(self, ctx:RuleParser.MainExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#assignExpression.
    def visitAssignExpression(self, ctx:RuleParser.AssignExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#zipExpression.
    def visitZipExpression(self, ctx:RuleParser.ZipExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#zipHexExpression.
    def visitZipHexExpression(self, ctx:RuleParser.ZipHexExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#printExpression.
    def visitPrintExpression(self, ctx:RuleParser.PrintExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#arithmeticExpression.
    def visitArithmeticExpression(self, ctx:RuleParser.ArithmeticExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#logicalExpression.
    def visitLogicalExpression(self, ctx:RuleParser.LogicalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#ofExpression.
    def visitOfExpression(self, ctx:RuleParser.OfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RuleParser#expression.
    def visitExpression(self, ctx:RuleParser.ExpressionContext):
        return self.visitChildren(ctx)



del RuleParser