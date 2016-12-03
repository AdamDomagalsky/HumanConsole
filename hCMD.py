#!/usr/bin/env python2

import os
import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN

class Parser():
	def __init__(selft):
		self.cmd=""
		self.reply=""
		self.natural_input =""
	