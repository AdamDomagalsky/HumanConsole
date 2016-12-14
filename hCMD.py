#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
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
        self.commands = 1
        self.cmd2 = ""
        self.kill = 0


    def loadToken(self, fileName):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        dirPathTokens = os.path.join(dirPath, "tokens")
        with open(os.path.join(dirPathTokens, fileName)) as file:
            return '|'.join(file.read().split())

    def get(self):

        tokens = (
            'RUN',
            'PROGRAM',
            'DOC',
            'HTML',
            'GOOGLE',
            'SPOJNIK',
            'CLOSE'
        )

        t_SPOJNIK = r'i|oraz|potem|następnie'
        t_HTML = r'(|www|https)\.?\w+\.(pl|cm)'
        t_DOC = r'\w+\.(txt|doc|docx|[tc]sv)'
        t_RUN = r'run|open|uruchom|otw[oó]rz|wykonaj|wejd[zźż]'
        t_GOOGLE = r'go{1,}gluj|wyszukaj|znajd[zżź]|wygo{1,}gluj|szukaj|go{1,}gle'

        @TOKEN(self.loadToken("t_PROGRAM"))
        def t_PROGRAM(t):
            return t

        @TOKEN(self.loadToken("t_CLOSE"))
        def t_CLOSE(t):
            return t

        def t_error(t):
            t.lexer.skip(1)

        lex.lex()

        def p_exp(p):
            ''' expression  : cmd source
                            | cmd program source
                            | program
                            | source
                            | expression spojnik expression '''
            print('p_exp')


        def p_cmd(p):
            ''' cmd : run
                    | close
                    '''

        def p_run(p):
            ' run : RUN '
            print('p_run')


        def p_close(p):
            ' close : CLOSE program '
            print('p_close')
            self.cmd = 'killall -9 '


        def p_spojnik(p):
            ' spojnik : SPOJNIK '
            self.commands+=1
            print('p_spojnik {0}'.format(self.commands))
            if self.cmd2 is "":
                self.cmd2 = ' '.join([self.cmd,self.files])
            else:
                self.cmd2 += self.cmd2 + ';' + ' '.join([self.cmd,self.files])

        def p_source(p):
            ''' source : doc
                        | html
                        | google
                        '''
            print(p[1])

        def p_google(p):
            ''' google : GOOGLE '''
            print('p_google')
            print(p[1])
            self.files = (self.natural_input.split(p[1])[1])[1:]
            self.files = 'google.com/search?q=' + self.files
            #print(self.files)
            self.cmd = 'sensible-browser'

            #self.files = 'google.com/search?q=' + ' '.join(self.natural_input.split()[1:])
            self.reply = 'Googluje hasło w google'

        def p_doc(p):
            ' doc : DOC '
            print('p_doc')
            self.cmd = 'vim'
            self.files = p[1]
            self.reply = 'Uruchamiam plik tekstowy'

        def p_html(p):
            ' html : HTML '
            print('p_html')
            self.cmd = 'sensible-browser'
            self.files = p[1]
            self.reply = 'Otwieram stronę internetową'

        def p_program(p):
            ''' program : PROGRAM
                        | PROGRAM source'''
            self.files = p[1]
            print('p_program')
            print(p[1])
            self.reply = 'Program zostanie za moment uruchomiony'

        def p_error(p):
            print("Nie rozumiem!")
            with open('.hCMD.log', 'a') as file:
                file.write(time.strftime("%d/%m %H:%M:%S") + "\tInput: " + self.natural_input + '\n')

        yacc.yacc()

        self.natural_input = input('> ').lower()
        yacc.parse(self.natural_input)

        if self.commands > 1:
            return ' ; '.join([self.cmd2,(' '.join([self.cmd,self.files]))])
        else:
            return ' '.join([self.cmd,self.files])




while True:
    obj = Parser()
    out = obj.get()
    print(out)

    #os.system(out)
