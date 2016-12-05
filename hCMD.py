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
            'PROGRAM',
            'DOC',
            'HTML',
            'GOOGLE'
        )

        t_HTML = r'((https?://|(w{3}?)|)\.?)\S+\.\w{1,4}\.?(\S+)'
        t_DOC = r'\w+\.(txt|doc|docx|[tc]sv)'
        t_RUN = r'run|open|uruchom|otw[oó]rz|wykonaj|wejd[zźż]'
        t_CLOSE = r'close|zamknij|wy[lł][aą]cz|zabij'
        t_GOOGLE = r'go{1,}gluj|wyszukaj|znajd[zżź]|wygo{1,}luj|szukaj'

        @TOKEN(self.loadToken("t_PROGRAM"))
        def t_PROGRAM(t):
            return t

        def t_error(t):
            t.lexer.skip(1)

        lex.lex()

        def p_exp(p):
            ''' expression  : cmd source
                            | html
                            | doc
                            | program
                            | google '''
            print('p_exp')

        def p_cmd(p):
            ''' cmd : run
                    | close
                    | google'''
            print('p_cmd')

        def p_run(p):
            ' run : RUN '
            print('p_run')

        def p_close(p):
            ' close : CLOSE '
            self.cmd='kill'
            print('p_close')

        def p_google(p):
            ' google : GOOGLE html'
            self.cmd = 'sensible-browser'
            self.files = 'google.com/search?q=' + self.files

        def p_source(p):
            ''' source : doc
                        | html
                        | program '''

        def p_doc(p):
            ' doc : DOC '
            print('p_doc')
            self.cmd='vim'
            self.files = p[1]

        def p_html(p):
            ' html : HTML '
            print('p_html')
            self.cmd='sensible-browser'
            self.files=p[1]

        def p_program(p):
            ' program : PROGRAM '
            print('p_program')

        def p_error(p):
            print("Nie rozumiem!")
            with open('.hCMD.log', 'a') as file:
                file.write(time.strftime("%d/%m %H:%M:%S") + "\tInput: " + self.natural_input + '\n')

        yacc.yacc()

        self.natural_input = input('> ').lower()
        yacc.parse(self.natural_input)
        return { 'cmd':self.cmd, 'file':self.files, 'input':self.natural_input }


while True:
    obj = Parser()
    out = obj.get()
    print(out)

