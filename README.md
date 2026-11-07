# MiniAntlr4Lsp


## Install MyantlrLsp
In the folder you want to install the LSP (ex: ~/Documents/Lsp/MiniAntlrLsp/)

git clone git@github.com:VociNur/MiniAntlr4Lsp.git
make install
Then add this lsp to your IDE.

### Add lsp to Helix IDE.
Edit your ~/.config/helix/languages.toml in adding

"""
[language-server.myantlr-lsp]
command = "myantlr-lsp"

[[language]]
name = "antlr4"
scope = "source.antlr4"
file-types = ["g4"]
comment-tokens = ["//"]

# language-servers = ["efm"]
block-comment-tokens = { start = "/*", end = "*/" }
indent = { tab-width = 4, unit = "    " }
roots = []
language-servers = ["myantlr-lsp"]
"""

Then you can open any .g4 file, antlr4 should be printed in the bottom-right corner. And lsp should work.
