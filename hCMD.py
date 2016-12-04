#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN


class Parser():
    def __init__(self):
        self.cmd = ""
        self.reply = ""
        self.natural_input = ""
        self.files = ""
        self.options = ""

    def loadToken(self, fileName):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        dirPathTokens = os.path.join(dirPath, "tokens")
        with open(os.path.join(dirPathTokens, fileName)) as file:
            return '|'.join(file.read().split())

    def get(self):

        tokens = (
            'RUN',
            'CLOSE'
        )

        @TOKEN(self.loadToken("t_RUN"))
        def t_RUN(t):
            return t

        @TOKEN(self.loadToken("t_CLOSE"))
        def t_CLOSE(t):
            return t

        def t_error(t):
            t.lexer.skip(1)

        lexer = lex.lex()

        def p_exp(p):
            ' expression  : RUN '
            p[0] = {"command": "move", "natural_input": self.natural_input}

        def p_error(p):
            print("Nie rozumiem!")
            with open('.hCMD.log', 'w+') as file:
                file.write(self.natural_input)

        yacc.yacc()

        self.natural_input = input('> ').lower()
        if (yacc.parse(self.natural_input) is None):
            return {"command": "error"}
        else:
            return yacc.parse(self.natural_input)


while True:
    obj = Parser()
    print(obj.get())
