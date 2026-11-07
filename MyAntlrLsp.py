#pyright: basic
# 
import logging
import sys
import traceback
from pathlib import Path

from defaults.antlr_default import DefaultLoader

sys.path.insert(0, str(Path(__file__).resolve().parent / "grammar"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "checking"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "errors"))

from urllib.parse import unquote, urlparse

import antlr4
from antlr4.error.ErrorListener import (
    ErrorListener,
)
from lsprotocol import types as lsp
from MyAntlrGrammarLexer import MyAntlrGrammarLexer
from MyAntlrGrammarParser import MyAntlrGrammarParser
from MyAntlrTyping import MyAntlrTyping
from pygls.lsp.server import LanguageServer
from rapidfuzz import process

# logging.basicConfig(level=logging.INFO)  # stderr
# log = logging.getLogger("my-antlr4-lsp")
logging.basicConfig(
    filename="/tmp/antlr_lsp.log",
    filemode="w",  # Écrase le fichier à chaque relance du serveur
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger("my-antlr4-lsp")

server = LanguageServer("my-antlr4-lsp", "0.1")

default_vars = DefaultLoader()

def stem_from_uri(uri: str) -> str:
    return Path(unquote(urlparse(uri).path)).stem

def make_diag(line: int, col: int, len: int, msg: str):

    line = max(line - 1, 0)   # ANTLR : ligne depuis 1, LSP : depuis 0

    #j’arrive pas a réglre ce end position donc par défaut col + 1
    return lsp.Diagnostic(
        range=lsp.Range(lsp.Position(line, col), lsp.Position(line, col + len)),
        message=msg,
        severity=lsp.DiagnosticSeverity.Error,
        source="my-antlr4-lsp")

def make_safe_diag(line: int, col: int, len: int, msg: str):

    line = max(line - 1, 0)   # ANTLR : ligne depuis 1, LSP : depuis 0

    #j’arrive pas a réglre ce end position donc par défaut col + 1
    return lsp.Diagnostic(
        range=lsp.Range(lsp.Position(line, col), lsp.Position(line, col + len)),
        message=msg,
        severity=lsp.DiagnosticSeverity.Warning,
        source="my-antlr4-lsp")
    #j’aurais pu le rennomer
    # 
class MyErrorListener(ErrorListener):

    def __init__(self):
        super().__init__()
        self.diags: list[lsp.Diagnostic] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):   
        # self.count += 1
        self.diags.append(make_diag(line, column, len(offendingSymbol.text), msg))


class Analyzer:

    def __init__(self):
        self.diags = []
        self.actions = []

    def analyze(self, uri, text):
        self.diags = []
        self.actions = []
        counter = MyErrorListener()

        # input_s = antlr4.FileStream(inputname, encoding='utf-8')

        lexer = MyAntlrGrammarLexer(antlr4.InputStream(text))
        lexer.removeErrorListeners()
        lexer.addErrorListener(counter)

        stream = antlr4.CommonTokenStream(lexer)
        parser = MyAntlrGrammarParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(counter)

        tree = parser.program()


        if len(counter.diags) > 0:
            self.diags = counter.diags
            return
            # return counter.diags
            # sys.exit(3)  # Syntax or lexicography errors occurred, don't try to go further.
        del counter

        typing_visitor = MyAntlrTyping(stem_from_uri(uri))
        try:
            typing_visitor.visit(tree)
            for used_rule in typing_visitor.used_rules:
                token = used_rule.token
                if token.text not in typing_visitor.defined_rules and token.text not in default_vars.already_init_variable:
                    diag = make_diag(token.line, token.column, len(token.text), "Is not defined")
                    self.diags.append(diag)

                    # trouver la variable la plus proche écrite par l’utilisateur
                    best, score, _ = process.extractOne(
                        token.text, typing_visitor.get_name_typing_rules()
                    )
                    # on pourra gérer le score un peu plus tard
                    # see on
                    # https://pygls.readthedocs.io/en/latest/servers/examples/code-actions.html
                     
                    text_edit = lsp.TextEdit(
                        range=diag.range, new_text=best
                    )
                    action = lsp.CodeAction(
                        title=f"Replace with {best} with score: {score}",
                        kind=lsp.CodeActionKind.QuickFix,
                        diagnostics=[diag],
                        edit=lsp.WorkspaceEdit(changes={uri: [text_edit]}),
                    )
                    self.actions.append(action)

                    # trouver la variable la plus proche à définir par les defaults

                    best, score, _ = process.extractOne(
                        token.text, default_vars.can_be_initialized
                    )
                    # on pourra gérer le score un peu plus tard
                    # see on
                    # https://pygls.readthedocs.io/en/latest/servers/examples/code-actions.html
                     
                    text_edit = lsp.TextEdit(
                        range=diag.range, new_text=best
                    )
                    action = lsp.CodeAction(
                        title=f"Replace with {best} with score: {score}",
                        kind=lsp.CodeActionKind.QuickFix,
                        diagnostics=[diag],
                        edit=lsp.WorkspaceEdit(changes={uri: [text_edit]}),
                    )
                    self.actions.append(action)


        
            # msg= str(typing_visitor.defined_rules.keys()) + "\n\n\n" + str(typing_visitor.defined_tags.keys())  + "\n\n\n" + str(typing_visitor.used_rules) 
            # msg = str(len(self.actions))
            # self.diags.append(make_safe_diag(0, 0, 1, msg))



        
            for e in typing_visitor.errors:
                self.diags.append(make_diag(e.line, e.column, e.column + e.len, str(e)))
            for e in typing_visitor.warnings:
                self.diags.append(make_safe_diag(e.line, e.column, e.column + e.len, str(e)))
        except Exception as e:  # noqa: BLE001
            tb = traceback.extract_tb(e.__traceback__)[-3:]
            tbm = ""
            for trace in tb:
                tbm += "\n" + str(trace)

            msg = f"[crash du typeur] {e!s}\n{tbm}"
            self.diags.append(make_diag(0, 0, 1,  msg))
        return 

