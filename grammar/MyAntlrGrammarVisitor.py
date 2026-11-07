# Generated from MyAntlrGrammar.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MyAntlrGrammarParser import MyAntlrGrammarParser
else:
    from MyAntlrGrammarParser import MyAntlrGrammarParser

# This class defines a complete generic visitor for a parse tree produced by MyAntlrGrammarParser.

class MyAntlrGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MyAntlrGrammarParser#program.
    def visitProgram(self, ctx:MyAntlrGrammarParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#header.
    def visitHeader(self, ctx:MyAntlrGrammarParser.HeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#grammarDecl.
    def visitGrammarDecl(self, ctx:MyAntlrGrammarParser.GrammarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#optionDecl.
    def visitOptionDecl(self, ctx:MyAntlrGrammarParser.OptionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#tokensDecl.
    def visitTokensDecl(self, ctx:MyAntlrGrammarParser.TokensDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#codeHeaderDecl.
    def visitCodeHeaderDecl(self, ctx:MyAntlrGrammarParser.CodeHeaderDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#codeMembersDecl.
    def visitCodeMembersDecl(self, ctx:MyAntlrGrammarParser.CodeMembersDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#myRuleList.
    def visitMyRuleList(self, ctx:MyAntlrGrammarParser.MyRuleListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#ruleDecl.
    def visitRuleDecl(self, ctx:MyAntlrGrammarParser.RuleDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#fragmentDecl.
    def visitFragmentDecl(self, ctx:MyAntlrGrammarParser.FragmentDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#branchListBase.
    def visitBranchListBase(self, ctx:MyAntlrGrammarParser.BranchListBaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#branchList.
    def visitBranchList(self, ctx:MyAntlrGrammarParser.BranchListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#myParserRule.
    def visitMyParserRule(self, ctx:MyAntlrGrammarParser.MyParserRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#myLexerRule.
    def visitMyLexerRule(self, ctx:MyAntlrGrammarParser.MyLexerRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#onlyTagName.
    def visitOnlyTagName(self, ctx:MyAntlrGrammarParser.OnlyTagNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#realCode.
    def visitRealCode(self, ctx:MyAntlrGrammarParser.RealCodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#skipCode.
    def visitSkipCode(self, ctx:MyAntlrGrammarParser.SkipCodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#exprBase.
    def visitExprBase(self, ctx:MyAntlrGrammarParser.ExprBaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#pipeExpr.
    def visitPipeExpr(self, ctx:MyAntlrGrammarParser.PipeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#concatExpr.
    def visitConcatExpr(self, ctx:MyAntlrGrammarParser.ConcatExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#valueModif.
    def visitValueModif(self, ctx:MyAntlrGrammarParser.ValueModifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#modif.
    def visitModif(self, ctx:MyAntlrGrammarParser.ModifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#parValue.
    def visitParValue(self, ctx:MyAntlrGrammarParser.ParValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#idWithNameValue.
    def visitIdWithNameValue(self, ctx:MyAntlrGrammarParser.IdWithNameValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#idValue.
    def visitIdValue(self, ctx:MyAntlrGrammarParser.IdValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#regExpValue.
    def visitRegExpValue(self, ctx:MyAntlrGrammarParser.RegExpValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#stringValue.
    def visitStringValue(self, ctx:MyAntlrGrammarParser.StringValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#plusRegExp.
    def visitPlusRegExp(self, ctx:MyAntlrGrammarParser.PlusRegExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#bracketRegExp.
    def visitBracketRegExp(self, ctx:MyAntlrGrammarParser.BracketRegExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#notRegExp.
    def visitNotRegExp(self, ctx:MyAntlrGrammarParser.NotRegExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#starRegExp.
    def visitStarRegExp(self, ctx:MyAntlrGrammarParser.StarRegExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#dotRegExp.
    def visitDotRegExp(self, ctx:MyAntlrGrammarParser.DotRegExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#withTagName.
    def visitWithTagName(self, ctx:MyAntlrGrammarParser.WithTagNameContext):
        return self.visitChildren(ctx)



del MyAntlrGrammarParser