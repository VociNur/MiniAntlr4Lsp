#pyright: basic
# pyright: reportArgumentType=false, reportOptionalMemberAccess=false, reportAttributeAccessIssue=false, reportOptionalIterable=false, reportGeneralTypeIssues=false,reportWildcardImportFromLibrary=false
from antlr4 import *
from lsprotocol import types as lsp
from MyAntlrErrors import MyAntlrErrorTyping
from MyAntlrGrammarParser import *
from MyAntlrGrammarVisitor import (
    MyAntlrGrammarVisitor,  # pyright: ignore[reportWildcardImportFromLibrary]
)


class UsedRule:
    def __init__(self, token: Token) -> None:
        self.token = token
        
    def __str__(self) -> str:
        return self.token.text

    def __repr__(self) -> str:
        return self.__str__()
           
class MyAntlrTyping(MyAntlrGrammarVisitor):


    def __init__(self, filename=""):
        self.used= {}
        self.defined_rules: dict[str, Token] = {}
        self.used_rules: list[UsedRule] = []
        self.defined_tags: dict[str, Token] = {}
        self.errors = []
        self.warnings = []
        self.filename = filename
        self.to_print = ""
        self.lexer_position_start : lsp.Position = None

    def __mprint__(self, msg):
        self.to_print += str(msg) + "\n"
    
    def get_name_typing_rules(self)->list[str]:
        return list(self.defined_rules.keys())

    def _raise(self, ctx, msg):
        self.errors.append(MyAntlrErrorTyping(msg, ctx.start.line, ctx.start.column, ctx.start.stop))

    def _raise_warning(self, ctx, msg):
        self.warnings.append(MyAntlrErrorTyping(msg, ctx.start.line, ctx.start.column, ctx.start.stop))

    def _raise_tok(self, tok, msg):


        # msg = msg + f"\ndebugtoken: {tok}\ndebug tok: {tok}\ntext:{tok.text}"
        self.errors.append(MyAntlrErrorTyping(msg, tok.line, tok.column, len(tok.text)))

    def _raise_warning_tok(self, tok, msg):


        # msg = msg + f"\ndebugtoken: {tok}\ndebug tok: {tok}\ntext:{tok.text}"
        self.warnings.append(MyAntlrErrorTyping(msg, tok.line, tok.column, len(tok.text)))

    def _define_rule(self, node):
        # if ruleName in self.defined_rules:
        #     self._raise(ctx, "Rule already defined")
        #
        tok = node.symbol
        name = tok.text
        if name == "":
            self._raise_tok(tok, "Token cannot be empty")
            return
        if name in self.defined_rules:

            first_tok = self.defined_rules[name]
            self._raise_tok(tok, f"This token is already defined as a rule at line {first_tok.line}")
            self._raise_warning_tok(first_tok, "You try to define a new time this rule later")

            return

        if name in self.defined_tags:
            tag = self.defined_tags[name]
            self._raise_tok(tok, f"This token is already defined as a tag at line {tag.line}")
            self._raise_tok(tag, "This token is also defined as a tag")

            return
        self.defined_rules[name] = tok

    def _define_tag(self, node):
        token = node.symbol
        name = token.text
        if name == "":
            self._raise_tok(token, "Token cannot be empty")
            return
        if name in self.defined_tags:
            first_tag = self.defined_tags[name]
            self._raise_tok(token, f"This token is already defined as a tag at {first_tag.line}")
            self._raise_warning_tok(first_tag, "You try to define a new time this tag later")

            return

        if name in self.defined_rules:
            first_tok = self.defined_rules[name]
            self._raise_tok(token, f"This token is already defined as a rule at {first_tok.line}")
            self._raise_tok(first_tok, "This token is also defined as a rule")

            return
        self.defined_tags[name] = token
    # Visit a parse tree produced by MyAntlrGrammarParser#program.
    def visitProgram(self, ctx:MyAntlrGrammarParser.ProgramContext):
        # return self.visitChildren(ctx)
        self.visit(ctx.header())
        self.visit(ctx.my_rules())


    # Visit a parse tree produced by MyAntlrGrammarParser#header.
    def visitHeader(self, ctx:MyAntlrGrammarParser.HeaderContext):
        self.visit(ctx.grammar_name())


    # Visit a parse tree produced by MyAntlrGrammarParser#grammarDecl.
    def visitGrammarDecl(self, ctx:MyAntlrGrammarParser.GrammarDeclContext):
        grammarName = ctx.ID().getText()
        if grammarName != self.filename:
            self._raise_tok(ctx.ID().symbol, f"Grammar name different from file name\nGrammar name: {ctx.ID().getText()}\nFilename: {self.filename}")



    # Visit a parse tree produced by MyAntlrGrammarParser#optionDecl.
    def visitOptionDecl(self, ctx:MyAntlrGrammarParser.OptionDeclContext):
        return 


    # Visit a parse tree produced by MyAntlrGrammarParser#tokensDecl.
    def visitTokensDecl(self, ctx:MyAntlrGrammarParser.TokensDeclContext):
        return 


    # Visit a parse tree produced by MyAntlrGrammarParser#codeHeaderDecl.
    def visitCodeHeaderDecl(self, ctx:MyAntlrGrammarParser.CodeHeaderDeclContext):
        return 


    # Visit a parse tree produced by MyAntlrGrammarParser#codeMembersDecl.
    def visitCodeMembersDecl(self, ctx:MyAntlrGrammarParser.CodeMembersDeclContext):
        return
    
    # Visit a parse tree produced by MyAntlrGrammarParser#myRuleList.
    def visitMyRuleList(self, ctx:MyAntlrGrammarParser.MyRuleListContext):
        for r in ctx.my_rule():
            self.visit(r)

    # Visit a parse tree produced by MyAntlrGrammarParser#ruleDecl.
    def visitRuleDecl(self, ctx:MyAntlrGrammarParser.RuleDeclContext):
        # self.defined_rules.append(ctx.ID().symbol)
        self._define_rule(ctx.ID())
        if ctx.ID().symbol.text[0].islower() and self.lexer_position_start is not None:
            pass
            # diagnose TODO
            
        if ctx.ID().symbol.text[0].isupper() and self.lexer_position_start is None:
                self.lexer_position_start = lsp.Position(ctx.start.line-1, 0)# lsp et antlr ne parlent pas pareil.
        self.visit(ctx.branch_l())

    def visitFragmentDecl(self, ctx:MyAntlrGrammarParser.FragmentDeclContext):
        self._define_rule(ctx.ID())
        self.visit(ctx.branch_l())

    # Visit a parse tree produced by MyAntlrGrammarParser#branchListBase.
    def visitBranchListBase(self, ctx:MyAntlrGrammarParser.BranchListBaseContext):
        self.visit(ctx.branch())   


    # Visit a parse tree produced by MyAntlrGrammarParser#branchList.
    def visitBranchList(self, ctx:MyAntlrGrammarParser.BranchListContext):
        self.visit(ctx.branch())
        return self.visit(ctx.branch_l())


    # Visit a parse tree produced by MyAntlrGrammarParser#myParserRule.
    def visitMyParserRule(self, ctx:MyAntlrGrammarParser.MyParserRuleContext):
        self.visit(ctx.expr())
        tag = ctx.tagName()
        if tag is not None:
            self._define_tag(tag.ID())


    # Visit a parse tree produced by MyAntlrGrammarParser#myLexerRule.
    def visitMyLexerRule(self, ctx:MyAntlrGrammarParser.MyLexerRuleContext):
        self.visit(ctx.expr())

    # Visit a parse tree produced by MyAntlrGrammarParser#onlyTagName.
    def visitOnlyTagName(self, ctx:MyAntlrGrammarParser.OnlyTagNameContext):
        self._raise_warning(ctx, "Avoid empty branch, use \'?\'")
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by MyAntlrGrammarParser#realCode.
    def visitRealCode(self, ctx:MyAntlrGrammarParser.RealCodeContext):
        return


    # Visit a parse tree produced by MyAntlrGrammarParser#skipCode.
    def visitSkipCode(self, ctx:MyAntlrGrammarParser.SkipCodeContext):
        return

    # Visit a parse tree produced by MyAntlrGrammarParser#exprBase.
    def visitExprBase(self, ctx:MyAntlrGrammarParser.ExprBaseContext):
        self.visit(ctx.value_modif())


    # Visit a parse tree produced by MyAntlrGrammarParser#pipeExpr.
    def visitPipeExpr(self, ctx:MyAntlrGrammarParser.PipeExprContext):
        self.visit(ctx.value_modif())
        self.visit(ctx.expr())

    # Visit a parse tree produced by MyAntlrGrammarParser#concatExpr.
    def visitConcatExpr(self, ctx:MyAntlrGrammarParser.ConcatExprContext):
        self.visit(ctx.value_modif())
        self.visit(ctx.expr())

    # Visit a parse tree produced by MyAntlrGrammarParser#valueModif.
    def visitValueModif(self, ctx:MyAntlrGrammarParser.ValueModifContext):
        self.visit(ctx.value())


    # Visit a parse tree produced by MyAntlrGrammarParser#modif.
    def visitModif(self, ctx:MyAntlrGrammarParser.ModifContext):
        return


    # Visit a parse tree produced by MyAntlrGrammarParser#parValue.
    def visitParValue(self, ctx:MyAntlrGrammarParser.ParValueContext):
        self.visit(ctx.expr())


    # Visit a parse tree produced by MyAntlrGrammarParser#idWithNameValue.
    def visitIdWithNameValue(self, ctx:MyAntlrGrammarParser.IdWithNameValueContext):
        # return self.visitChildren(ctx)
        # faudrait s’intéresser à ce qu’il est possible de faire, à priori dans une même branche il faut des "ID =" unique
        self.visit(ctx.value())
    # bon en vrai c’est pas parfait, on peut ici carrément faire bon=jour=ID...

    # Visit a parse tree produced by MyAntlrGrammarParser#idValue.
    def visitIdValue(self, ctx:MyAntlrGrammarParser.IdValueContext):
        # return self.visitChildren(ctx)
        self.used_rules.append(UsedRule(ctx.ID().symbol))


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



