antlr4 = java -jar ~/lib/antlr-4.13.2-complete.jar 
	 
# for debug
python:
	java -jar /home/jules/lib/antlr-4.13.2-complete.jar MyAntlrGrammar.g4 -Dlanguage=Python3 -visitor -no-listener -Werror

antlr:
	$(antlr4) *.g4

javac:
	javac *.java

# run:
# 	java org.antlr.v4.gui.TestRig MaGrammaire prog -tree

run_tokens:
	java org.antlr.v4.gui.TestRig MyAntlrGrammar program -tokens $(FILE)

run_gui:
	java org.antlr.v4.gui.TestRig MyAntlrGrammar program -gui $(FILE)

run_trace:
	java org.antlr.v4.gui.TestRig MyAntlrGrammar program -trace $(FILE)

run_tree:
	java org.antlr.v4.gui.TestRig MyAntlrGrammar program -tree $(FILE)

clean:
	rm -f *.class *.java *.tokens *.interp
	rm -f MyAntlrGrammar*.py MyAntlrGrammar*.interp MyAntlrGrammar*.tokens