analyzer = Analyzer()

def publish(ls: LanguageServer, uri: str):
    doc = ls.workspace.get_text_document(uri)
    analyzer.analyze(doc.uri, doc.source)
    ls.text_document_publish_diagnostics(
        lsp.PublishDiagnosticsParams(uri=doc.uri, diagnostics=analyzer.diags)
    )

def intersection(range1:lsp.Range, range2:lsp.Range) -> bool:
    # log.info("auie")
    # log.info(range1)
    # log.info(type(range1))
    # log.info(range2)
    # log.info(type(range2))
    # start_line = max(range1.start.line, range2.start.line)
    # end_line = min(range1.end.line, range2.end.line)
    # log.info("1")
    # if start_line > end_line:
    #     return False
    # log.info("2")
    # if start_line < end_line:
    #     return True

    # log.info("3")
    # start_col = max(range1.start.character, range2.start.character)
    # end_col = min(range1.end.character, range2.end.character)
    # log.info(start_col)
    # log.info(end_col)
    # return start_col <= end_col
    start1before2 = range1.start.line < range2.start.line or (range1.start.line == range2.start.line and range1.start.character <= range2.start.character)
    end1after2= range1.end.line > range2.start.line or (range1.end.line == range2.start.line and range1.end.character >= range2.start.character)
    start2before1 = range2.start.line < range1.start.line or (range2.start.line == range1.start.line and range2.start.character <= range1.start.character)
    end2after1= range2.end.line > range1.start.line or (range2.end.line == range1.start.line and range2.end.character >= range1.start.character)
    return (start1before2 and end1after2) or (start2before1 and end2after1)

@server.feature(lsp.TEXT_DOCUMENT_CODE_ACTION)
def code_actions(ls: LanguageServer, params: lsp.CodeActionParams) -> list[lsp.CodeAction]:
    actions = []
    mouse_range = params.range
    for a in analyzer.actions:
        # msg = "auie" + str(mouse_range) + "///" + str(a.diagnostics[0]) + "///" + str(a.diagnostics[0].range)
        # log.info(msg)
        if intersection(mouse_range, a.diagnostics[0].range):
            actions.append(a)
        
    return actions

@server.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls, params: lsp.DidOpenTextDocumentParams):
    publish(ls, params.text_document.uri)


@server.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: lsp.DidChangeTextDocumentParams):
    publish(ls, params.text_document.uri)


@server.feature(lsp.TEXT_DOCUMENT_DID_SAVE)
def did_save(ls, params: lsp.DidSaveTextDocumentParams):
    publish(ls, params.text_document.uri)


if __name__ == "__main__":
    server.start_io()

