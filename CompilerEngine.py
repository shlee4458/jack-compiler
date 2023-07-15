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
                        doStatement - do Keyboard.methodname(x, y)
                            pre expression: 
                            expressionList: after the '('
                                expression:
                                    term:
                        returnStatement - return ;
'''

DEBUG_MODE = True

class CompilerEngine:
    
    def __init__(self, tokenFile):
        self.tokenFile = open(tokenFile, "r")
        self.outputFile = self.getOutputFile(tokenFile)
        self.line = self.tokenFile.readline()
        self.triple = [] # represents [opening tag, token, closing tag]
        self.tabs = 0

    def getOutputFile(self, tokenFile):
        outputFile = os.path.basename(tokenFile)[:-len("T.xml")] + ".xml"
        return open(outputFile, "w")

    def writeClass(self):
        self.writeCurrentTag("class", True) # write opening tag

        # write tokens before the classVarDec starts
        self.tabs += 1
        self.writeUntilFound(["static", "field"], False) # TODO: check assumption that there will always be static/field
        self.tabs -= 1

        # write classVarDec and subroutineDec
        self.writeClassVarDec() 
        self.writeSubRoutineDec()

        # write closing tag
        self.writeCurrentTag("class", False) # write closing tag

    def writeClassVarDec(self):
        while self.triple[1] in ["static", "field"]:
            self.tabs += 1
            self.writeCurrentTag("classVarDec", True) # write opening tag
            self.tabs += 1
        
            # include all the tokens before the first ";"
            self.writeUntilFound(";", True)

            self.tabs -= 1
            self.writeCurrentTag("classVarDec", False) # write closing tag
            self.tabs -= 1

    def writeUntilFound(self, tokens, end):
        '''
        Write the triple of the [opening tag, token, closing tag] in a line
        until the token is found.
            i.e writeClassVarDec will be written until 'j' is found 
        If it is the end of the current block, write the last triple in with the tab
        and update the triple.
        '''
        while self.triple[1] not in tokens or not self.triple:
            self.writeWithTab()
            self.advance()
        
        if end:
            self.writeWithTab()
            self.advance()

    def writeWithTab(self):
        '''
        Write to the output file the text with \t by self.tabs times prefixed.
        '''
        print(self.triple)
        text = ("  " * self.tabs) + (" ".join(self.triple)) + '\n'
        if DEBUG_MODE:
            print(f"Wrote the text {text}")
        self.outputFile.write(text)

    def writeSubRoutineDec(self):
        self.tabs += 1
        self.writeCurrentTag("subroutineDec", True) # write opening tag
        self.tabs += 1

        # include all the tokens before paramList
        self.writeUntilFound("(", True) # current block ends with "("

        # write paramList
        self.writeParamList()

        # write a single symbol
        self.writeUntilFound(")", True)
    
        # write subroutineBody
        self.writeSubRoutineBody()

        self.tabs -= 1
        self.writeCurrentTag("subroutineDec", False) # write closing tag
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

        # write statements
        # self.writeStatements()

        self.tabs -= 1
        self.writeCurrentTag("subroutineBody", False) # write closing tag

    def writeStatements(self):
        stack = [] # use stack to keep track of the current token, including closing and opening tag
        self.writeCurrentTag("statements", True) # write opening tag
        self.tabs += 1
        # write opening symbol 
        while self.line != "}":

            # write let / if / while / do / return statements
            # if it is "letStatement"


            # if it is "ifStatement"

            # if it is "whileStatement"

            # if it is "doStatement"

            # if it is "returnStatement"

            pass        
        # write closing symbol
        self.tabs -= 1
        self.writeCurrentTag("statements", False) # write opening tag

    def writeLetStatement(self):
        self.tabs += 1
        self.writeCurrentTag("letStatement", True) # write opening tag

        # write pre expression
        while True:
            break

        # write expression
        self.writeExpression()

        self.writeCurrentTag("letStatement", False) # write opening tag
        self.tabs -= 1
    def writeIfStatement(self):
        self.writeCurrentTag("ifStatement", True) # write opening tag
        self.tabs += 1

        # pre expression
        while True:
            break 

        # expression
        self.writeExpression()

        # post expressions
        while True:
            break

        # more statements
        self.writeStatements()

        self.tabs -= 1
        self.writeCurrentTag("ifStatement", False) # write opening tag


    def writeWhileStatement(self):
        # TODO: refactor if and while
        self.writeCurrentTag("whileStatement", True) # write opening tag
        self.tabs += 1

        # pre expression
        while True:
            break 

        # expression
        self.writeExpression()

        # post expressions
        while True:
            break

        # more statements
        self.writeStatements()

        self.tabs -= 1
        self.writeCurrentTag("whileStatement", False) # write opening tag

    def writeDoStatement(self):
        self.writeCurrentTag("doStatement", True) # write opening tag
        self.tabs += 1

        # pre expression

        # expression

        self.tabs -= 1
        self.writeCurrentTag("doStatement", True) # write opening tag

    def writeReturnStatement(self):
        self.writeCurrentTag("returnStatement", True) # write opening tag

        # parse until ";" is found

        self.writeCurrentTag("returnStatement", False) # write opening tag

    def writeExpression(self):
        self.writeCurrentTag("expression", True) # write opening tag
        self.tabs += 1

        # write term and symbols...
        while True:
            break

        self.tabs -= 1
        self.writeCurrentTag("expression", False) # write closing tag
        
    def writeExpressionList(self):
        self.writeCurrentTag("expressionList", True) # write opening tag
        self.tabs += 1

        while True:
            # write expression and symbols...
            break


        self.tabs -= 1
        self.writeCurrentTag("expressionList", False) # write closing tag

    def writeCurrentTag(self, tagName, open):
        '''
        Write the tagName to the output
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
        return self.triple
    
    def isEnd(self):
        '''
        If the self.triple has only one element after advancing, it is the end
        '''
        return len(self.triple) == 1

    def run(self):
        '''
        Run the wrapping function for each stage.
        '''
        
        # skip the line containing token tag, and load with the next token
        self.advance()

        
        # recursively call wrapping functions, starting from writeClass
        self.writeClass()

if __name__ == "__main__":
    engine = CompilerEngine(sys.argv[1])
    engine.run()