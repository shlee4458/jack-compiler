#!/usr/bin/env python
import sys, os
import re
import definitions

'''
This program is a jack compiler engine for the jack high level programming language.
Program Structure:
    class:
        branches - 
            classVarDec(';'): startswith - (static | field), endswith - ; (symbol and ';')
            subroutineDec: startswith - keyword, ends when the first '{' ends with the respective '}'
                parameterList('()'): in the first '(', include every token, until the first ')'
                subroutineBody: starts at the end of the parameterList(or start of the '{')
                                and ends when the corresponding '}' is found
                    statements('{}'): starts after the first opening tag 
                        letStatement - let a = b
                            pre expression; let a =
                            expression:
                                term: b
                        doStatement - do Keyboard.methodname(x, y)
                            pre expression: 
                            expressionList: after the '('
                                expression:
                                    term:
                        ifStatement - if (a = b) { statements }
                            pre expression if (
                            expression: 
                                term: a + b = c
                            post expression: ), {
                            statements
                                .... recursively call writeStatements
                        whileStatement - while (a = b) { statements }
                            pre expression: while (
                            expression: a + b = c
                            post expression: ), {
                            statements
                                .... recursively call writeStatements
                        returnStatement - return ;

            expressionList: list of expressions
            expression: comination of terms and symbol
'''

DEBUG_MODE = False

