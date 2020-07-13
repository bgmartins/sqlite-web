#!/usr/bin/env python

import sys
sys.stdout.reconfigure(encoding='utf-8')
import datetime
import math
import operator
import optparse
import os
import re
import sys
import threading
import time
import webbrowser
import pandas as pd
import numpy as np
import json
from collections import namedtuple, OrderedDict
from functools import wraps
from getpass import getpass
from io import TextIOWrapper
import sqlite3

conn = None
try:
    conn = sqlite3.connect("../rep-database.db")
except Error as e:
    print(e)

c = conn.cursor()
c.execute('SELECT DISTINCT o.Nome, o.Acronimo, m.Numero, m.Ano, m.Mudanca_Estatuto FROM Mencoes_BTE_Org_Sindical m, Org_Sindical o WHERE m.Id_Organizacao_Sindical = o.ID AND o.Nome="SINDICATO NACIONAL DOS TRABALHADORES DO SECTOR DAS PESCAS"')
row = c.fetchone()
print(row)
name = row[0]
acronimo = row[1]

filename = "bte" + str(row[2]) + "_" + str(row[3]) + ".txt"
f = open("../BTE-data/" + filename, "r", encoding="utf-8")

f2 = open(name + "_" + filename, "a")
#colocar o tipo de evento (se é ou não mudança de estatuto)
if row[4] == 0:
	mudancaEstatuto = "FALSE"
else:
	mudancaEstatuto = "TRUE"

print("Mudanca_Estatuto:" + mudancaEstatuto)
f2.write("Mudanca_Estatuto:" + mudancaEstatuto)
f2.write("\n")
f2.write("\n")

#separar a escrita por antes, match e depois
for x in f:
	if name in x.upper():
		for match in re.finditer(name, x.upper()):
			print(x.upper()[match.start() - 200 : match.start()])
			print("\n")
			print(x.upper()[match.start() : match.end()])
			print("\n")
			print(x.upper()[match.end() : match.end() + 200])
			print("\n")
			f2.write(x.upper()[match.start() - 200 : match.start()])
			f2.write("\n")
			f2.write("\n")
			f2.write(x.upper()[match.start() : match.end()])
			f2.write("\n")
			f2.write("\n")
			f2.write(x.upper()[match.end() : match.end() + 200])
			f2.write("\n")
			f2.write("\n")

	if acronimo is not None:
		if acronimo in x.upper():
			for match in re.finditer(acronimo, x.upper()):
				print(x.upper()[match.start() - 200 : match.start()])
				print("\n")
				print(x.upper()[match.start() : match.end()])
				print("\n")
				print(x.upper()[match.end() : match.end() + 200])
				print("\n")
				f2.write(x.upper()[match.start() - 200 : match.start()])
				f2.write("\n")
				f2.write("\n")
				f2.write(x.upper()[match.start() : match.end()])
				f2.write("\n")
				f2.write("\n")
				f2.write(x.upper()[match.end() : match.end() + 200])
				f2.write("\n")
				f2.write("\n")

f.close()
f2.close()
	