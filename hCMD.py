#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN
import time

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
            'CLOSE',
            'PROGRAM'
        )
      #     'DOC',
       #     'HTML',
        #    'PAGE',
         #   'PROGRAM'


      #  t_WEBPAGE = r'https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{4,}'
       # t_DOCFILE = r'.+\.\w{1,5}'
      #  t_PROGRAM = r'\w{2,}'

        @TOKEN(self.loadToken("t_RUN"))
        def t_RUN(t):
            return t

        @TOKEN(self.loadToken("t_CLOSE"))
        def t_CLOSE(t):
            return t

        def t_error(t):
            t.lexer.skip(1)

        lex.lex()

        def p_exp(p):
            ' expression  : cmd source '
            p[0] = {"command": "move", "natural_input": self.natural_input}

        def p_cmd(p):
            ''' cmd : run
                    | close '''

        def p_run(p):
            ' run : RUN '

        def p_close(p):
            ' close : CLOSE '

        def p_source(p):
            ' source : PROGRAM '



        def p_error(p):
            print("Nie rozumiem!")
            with open('.hCMD.log', 'a') as file:
                file.write(time.strftime("%d/%m %H:%M:%S") + "\tInput: " + self.natural_input + '\n')

        yacc.yacc()

        self.natural_input = input('> ').lower()
        out = yacc.parse(self.natural_input)
        if out:
            return out
        else:
            return 0


while True:
    obj = Parser()
    print(obj.get())