class CompilerEngine:
    
    def __init__(self, tokenFile):
        self.tokenFile = open(tokenFile, "r")
        self.outputFile = self.getOutputFile(tokenFile)
        self.line = self.tokenFile.readline()
        self.triple = [] # represents [opening tag, token, closing tag]
        self.open = 0
        self.tabs = 0

    def getOutputFile(self, tokenFile):
        outputFile = os.path.basename(tokenFile)[:-len("T.xml")] + ".xml"
        return open(outputFile, "w")
    
    def run(self):        
        # skip the line containing token tag, and load with the next token
        self.advance()
        
        # recursively call wrapping functions, starting from writeClass
        self.writeClass()

    def writeClass(self):
        self.writeCurrentTag("class", True) # write opening tag

        # write until classVarDec starts
        self.tabs += 1
        self.writeUntilFound("{", True)
        self.tabs -= 1

        # write classVarDec and subroutineDec
        self.writeClassVarDec() 
        self.writeSubRoutineDec()

        # write closing tag
        self.writeCurrentTag("class", False) # write closing tag

        # close the file
        self.close()

    def writeClassVarDec(self):
        while not self.isEnd() and self.triple[1] in ["static", "field"]:
            self.tabs += 1
            self.writeCurrentTag("classVarDec", True) # write opening tag
            self.tabs += 1
        
            # include all the tokens before the first ";"
            self.writeUntilFound(";", True)

            self.tabs -= 1
            self.writeCurrentTag("classVarDec", False) # write closing tag
            self.tabs -= 1

    def writeSubRoutineDec(self):
        self.tabs += 1
        self.writeCurrentTag("subroutineDec", True) # write opening tag
        self.tabs += 1

        # include all the tokens before paramList
        self.writeUntilFound("(", True) # current block ends with "("

        # write paramList
        self.writeParamList()

        # write a single symbol
        self.writeSingle()
    
        # write subroutineBody
        self.writeSubRoutineBody()

        self.tabs -= 1
        self.writeCurrentTag("subroutineDec", False) # write closing tag

        # write "}"
        self.writeSingle()

        self.tabs -= 1

    def writeParamList(self):
        self.writeCurrentTag("parameterList", True) # write opening tag
        self.tabs += 1

        # include all the list of tokens between paramList
        self.writeUntilFound(')', False) # ")" current block ends before ")" -- do not include in the current

        self.tabs -= 1
        self.writeCurrentTag("parameterList", False) # write closing tag

    def writeSubRoutineBody(self):
        self.writeCurrentTag("subroutineBody", True) # write opening tag
        self.tabs += 1

        # include the opening tag before writing statements
        self.writeUntilFound("{", True)

        # write varDec if found
        self.writeVarDec()

        # write statements
        self.writeStatements()

        self.tabs -= 1
        self.writeCurrentTag("subroutineBody", False) # write closing tag

    def writeVarDec(self):
        while self.triple[1] in ["var"]:
            self.writeCurrentTag("varDec", True) # write opening tag
            self.tabs += 1

            # write until ";" is found
            self.writeUntilFound(";", True)

            self.tabs -= 1
            self.writeCurrentTag("varDec", False) # write closing tag

    def writeStatements(self):
        self.writeCurrentTag("statements", True) # write opening tag
        self.tabs += 1
        self.open += 1
        # write opening symbol 
        while self.open: # while there is open statements

            # write let / if / while / do / return statements
            # if it is "letStatement"
            if self.triple[1] == "let":
                self.writeLetStatement()

            # if it is "ifStatement"
            elif self.triple[1] == "if":
                self.writeIfStatement()

            # if it is "whileStatement"
            elif self.triple[1] == "while":
                self.writeWhileStatement()

            # if it is "doStatement"
            elif self.triple[1] == "do":
                self.writeDoStatement()

            # if it is "returnStatement"
            elif self.triple[1] == "return":
                self.writeReturnStatement()

            # update the open if the current statement is closed
            if self.triple[1] == "}":
                self.writeSingle()
                self.open -= 1
                break

        # write closing symbol
        self.tabs -= 1
        self.writeCurrentTag("statements", False) # write opening tag

    def writeLetStatement(self):
        self.writeCurrentTag("letStatement", True) # write opening tag
        self.tabs += 1        

        # write LHS
        self.writeUntilFound(["[", "="], False)
        if self.triple[1] == "[":
            self.writeSingle()
            self.writeExpression()
        
        # finsish the LHS
        self.writeUntilFound('=', True)

        # write RHS
        self.writeExpression()

        # write until ";" is found
        self.writeUntilFound(';', True)

        self.tabs -= 1
        self.writeCurrentTag("letStatement", False) # write opening tag
        
    def writeIfStatement(self):
        self.writeCurrentTag("ifStatement", True) # write opening tag
        self.tabs += 1

        # write until the (, where the expression for checking condition starts
        self.writeUntilFound("(", True) 

        # expression
        self.writeExpression()

        # write until the statements start
        self.writeUntilFound("{", True)

        # more statements
        self.writeStatements()

        self.tabs -= 1
        self.writeCurrentTag("ifStatement", False) # write opening tag

    def writeWhileStatement(self):
        self.writeCurrentTag("whileStatement", True) # write opening tag
        self.tabs += 1

        # write until the condition checking starts
        self.writeUntilFound("(", True)

        # expression
        self.writeExpression()

        # write until the statements start
        self.writeUntilFound("{", True)

        # more statements
        self.writeStatements()

        self.tabs -= 1
        self.writeCurrentTag("whileStatement", False) # write opening tag

    def writeDoStatement(self):
        self.writeCurrentTag("doStatement", True) # write opening tag
        self.tabs += 1

        # pre expression
        self.writeUntilFound("(", False)

        # write expressionList
        self.writeExpressionList()

        # write ;
        self.writeSingle()

        self.tabs -= 1
        self.writeCurrentTag("doStatement", True) # write opening tag

    def writeReturnStatement(self):
        self.writeCurrentTag("returnStatement", True) # write opening tag
        self.tabs += 1

        # write until ; is found, inclusive
        self.writeUntilFound(";", True)

        self.tabs -= 1
        self.writeCurrentTag("returnStatement", False) # write opening tag

    def writeExpression(self):
        self.writeCurrentTag("expression", True) # write opening tag
        self.tabs += 1

        # while it is not the end of the expression
            # ']' -- indexing -> let a[i]
            # ')' -- condition checking -> while (a > b)
            # ';' -- end of let -> let a = 1 + 2;
            # ',' -- separate expresssionList -> Screen.print(a, b)
        while self.triple[1] not in ["]", ")", ";", ","]:
            # write term
            if self.triple[1] not in definitions.OPERATIONS:
                self.writeTerm()

            # write operation symbols; 
            if self.triple[1] in definitions.OPERATIONS:
                self.writeSingle()

        self.tabs -= 1
        self.writeCurrentTag("expression", False) # write closing tag

    def writeTerm(self):
        self.writeCurrentTag("term", True) # write opening tag
        self.tabs += 1

        # a[i], a + b, keyboard.space(abe);
        # write until [symbols, "(", "]", ";", ")"]

        while self.triple[1] not in definitions.OPERATIONS and self.triple[1] not in ["(", "[", "]", ";", ")"]:
            self.writeSingle()

        # if expressionList starts
        if self.triple[1] == "(":
            self.writeExpressionList()

        # if expression starts
        if self.triple[1] == '[':
            self.writeSingle()
            self.writeExpression()
            self.writeSingle()

        self.tabs -= 1
        self.writeCurrentTag("term", False) # write closing tag

    def writeExpressionList(self):
        '''
        This is called when Keyboard.screen(a, b).., when triple[1] == a
            writeExpression should be called until the first ")"
        '''
        self.writeSingle() # write "("
        self.writeCurrentTag("expressionList", True) # write opening tag
        self.tabs += 1

        # write expression
        while self.triple[1] != ")":
            self.writeExpression()

        self.tabs -= 1
        self.writeCurrentTag("expressionList", False) # write closing tag
        self.writeSingle() # write ")"

    def writeCurrentTag(self, tagName, open):
        '''
        Write the tagName to the output.
        '''
        tag = self.getTag(tagName, open)
        if DEBUG_MODE:
            print(f"Wrote the tag {tagName}")
        self.outputFile.write(tag)

    def getTag(self, tagName, open):
        '''
        Get the opened or closing tag.
        '''
        space = "  " * self.tabs
        return f"{space}<{tagName}>\n" if open else f"{space}</{tagName}>\n"

    def close(self):
        '''
        Close open file for both writing and reading.
        '''
        self.tokenFile.close()
        self.outputFile.close()

    def advance(self):
        self.triple = self.tokenFile.readline().strip('\n').split()
        print(self.triple)

        # if current line is not a single word
        if len(self.triple) > 1:
            self.triple = [self.triple[0]] + [" ".join(self.triple[1:-1])] + [self.triple[-1]]

        return self.triple

    def writeSingle(self):
        self.writeWithTab()
        self.advance()

    def writeUntilFound(self, tokens, end):
        '''
        Write the triple of the [opening tag, token, closing tag] in a line
        until the token is found.
            i.e writeClassVarDec will be written until 'j' is found 
        If it is the end of the current block, write the last triple in with the tab
        and update the triple.
        '''

        while not self.isEnd() and self.triple[1] not in tokens:
            self.writeSingle()
        
        if not self.isEnd() and end:
            self.writeSingle()

    def writeWithTab(self):
        '''
        Write to the output file the text with \t by self.tabs times prefixed.
        '''
        print(self.triple)
        text = ("  " * self.tabs) + (" ".join(self.triple)) + '\n'
        if DEBUG_MODE:
            print(f"Wrote the text {text}")
        self.outputFile.write(text)

    def isEnd(self):
        '''
        If the self.triple has only one element after advancing, it is the end
        '''
        return len(self.triple) == 1

if __name__ == "__main__":
    engine = CompilerEngine(sys.argv[1])
    engine.run()