#!/usr/bin/env python
import sys, os, re
import definitions

"""
This file is a script used to tokenize a .jack high level programming language
and outputs a tokenized file in xml format.

    possible tokens are;
        keyword: check
        symbol: 
        integerConstant
        StringConstant
        identifier
"""

def tokenize(content):
    # create a list of lines where; /** */ comment, // comment is removed, and stripped of whitespace
    lines = [line.strip() for line in re.sub('/\*.*?\*/', "", content, flags=re.DOTALL).split('\n')\
             if line and not line.startswith('//')] 

    # add the opening tag
    xml = ['<tokens>']

    # parse line -> word -> char 
    for line in lines:
        words = line.split()
        # remove the '//' in words
        if '//' in words:
            idx = words.index('//')
            words = words[:idx]
            
        for word in words:
            
            # if the word is in keywords
            if word in definitions.KEYWORDS:
                addToken(xml, word, 'keyword')
                continue

            chars = ""
            for c in word:
                if c in definitions.SYMBOLS: # if symbol is found in the word
                    if chars: # for characters found hereto
                        classifier = classify(chars) # classify the chars
                        addToken(xml, chars, classifier) # and add to the token list

                    addToken(xml, c, 'symbol')
                    chars = "" # flush the tokenized chars
                    continue
                    
                chars += c

            if chars: # for the remaining chars classify and tokenize 
                classifier = classify(chars)
                addToken(xml, chars, classifier)

    # Add closing tag and return
    xml.append('<tokens>')
    return "\n".join(xml)

def classify(chars):
    '''
    Classifies integerConstant, StringConstant, identifier,
    given string representation of the data. Only called when chars
    is not an empty string
    '''
    if chars in definitions.KEYWORDS:
        return "keyword"
    elif chars.isdigit():
        return "integerConstant"
    elif chars.startswith('"') and chars.endswith('"'):
        return "StringConstant"
    else: 
        return "identifier"

def addToken(xml, c, tokenType):
    '''
    Adds the opening tag, token and closing tag to the input list.
    '''
    xml.append(f"<{tokenType}>")
    xml.append(f"{c}")
    xml.append(f"</{tokenType}>")

def parsePath(path):
    '''
    Return a list of paths.
        if input path is filename: single file name will be included
        if it is directory: parse all the files and 
    '''
    if os.path.isdir(path):
        files = [os.path.join(path, file) for file in os.listdir(path) if ".jack" in file]
    else:
        files = [path]
    return files 

def main(path):
    files = parsePath(path)

    for file in files:
        with open(file, 'r') as inputFile:
            tokenizedXML = tokenize(inputFile.read())
            outputFile = os.path.basename(file)[:-len(".jack")] + "T.xml"
            with open(outputFile, 'w') as output:
                output.write(tokenizedXML)

if __name__ == "__main__":
    main(sys.argv[1])

