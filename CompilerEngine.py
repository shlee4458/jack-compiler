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
import sys, os
import re
import definitions

class CompilerEngine:
    
    def __init__(self, tokenFile):
        self.tokenFile = open(tokenFile, "r")
        self.outputFile = self.getOutputFile(tokenFile)
        self.line = self.tokenFile.readline()
        self.tabs = 0

    def getOutputFile(self, tokenFile):
        outputFile = os.path.basename(tokenFile)[:-len("T.xml")] + ".xml"
        return open(outputFile, "w")

    def writeClass(self):
        self.writeCurrentTag("class", True) # write opening tag
        self.writeClassVarDec() 
        self.writeSubRoutineDec() 
        self.writeCurrentTag("class", False) # write closing tag

    def writeClassVarDec(self):
        self.tabs += 1
        self.writeCurrentTag("classVarDec", True) # write opening tag
        self.tabs += 1
        
        # include all the tokens before the first ";"

        self.tabs -= 1
        self.writeCurrentTag("classVarDec", False) # write closing tag
        self.tabs -= 1

    def writeSubRoutineDec(self):
        self.tabs += 1
        self.writeCurrentTag("subroutineDec", True) # write opening tag
        self.tabs += 1

        # include all the tokens before paramList

        # write paramList
        self.writeParamList()

        # write subroutineBody
        self.writeSubRoutineBody()

        self.tabs -= 1
        self.writeCurrentTag("subroutineDec", False) # write closing tag
        self.tabs -= 1

    def writeParamList(self):
        self.writeCurrentTag("parameterList", True) # write opening tag
        self.tabs += 1

        # include all the list of tokens between paramList

        self.tabs -= 1
        self.writeCurrentTag("parameterList", False) # write closing tag

    def writeSubRoutineBody(self):
        self.writeCurrentTag("subroutineBody", True) # write opening tag
        self.tabs += 1

        # write statements
        self.writeStatements()

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
        tag = self.getTag(tagName, open, num)
        self.outputFile.write(tag)

    def getTag(self, tagName, open):
        '''
        Get the opened or closing tag.
        '''
        return f"<{tagName}>" if open else f"</{tagName}>"

    def close(self):
        '''
        Close open file for both writing and reading.
        '''
        self.tokenFile.close()
        self.outputFile.close()

    def run(self):
        '''
        Run the wrapping function for each stage.
        '''
        
        # skip the line containing token tag
        while re.match(r"<\/?token>", self.line): 
            self.line = self.tokenFile.readline()
        
        # recursively call wrapping functions, starting from writeClass
        self.writeClass()

            

if __name__ == "__main__":
    text = "<token>"

    # Find <token> and </token> using regex
    pattern = r"<\/?token>"
    matches = re.match(pattern, text)

    # Print the matches
    print(matches)