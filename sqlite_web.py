#!/usr/bin/env python

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
import rep_database
from collections import namedtuple, OrderedDict
from functools import wraps
from getpass import getpass
from io import TextIOWrapper
from io import BytesIO


# Py2k compat.
if sys.version_info[0] == 2:
    PY2 = True
    binary_types = (buffer, bytes, bytearray)
    decode_handler = 'replace'
    numeric = (int, long, float)
    unicode_type = unicode
    from StringIO import StringIO
else:
    PY2 = False
    binary_types = (bytes, bytearray)
    decode_handler = 'backslashreplace'
    numeric = (int, float)
    unicode_type = str
    from io import StringIO

try:
    from flask import (
        Flask, abort, escape, flash, jsonify, make_response, Markup, redirect,
        render_template, request, send_file, session, url_for)
except ImportError:
    raise RuntimeError('Unable to import flask module. Install by running '
                       'pip install flask')

try:
    from pygments import formatters, highlight, lexers
except ImportError:
    import warnings
    warnings.warn('pygments library not found.', ImportWarning)
    syntax_highlight = lambda data: '<pre>%s</pre>' % data
else:
    def syntax_highlight(data):
        if not data:
            return ''
        lexer = lexers.get_lexer_by_name('sql')
        formatter = formatters.HtmlFormatter(linenos=False)
        return highlight(data, lexer, formatter)

try:
    from peewee import __version__
    peewee_version = tuple([int(p) for p in __version__.split('.')])
except ImportError:
    raise RuntimeError('Unable to import peewee module. Install by running '
                       'pip install peewee')
else:
    if peewee_version <= (3, 0, 0):
        raise RuntimeError('Peewee >= 3.0.0 is required. Found version %s. '
                           'Please update by running pip install --update '
                           'peewee' % __version__)

from peewee import *
from peewee import IndexMetadata
from peewee import sqlite3
from playhouse.dataset import DataSet
from playhouse.migrate import migrate

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
DEBUG = False
MAX_RESULT_SIZE = 1000
ROWS_PER_PAGE = 50
SECRET_KEY = 'sqlite-database-browser-0.1.0'

app = Flask(
    __name__,
    static_folder=os.path.join(CUR_DIR, 'static'),
    template_folder=os.path.join(CUR_DIR, 'templates'))
app.config.from_object(__name__)
dataset = None
migrator = None

#
# Database metadata objects.
#

TriggerMetadata = namedtuple('TriggerMetadata', ('name', 'sql'))

ViewMetadata = namedtuple('ViewMetadata', ('name', 'sql'))

#
# Database helpers.
#

class SqliteDataSet(DataSet):
    @property
    def filename(self):
        db_file = dataset._database.database
        if db_file.startswith('file:'):
            db_file = db_file[5:]
        return os.path.realpath(db_file.rsplit('?', 1)[0])

    @property
    def is_readonly(self):
        db_file = dataset._database.database
        return db_file.endswith('?mode=ro')

    @property
    def base_name(self):
        return os.path.basename(self.filename)

    @property
    def created(self):
        stat = os.stat(self.filename)
        return datetime.datetime.fromtimestamp(stat.st_ctime)

    @property
    def modified(self):
        stat = os.stat(self.filename)
        return datetime.datetime.fromtimestamp(stat.st_mtime)

    @property
    def size_on_disk(self):
        stat = os.stat(self.filename)
        return stat.st_size


    #orgSindicaisAtivasPorTipoeAno

    @property
    def barchart_labels(self):
        cursor = self.query("SELECT ANO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Sindical, ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND ANO > 1996 GROUP BY ANO")
        return [row[0] for row in cursor.fetchall()]

    '''@property
    def barchart_data(self):
        cursor = self.query("SELECT ANO, COUNT(DISTINCT ID) FROM Org_Sindical, ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL ) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO ) AND ANO > 1996 GROUP BY ANO")
        return [row[1] for row in cursor.fetchall()]
    '''

    #confederacoes
    @property
    def barchart_data(self):
        cursor = self.query("SELECT ANO, TIPO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Sindical, ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND ANO > 1996 GROUP BY ANO, TIPO")
        lista = []

        for i in range(0,7):
            lista.append(0)

        for row in cursor.fetchall():
        	if row[1].startswith('CONF'):
        		lista.append(row[2])

        return lista

    #federacoes
    @property
    def barchart_data2(self):
        cursor = self.query("SELECT ANO, TIPO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Sindical, ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND ANO > 1996 GROUP BY ANO, TIPO")
        lista = []

        for i in range(0,7):
            lista.append(0)

        for row in cursor.fetchall():
        	if row[1].startswith('FED'):
        		lista.append(row[2])
        return lista


    #sindicatos
    @property
    def barchart_data3(self):
    	cursor = self.query("SELECT ANO, TIPO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Sindical, ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND ANO > 1996 GROUP BY ANO, TIPO")
    	return [row[2] for row in cursor.fetchall() if row[1].startswith('SIND') and row[0] >= 1977]

    #unioes
    @property
    def barchart_data4(self):
    	cursor = self.query("SELECT ANO, TIPO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Sindical, ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND ANO > 1996 GROUP BY ANO, TIPO")
    	lista = []

    	for i in range(0,7):
    		lista.append(0)

    	for row in cursor.fetchall():
    		if row[1].startswith('UNI'):
    			lista.append(row[2])

    	return lista

    #choroplethMapDistritos
    @property
    def map_labels(self):
        cursor = self.query("SELECT Distrito_Sede, COUNT(Distinct ID) as NUM_ORG FROM Org_Sindical WHERE Activa=1 GROUP BY Distrito_Sede")
        lista = []
        for row in cursor.fetchall():
            if(row[0]!="" and row[0]!="REG. AUT. AÇORES" and row[0]!="REG. AUT. MADEIRA"):
                lista.append(row[0])
        
        return lista

    #choroplethMap
    @property
    def map_data(self):
        cursor = self.query("SELECT Distrito_Sede, COUNT(Distinct ID) as NUM_ORG FROM Org_Sindical WHERE Activa=1 GROUP BY Distrito_Sede")
        lista = []
        for row in cursor.fetchall():
            if(row[0]!="" and row[0]!="REG. AUT. AÇORES" and row[0]!="REG. AUT. MADEIRA"):
                lista.append(row[1])
        
        return lista

    
    #avisosGreveAnos
    @property
    def barchart2_labels(self):
        cursor = self.query("SELECT Ano_Inicio as Ano, COUNT(*) as NUM_GREVES FROM Avisos_Greve WHERE ANO > 1996 GROUP BY Ano_Inicio")
        return [row[0] for row in cursor.fetchall()]


    #avisosGreve
    @property
    def barchart2_data(self):
        cursor = self.query("SELECT Ano_Inicio as Ano, COUNT(*) as NUM_GREVES FROM Avisos_Greve WHERE ANO > 1996 GROUP BY Ano_Inicio")
        return [row[1] for row in cursor.fetchall()]

    
    #orgSindicaisAtivasPorSector
    @property
    def barchart3_labels(self):
        cursor = self.query("SELECT Sectores_Profissionais.Sector, COUNT(DISTINCT Org_Sindical.ID) AS Num_Org FROM Sectores_Profissionais LEFT JOIN Org_Sindical ON Org_Sindical.Sector = Sectores_Profissionais.Sector GROUP BY Sectores_Profissionais.Sector ORDER BY Sectores_Profissionais.Sector")
        return [row[0] for row in cursor.fetchall()]

    @property
    def barchart3_labels_red(self):
        cursor = self.query("SELECT Sectores_Profissionais.Sector, Sectores_Profissionais.Nome_Abrev, COUNT(DISTINCT Org_Sindical.ID) AS Num_Org FROM Sectores_Profissionais LEFT JOIN Org_Sindical ON Org_Sindical.Sector = Sectores_Profissionais.Sector GROUP BY Sectores_Profissionais.Sector, Sectores_Profissionais.Nome_Abrev ORDER BY Sectores_Profissionais.Sector")
        return [row[1] for row in cursor.fetchall()]

    #sectores
    @property
    def barchart3_data(self):
        cursor = self.query("SELECT Sectores_Profissionais.Sector, COUNT(DISTINCT Org_Sindical.ID) AS Num_Org FROM Sectores_Profissionais LEFT JOIN Org_Sindical ON Org_Sindical.Sector = Sectores_Profissionais.Sector AND Activa = 1 GROUP BY Sectores_Profissionais.Sector ORDER BY Sectores_Profissionais.Sector")
        return [row[1] for row in cursor.fetchall()]


    #ircts por ano
    @property
    def irctchart_labels(self):
        cursor = self.query("SELECT Ano, COUNT(*) AS Num_IRCT FROM Actos_Negociacao_Colectiva WHERE ANO > 1996 GROUP BY Ano")
        return [row[0] for row in cursor.fetchall()]

    @property
    def irctchart_data(self):
        cursor = self.query("SELECT Ano, COUNT(*) AS Num_IRCT FROM Actos_Negociacao_Colectiva WHERE ANO > 1996 GROUP BY Ano")
        return [row[1] for row in cursor.fetchall()]

    @property
    def orgsindical1_data(self):
        lista = []
        cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Sindical")
        for row in cursor.fetchall():
            lista.append(list(row))

        for i in range(len(lista)):
            for j in range(len(lista[i])):
                if lista[i][j] is None:
                    lista[i][j] = ""
                elif lista[i][j] == 1:
                    lista[i][j] = "Ativa"
                elif lista[i][j] == 0:
                    lista[i][j] = "Inativa"

        return lista

    def orgsindical_data(self):
        lista = self.orgsindical1_data
        new_dict = {}
        
        for c, value in enumerate(lista):
            new_dict[str(c)] = value

        return new_dict


    def orgpatronal_data(self):
        lista = []
        new_dict = {}
        cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Patronal WHERE Tipo IS NOT NULL")
        
        for row in cursor.fetchall():
            lista.append(list(row))

        for i in range(len(lista)):
            for j in range(len(lista[i])):
                if lista[i][j] is None:
                    lista[i][j] = ""
                elif lista[i][j] == 1:
                    lista[i][j] = "Ativa"
                elif lista[i][j] == 0:
                    lista[i][j] = "Inativa"

        for c, value in enumerate(lista):
            new_dict[str(c)] = value

        return new_dict

    def searchbar_data(self, table, org):
        lista = []
        new_dict = {}

        if table=="Unions" or table=="":
            cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Sindical WHERE Nome LIKE ? OR Acronimo LIKE ?", ('%' + org + '%', '%' + org + '%'))
        else:
            cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Patronal WHERE Nome LIKE ? OR Acronimo LIKE ?", ('%' + org + '%', '%' + org + '%'))

        for row in cursor.fetchall():
            if row[0] is not None:
                lista.append(list(row))

        for i in range(len(lista)):
            for j in range(len(lista[i])):
                if lista[i][j] is None:
                    lista[i][j] = ""
                elif lista[i][j] == 1:
                    lista[i][j] = "Ativa"
                elif lista[i][j] == 0:
                    lista[i][j] = "Inativa"

        for c, value in enumerate(lista):
            new_dict[str(c)] = value

        return new_dict

    def searchbar_distrito_data(self, table, org, distrito):
        lista = []
        new_dict = {}

        if table=="Unions" or table=="":
            if org == "":
                cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Sindical WHERE Distrito_Sede LIKE ?", ('%' + distrito + '%',))
            else:
                cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Sindical WHERE (Nome LIKE ? OR Acronimo LIKE ?) AND Distrito_Sede LIKE ?", ('%' + org + '%', '%' + org + '%', '%' + distrito + '%'))
        else:
            if org == "":
                cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Patronal WHERE Distrito_Sede LIKE ?", ('%' + distrito + '%',))
            else:
                cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Patronal WHERE (Nome LIKE ? OR Acronimo LIKE ?) AND Distrito_Sede LIKE ?", ('%' + org + '%', '%' + org + '%', '%' + distrito + '%'))

        for row in cursor.fetchall():
            if row[0] is not None:
                lista.append(list(row))

        for i in range(len(lista)):
            for j in range(len(lista[i])):
                if lista[i][j] is None:
                    lista[i][j] = ""
                elif lista[i][j] == 1:
                    lista[i][j] = "Ativa"
                elif lista[i][j] == 0:
                    lista[i][j] = "Inativa"

        for c, value in enumerate(lista):
            new_dict[str(c)] = value

        return new_dict

    def searchbar_setor_data(self, table, org, setor):
        lista = []
        new_dict = {}

        if table=="Unions" or table=="":
            if org == "":
                cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Sindical WHERE Sector LIKE ?", ('%' + setor + '%',))
            else:
                cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Sindical WHERE (Nome LIKE ? OR Acronimo LIKE ?) AND Sector LIKE ?", ('%' + org + '%', '%' + org + '%', '%' + setor + '%'))
        else:
            if org == "":
                cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Patronal WHERE Sector LIKE ?", ('%' + setor + '%',))
            else:
                cursor = self.query("SELECT Tipo, Nome, Acronimo, Distrito_Sede, Sector, Activa FROM Org_Patronal WHERE (Nome LIKE ? OR Acronimo LIKE ?) AND Sector LIKE ?", ('%' + org + '%', '%' + org + '%', '%' + setor + '%'))

        for row in cursor.fetchall():
            if row[0] is not None:
                lista.append(list(row))

        for i in range(len(lista)):
            for j in range(len(lista[i])):
                if lista[i][j] is None:
                    lista[i][j] = ""
                elif lista[i][j] == 1:
                    lista[i][j] = "Ativa"
                elif lista[i][j] == 0:
                    lista[i][j] = "Inativa"

        for c, value in enumerate(lista):
            new_dict[str(c)] = value

        return new_dict

    def updateChart(self, table, org):
        lista_final = []

        lista_orgs_tipo_ano = self.orgs_tipo_ano(table, org)

        for lista_org_tipo_ano in lista_orgs_tipo_ano:
            lista_final.append(lista_org_tipo_ano)

        org_distritos = self.orgs_por_distrito(table, org)
        lista_greves = self.avisos_greve_ano(table, org)
        orgs_por_sector = self.orgs_por_sector(table, org)

        lista_final.append(org_distritos)
        lista_final.append(lista_greves)
        lista_final.append(orgs_por_sector)

        return lista_final


    def orgs_tipo_ano(self, table, org):
        lista_orgs = []
        orgs_tipo_ano_conf = {} #confederacao
        orgs_tipo_ano_fed = {} #federacao
        orgs_tipo_ano_org = {} #organizacao / associacao
        orgs_tipo_ano_uni = {} #uniao
        linhas = 0
        
        anos = self.barchart_labels

        for ano in anos:
            orgs_tipo_ano_conf[ano] = 0
            orgs_tipo_ano_fed[ano] = 0
            orgs_tipo_ano_org[ano] = 0
            orgs_tipo_ano_uni[ano] = 0


        if ((table=="Unions" or table=="") and org !=""):
            cursor = self.query("""SELECT ANO, TIPO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Sindical, 
            ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical 
            WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical 
            WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND 
            ID IN (SELECT ID FROM Org_Sindical WHERE Nome LIKE ? OR Acronimo LIKE ? AND Activa = 1 ) AND ANO > 1996 GROUP BY ANO, TIPO""",('%' + org + '%', '%' + org + '%'))
        
        elif ((table=="Unions" or table=="") and org==""):
            cursor = self.query("""SELECT ANO, TIPO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Sindical, 
            ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Sindical
             WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano
             FROM Org_Sindical WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND 
             (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND ANO > 1996 GROUP BY ANO, TIPO""")
        
        elif table=="Employees" and org!="":
            cursor = self.query("""SELECT ANO, TIPO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Patronal, 
            ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Patronal 
            WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano FROM Org_Patronal 
            WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND 
            ID IN (SELECT ID FROM Org_Patronal WHERE Nome LIKE ? OR Acronimo LIKE ? AND Activa = 1) AND TIPO IS NOT NULL AND ANO > 1996 GROUP BY ANO, TIPO""",('%' + org + '%', '%' + org + '%'))
        
        elif table=="Employees" and org=="":
            cursor = self.query("""SELECT ANO, TIPO, COUNT(DISTINCT ID) AS NUM_ORG FROM Org_Patronal, 
            ( SELECT DISTINCT CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) AS Ano FROM Org_Patronal
             WHERE Data_Primeira_Actividade IS NOT NULL AND Ano >= 1977 UNION SELECT DISTINCT CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) AS Ano
             FROM Org_Patronal WHERE Data_Primeira_Actividade IS NOT NULL) AS ANOS WHERE CAST(strftime('%Y',date(Data_Primeira_Actividade)) AS DECIMAL) <= ANO AND 
             (Activa = 1 OR CAST(strftime('%Y',date(Data_Ultima_Actividade)) AS DECIMAL) >= ANO) AND TIPO IS NOT NULL AND ANO > 1996 GROUP BY ANO, TIPO""")

        
        for row in cursor.fetchall():
            linhas = 1   
            if row[1].startswith("CONF"):
                orgs_tipo_ano_conf[row[0]] = row[2]
            
            elif row[1].startswith("FED"):
                orgs_tipo_ano_fed[row[0]] = row[2]
            
            elif row[1].startswith("SIND") or row[1].startswith("ASSO"):
                orgs_tipo_ano_org[row[0]] = row[2]
            
            elif row[1].startswith("UNI"):
                orgs_tipo_ano_uni[row[0]] = row[2]

        if linhas == 1:
            lista_orgs.append(list(orgs_tipo_ano_conf.values()))
            lista_orgs.append(list(orgs_tipo_ano_fed.values()))
            lista_orgs.append(list(orgs_tipo_ano_org.values()))
            lista_orgs.append(list(orgs_tipo_ano_uni.values()))
        else:
            lista_orgs = [[] for _ in range(4)]

        return lista_orgs


    def orgs_por_distrito(self, table, org):
        distritos = self.map_labels
        linhas = 0
        org_distritos = {}

        for distrito in distritos:
            org_distritos[distrito] = 0


        if ((table=="Unions" or table=="") and org!=""):
            cursor = self.query("SELECT Distrito_Sede, COUNT(Distinct ID) as NUM_ORG FROM Org_Sindical WHERE ID IN (SELECT ID FROM Org_Sindical WHERE Nome LIKE ? OR Acronimo LIKE ?) AND Activa=1 GROUP BY Distrito_Sede",('%' + org + '%', '%' + org + '%'))
        
        elif ((table=="Unions" or table=="") and org==""):
            cursor = self.query("SELECT Distrito_Sede, COUNT(Distinct ID) as NUM_ORG FROM Org_Sindical WHERE Activa=1 GROUP BY Distrito_Sede")
        
        elif table=="Employees" and org!="":
            cursor = self.query("SELECT Distrito_Sede, COUNT(Distinct ID) as NUM_ORG FROM Org_Patronal WHERE ID IN (SELECT ID FROM Org_Patronal WHERE Nome LIKE ? OR Acronimo LIKE ?) AND Activa=1 GROUP BY Distrito_Sede",('%' + org + '%', '%' + org + '%'))

        elif table=="Employees" and org=="":
            cursor = self.query("SELECT Distrito_Sede, COUNT(Distinct ID) as NUM_ORG FROM Org_Patronal WHERE Activa=1 GROUP BY Distrito_Sede")

        for row in cursor.fetchall():
            linhas = 1
            if(row[0]!="" and row[0]!="REG. AUT. AÇORES" and row[0]!="REG. AUT. MADEIRA"):
                org_distritos[row[0]] = row[1]


        if linhas == 1:
            return list(org_distritos.values())
        else:
            return []


    def avisos_greve_ano(self, table, org):
        anos_greve = self.barchart2_labels
        avisos_greve = {}
        linhas = 0
        
        for ano in anos_greve:
            avisos_greve[ano] = 0

        if ((table == "Unions" or table=="") and org!=""):
            cursor = self.query("SELECT Ano_Inicio as Ano, COUNT(*) as NUM_GREVES FROM Avisos_Greve WHERE Entidade_Sindical IN (SELECT Nome FROM Org_Sindical WHERE Nome LIKE ? OR Acronimo LIKE ? AND Activa = 1) AND ANO > 1996 GROUP BY Ano_Inicio",('%' + org + '%', '%' + org + '%'))
        
        elif ((table=="Unions" or table=="") and org==""):
            cursor = self.query("SELECT Ano_Inicio as Ano, COUNT(*) as NUM_GREVES FROM Avisos_Greve WHERE ANO > 1996 GROUP BY Ano_Inicio")
        
        elif table=="Employees" and org!="":
            cursor = self.query("SELECT Ano_Inicio as Ano, COUNT(*) as NUM_GREVES FROM Avisos_Greve WHERE Entidade_Patronal IN (SELECT Nome FROM Org_Patronal WHERE Nome LIKE ? OR Acronimo LIKE ? AND Activa = 1) AND ANO > 1996 GROUP BY Ano_Inicio",('%' + org + '%', '%' + org + '%'))

        elif table=="Employees" and org=="":
            cursor = self.query("SELECT Ano_Inicio as Ano, COUNT(*) as NUM_GREVES FROM Avisos_Greve WHERE ANO > 1996 GROUP BY Ano_Inicio")

        
        for row in cursor.fetchall():
            linhas = 1
            avisos_greve[row[0]] = row[1]


        if linhas == 1:
            return list(avisos_greve.values())
        else:
            return []

    def orgs_por_sector(self, table, org):
        sectores = self.barchart3_labels
        orgs_por_sector = {}
        linhas = 0

        for sector in sectores:
            orgs_por_sector[sector] = 0

        if ((table == "Unions" or table=="") and org!=""):
            cursor = self.query("""SELECT Sectores_Profissionais.Sector, COUNT(DISTINCT Org_Sindical.ID) AS Num_Org 
                FROM Sectores_Profissionais LEFT JOIN Org_Sindical ON Org_Sindical.Sector = Sectores_Profissionais.Sector WHERE Org_Sindical.ID IN 
             (SELECT ID FROM Org_Sindical WHERE Nome LIKE ? OR Acronimo LIKE ? AND Activa = 1) 
             GROUP BY Sectores_Profissionais.Sector ORDER BY Sectores_Profissionais.Sector""",('%' + org + '%', '%' + org + '%'))

        elif ((table == "Unions" or table=="") and org==""):
            cursor = self.query("""SELECT Sectores_Profissionais.Sector, COUNT(DISTINCT Org_Sindical.ID) AS Num_Org 
                FROM Sectores_Profissionais LEFT JOIN Org_Sindical ON Org_Sindical.Sector = Sectores_Profissionais.Sector 
                AND Activa = 1 GROUP BY Sectores_Profissionais.Sector ORDER BY Sectores_Profissionais.Sector""")
        
        elif table=="Employees" and org!="":
            cursor = self.query("""SELECT Sectores_Profissionais.Sector, COUNT(DISTINCT Org_Patronal.ID) AS Num_Org 
                FROM Sectores_Profissionais LEFT JOIN Org_Patronal ON Org_Patronal.Sector = Sectores_Profissionais.Sector WHERE Org_Patronal.ID IN 
                (SELECT ID FROM Org_Patronal WHERE Nome LIKE ? OR Acronimo LIKE ? AND Activa = 1)
                 GROUP BY Sectores_Profissionais.Sector ORDER BY Sectores_Profissionais.Sector""",('%' + org + '%', '%' + org + '%'))

        elif table=="Employees" and org=="":
            cursor = self.query("""SELECT Sectores_Profissionais.Sector, COUNT(DISTINCT Org_Patronal.ID) AS Num_Org 
                FROM Sectores_Profissionais LEFT JOIN Org_Patronal ON Org_Patronal.Sector = Sectores_Profissionais.Sector AND Activa = 1
                GROUP BY Sectores_Profissionais.Sector ORDER BY Sectores_Profissionais.Sector""")

        for row in cursor.fetchall():
            linhas = 1
            orgs_por_sector[row[0]] = row[1]

        if linhas == 1:
            return list(orgs_por_sector.values())
        else:
            return []
    

    def table_toExcel(self, table, org, setor, distrito):
        registos = []
        colunas = []
        linhas = []
        
        if ((table == "Unions" or table=="") and org!=""):
            table = 'Org_Sindical'
            if setor != "":
                cursor = self.query("SELECT * FROM Org_Sindical WHERE (Nome LIKE ? OR Acronimo LIKE ?) AND Sector LIKE ?", ('%' + org + '%', '%' + org + '%', '%' + setor + '%'))
            elif distrito != "":
                cursor = self.query("SELECT * FROM Org_Sindical WHERE (Nome LIKE ? OR Acronimo LIKE ?) AND Distrito_Sede LIKE ?", ('%' + org + '%', '%' + org + '%', '%' + distrito + '%'))
            else:
                cursor = self.query("SELECT * FROM Org_Sindical WHERE Nome LIKE ? OR Acronimo LIKE ?", ('%' + org + '%', '%' + org + '%'))
        
        elif ((table == "Unions" or table=="") and org==""):
            table = 'Org_Sindical'
            if setor != "":
                cursor = self.query("SELECT * FROM Org_Sindical WHERE Sector LIKE ?", ('%' + setor + '%'))
            elif distrito != "":
                cursor = self.query("SELECT * FROM Org_Sindical WHERE Distrito_Sede LIKE ?", ('%' + distrito + '%'))
            else:
                cursor = self.query("SELECT * FROM Org_Sindical")

        elif table=="Employees" and org!="":
            table = 'Org_Patronal'
            if setor != "":
                cursor = self.query("SELECT * FROM Org_Patronal WHERE (Nome LIKE ? OR Acronimo LIKE ?) AND Sector LIKE ?", ('%' + org + '%', '%' + org + '%', '%' + setor + '%'))
            elif distrito != "":
                cursor = self.query("SELECT * FROM Org_Patronal WHERE (Nome LIKE ? OR Acronimo LIKE ?) AND Distrito_Sede LIKE ?", ('%' + org + '%', '%' + org + '%', '%' + distrito + '%'))
            else:
                cursor = self.query("SELECT * FROM Org_Patronal WHERE Nome LIKE ? OR Acronimo LIKE ?", ('%' + org + '%', '%' + org + '%'))

        elif table=="Employees" and org=="": 
            table = 'Org_Patronal'
            if setor != "":
                cursor = self.query("SELECT * FROM Org_Patronal WHERE Sector LIKE ?", ('%' + setor + '%'))
            elif distrito != "":
                cursor = self.query("SELECT * FROM Org_Patronal WHERE Distrito_Sede LIKE ?", ('%' + distrito + '%'))
            else:
                cursor = self.query("SELECT * FROM Org_Patronal")

        for tuplo in self.get_columns(table):
            cols = list(tuplo)
            if cols[0] == "Activa":
                cols[0] = "Estado"
            elif cols[0] == "Sector":
                cols[0] = "Setor"
            elif cols[0] == "Acronimo":
                cols[0] = "Acrónimo"

            colunas.append(cols[0])

        print(colunas[18])

        for row in cursor.fetchall():
            linhas.append(list(row))

        # 18 é a coluna do Estado
        for i in range(len(linhas)):
            for j in range(len(linhas[i])):
                if j == 18:
                    if linhas[i][j] is None:
                        linhas[i][j] = ""
                    elif linhas[i][j] == 1:
                        linhas[i][j] = "Ativa"
                    elif linhas[i][j] == 0:
                        linhas[i][j] = "Inativa"
        
        return pd.DataFrame(linhas, columns=colunas)

    def get_indexes(self, table):
        return dataset._database.get_indexes(table)

    def get_all_indexes(self):
        cursor = self.query(
            'SELECT name, sql FROM sqlite_master '
            'WHERE type = ? ORDER BY name',
            ('index',))
        return [IndexMetadata(row[0], row[1], None, None, None)
                for row in cursor.fetchall()]

    def get_columns(self, table):
        return dataset._database.get_columns(table)

    def get_foreign_keys(self, table):
        return dataset._database.get_foreign_keys(table)

    def get_triggers(self, table):
        cursor = self.query(
            'SELECT name, sql FROM sqlite_master '
            'WHERE type = ? AND tbl_name = ?',
            ('trigger', table))
        return [TriggerMetadata(*row) for row in cursor.fetchall()]

    def get_all_triggers(self):
        cursor = self.query(
            'SELECT name, sql FROM sqlite_master '
            'WHERE type = ? ORDER BY name',
            ('trigger',))
        return [TriggerMetadata(*row) for row in cursor.fetchall()]

    def get_all_views(self):
        cursor = self.query(
            'SELECT name, sql FROM sqlite_master '
            'WHERE type = ? ORDER BY name',
            ('view',))
        return [ViewMetadata(*row) for row in cursor.fetchall()]

    def get_virtual_tables(self):
        cursor = self.query(
            'SELECT name FROM sqlite_master '
            'WHERE type = ? AND sql LIKE ? '
            'ORDER BY name',
            ('table', 'CREATE VIRTUAL TABLE%'))
        return set([row[0] for row in cursor.fetchall()])

    def get_corollary_virtual_tables(self):
        virtual_tables = self.get_virtual_tables()
        suffixes = ['content', 'docsize', 'segdir', 'segments', 'stat']
        return set(
            '%s_%s' % (virtual_table, suffix) for suffix in suffixes
            for virtual_table in virtual_tables)

#
# Flask views.
#
@app.route('/')
def welcome_page():
    return render_template('welcome_page.html', sqlite=sqlite3)


@app.route('/admin-panel/', methods=['GET'])
def admin_panel():
    return render_template('admin_panel.html', sqlite=sqlite3)



@app.route('/export/', methods=['GET'])
def export():
    table = request.args.get('table_org')
    org = request.args.get('organization')
    export = request.args.get('export')
    setor = request.args.get('setor')
    distrito = request.args.get('distrito')

    df = dataset.table_toExcel(table, org, setor, distrito)
    strIO = BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="sheet1", index=False)
    excel_writer.save()
    excel_data = strIO.getvalue()
    strIO.seek(0)

    return send_file(strIO,
             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
             attachment_filename='output.xlsx',
             as_attachment=True)


@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():  
    if request.method == 'POST':
        if request.form.get('password') == app.config['PASSWORD']:
            session['authorized'] = True
            return redirect(url_for('admin_panel'))
        flash('The password you entered is incorrect.', 'danger')
        return render_template('welcome_page.html')
    return render_template('dashboard.html')


@app.route('/logout/', methods=['GET'])
def logout():
    session.pop('authorized', None)
    return redirect(url_for('welcome_page'))

def require_table(fn):
    @wraps(fn)
    def inner(table, *args, **kwargs):
        if table not in dataset.tables:
            abort(404)
        return fn(table, *args, **kwargs)
    return inner

@app.route('/search/', methods=['GET'])
def search():
    table = request.args.get('table_org')
    org = request.args.get('organization')
    distrito  = request.args.get('distrito')
    setor = request.args.get('setor')

    if distrito != "":
        return jsonify(tabela = dataset.searchbar_distrito_data(table, org, distrito))
    
    if setor != "":
        return jsonify(tabela = dataset.searchbar_setor_data(table, org, setor))

    if org != "":
        return jsonify(tabela = dataset.searchbar_data(table, org))
    elif org == "" and table == "Unions":
        return jsonify(tabela = dataset.orgsindical_data())
    elif org == "" and table == "Employees":
        return jsonify(tabela = dataset.orgpatronal_data())
    else:
        return jsonify(tabela = dataset.orgsindical_data())

@app.route('/updateDB/', methods=['GET'])
def updateDB():
    return rep_database.repDatabase()

@app.route('/updateCharts/', methods=['GET'])
def updateCharts():
    table = request.args.get('table_org')
    org = request.args.get('organization')

    return jsonify(tabela = dataset.updateChart(table,org))


@app.route('/create-table/', methods=['POST'])
def table_create():
    table = (request.form.get('table_name') or '').strip()
    if not table:
        flash('Table name is required.', 'danger')
        return redirect(request.form.get('redirect') or url_for('index'))

    dataset[table]
    return redirect(url_for('table_import', table=table))

@app.route('/<table>/')
@require_table
def table_structure(table):
    ds_table = dataset[table]
    model_class = ds_table.model_class

    table_sql = dataset.query(
        'SELECT sql FROM sqlite_master WHERE tbl_name = ? AND type = ?',
        [table, 'table']).fetchone()[0]

    return render_template(
        'table_structure.html',
        columns=dataset.get_columns(table),
        ds_table=ds_table,
        foreign_keys=dataset.get_foreign_keys(table),
        indexes=dataset.get_indexes(table),
        model_class=model_class,
        table=table,
        table_sql=table_sql,
        triggers=dataset.get_triggers(table))

def get_request_data():
    if request.method == 'POST':
        return request.form
    return request.args

@app.route('/<table>/add-column/', methods=['GET', 'POST'])
@require_table
def add_column(table):
    column_mapping = OrderedDict((
        ('VARCHAR', CharField),
        ('TEXT', TextField),
        ('INTEGER', IntegerField),
        ('REAL', FloatField),
        ('BOOL', BooleanField),
        ('BLOB', BlobField),
        ('DATETIME', DateTimeField),
        ('DATE', DateField),
        ('TIME', TimeField),
        ('DECIMAL', DecimalField)))

    request_data = get_request_data()
    col_type = request_data.get('type')
    name = request_data.get('name', '')

    if request.method == 'POST':
        if name and col_type in column_mapping:
            migrate(
                migrator.add_column(
                    table,
                    name,
                    column_mapping[col_type](null=True)))
            flash('Column "%s" was added successfully!' % name, 'success')
            dataset.update_cache(table)
            return redirect(url_for('table_structure', table=table))
        else:
            flash('Name and column type are required.', 'danger')

    return render_template(
        'add_column.html',
        col_type=col_type,
        column_mapping=column_mapping,
        name=name,
        table=table)

@app.route('/<table>/drop-column/', methods=['GET', 'POST'])
@require_table
def drop_column(table):
    request_data = get_request_data()
    name = request_data.get('name', '')
    columns = dataset.get_columns(table)
    column_names = [column.name for column in columns]

    if request.method == 'POST':
        if name in column_names:
            migrate(migrator.drop_column(table, name))
            flash('Column "%s" was dropped successfully!' % name, 'success')
            dataset.update_cache(table)
            return redirect(url_for('table_structure', table=table))
        else:
            flash('Name is required.', 'danger')

    return render_template(
        'drop_column.html',
        columns=columns,
        column_names=column_names,
        name=name,
        table=table)

@app.route('/<table>/rename-column/', methods=['GET', 'POST'])
@require_table
def rename_column(table):
    request_data = get_request_data()
    rename = request_data.get('rename', '')
    rename_to = request_data.get('rename_to', '')

    columns = dataset.get_columns(table)
    column_names = [column.name for column in columns]

    if request.method == 'POST':
        if (rename in column_names) and (rename_to not in column_names):
            migrate(migrator.rename_column(table, rename, rename_to))
            flash('Column "%s" was renamed successfully!' % rename, 'success')
            dataset.update_cache(table)
            return redirect(url_for('table_structure', table=table))
        else:
            flash('Column name is required and cannot conflict with an '
                  'existing column\'s name.', 'danger')

    return render_template(
        'rename_column.html',
        columns=columns,
        column_names=column_names,
        rename=rename,
        rename_to=rename_to,
        table=table)

@app.route('/<table>/add-index/', methods=['GET', 'POST'])
@require_table
def add_index(table):
    request_data = get_request_data()
    indexed_columns = request_data.getlist('indexed_columns')
    unique = bool(request_data.get('unique'))

    columns = dataset.get_columns(table)

    if request.method == 'POST':
        if indexed_columns:
            migrate(
                migrator.add_index(
                    table,
                    indexed_columns,
                    unique))
            flash('Index created successfully.', 'success')
            return redirect(url_for('table_structure', table=table))
        else:
            flash('One or more columns must be selected.', 'danger')

    return render_template(
        'add_index.html',
        columns=columns,
        indexed_columns=indexed_columns,
        table=table,
        unique=unique)

@app.route('/<table>/drop-index/', methods=['GET', 'POST'])
@require_table
def drop_index(table):
    request_data = get_request_data()
    name = request_data.get('name', '')
    indexes = dataset.get_indexes(table)
    index_names = [index.name for index in indexes]

    if request.method == 'POST':
        if name in index_names:
            migrate(migrator.drop_index(table, name))
            flash('Index "%s" was dropped successfully!' % name, 'success')
            return redirect(url_for('table_structure', table=table))
        else:
            flash('Index name is required.', 'danger')

    return render_template(
        'drop_index.html',
        indexes=indexes,
        index_names=index_names,
        name=name,
        table=table)

@app.route('/<table>/drop-trigger/', methods=['GET', 'POST'])
@require_table
def drop_trigger(table):
    request_data = get_request_data()
    name = request_data.get('name', '')
    triggers = dataset.get_triggers(table)
    trigger_names = [trigger.name for trigger in triggers]

    if request.method == 'POST':
        if name in trigger_names:
            dataset.query('DROP TRIGGER "%s";' % name)
            flash('Trigger "%s" was dropped successfully!' % name, 'success')
            return redirect(url_for('table_structure', table=table))
        else:
            flash('Trigger name is required.', 'danger')

    return render_template(
        'drop_trigger.html',
        triggers=triggers,
        trigger_names=trigger_names,
        name=name,
        table=table)

@app.route('/<table>/content/')
@require_table
def table_content(table):
    page_number = request.args.get('page') or ''
    page_number = int(page_number) if page_number.isdigit() else 1

    dataset.update_cache(table)
    ds_table = dataset[table]
    total_rows = ds_table.all().count()
    rows_per_page = app.config['ROWS_PER_PAGE']
    total_pages = int(math.ceil(total_rows / float(rows_per_page)))
    # Restrict bounds.
    page_number = min(page_number, total_pages)
    page_number = max(page_number, 1)

    previous_page = page_number - 1 if page_number > 1 else None
    next_page = page_number + 1 if page_number < total_pages else None

    query = ds_table.all().paginate(page_number, rows_per_page)

    ordering = request.args.get('ordering')
    if ordering:
        field = ds_table.model_class._meta.columns[ordering.lstrip('-')]
        if ordering.startswith('-'):
            field = field.desc()
        query = query.order_by(field)

    field_names = ds_table.columns
    columns = [f.column_name for f in ds_table.model_class._meta.sorted_fields]

    table_sql = dataset.query(
        'SELECT sql FROM sqlite_master WHERE tbl_name = ? AND type = ?',
        [table, 'table']).fetchone()[0]

    return render_template(
        'table_content.html',
        columns=columns,
        ds_table=ds_table,
        field_names=field_names,
        next_page=next_page,
        ordering=ordering,
        page=page_number,
        previous_page=previous_page,
        query=query,
        table=table,
        total_pages=total_pages,
        total_rows=total_rows)

@app.route('/<table>/query/', methods=['GET', 'POST'])
@require_table
def table_query(table):
    data = []
    data_description = error = row_count = sql = None

    if request.method == 'POST':
        sql = request.form['sql']
        if 'export_json' in request.form:
            return export(table, sql, 'json')
        elif 'export_csv' in request.form:
            return export(table, sql, 'csv')

        try:
            cursor = dataset.query(sql)
        except Exception as exc:
            error = str(exc)
        else:
            data = cursor.fetchall()[:app.config['MAX_RESULT_SIZE']]
            data_description = cursor.description
            row_count = cursor.rowcount
    else:
        if request.args.get('sql'):
            sql = request.args.get('sql')
        else:
            sql = 'SELECT *\nFROM "%s"' % (table)

    table_sql = dataset.query(
        'SELECT sql FROM sqlite_master WHERE tbl_name = ? AND type = ?',
        [table, 'table']).fetchone()[0]

    return render_template(
        'table_query.html',
        data=data,
        data_description=data_description,
        error=error,
        query_images=get_query_images(),
        row_count=row_count,
        sql=sql,
        table=table,
        table_sql=table_sql)

@app.route('/table-definition/', methods=['POST'])
def set_table_definition_preference():
    key = 'show'
    show = False
    if request.form.get(key) and request.form.get(key) != 'false':
        session[key] = show = True
    elif key in session:
        del session[key]
    return jsonify({key: show})

def export(table, sql, export_format):
    model_class = dataset[table].model_class
    query = model_class.raw(sql).dicts()
    buf = StringIO()
    if export_format == 'json':
        kwargs = {'indent': 2}
        filename = '%s-export.json' % table
        mimetype = 'text/javascript'
    else:
        kwargs = {}
        filename = '%s-export.csv' % table
        mimetype = 'text/csv'

    dataset.freeze(query, export_format, file_obj=buf, **kwargs)

    response_data = buf.getvalue()
    response = make_response(response_data)
    response.headers['Content-Length'] = len(response_data)
    response.headers['Content-Type'] = mimetype
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % (
        filename)
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'public'
    return response

@app.route('/<table>/import/', methods=['GET', 'POST'])
@require_table
def table_import(table):
    count = None
    request_data = get_request_data()
    strict = bool(request_data.get('strict'))

    if request.method == 'POST':
        file_obj = request.files.get('file')
        if not file_obj:
            flash('Please select an import file.', 'danger')
        elif not file_obj.filename.lower().endswith(('.csv', '.json')):
            flash('Unsupported file-type. Must be a .json or .csv file.',
                  'danger')
        else:
            if file_obj.filename.lower().endswith('.json'):
                format = 'json'
            else:
                format = 'csv'

            # Here we need to translate the file stream. Werkzeug uses a
            # spooled temporary file opened in wb+ mode, which is not
            # compatible with Python's CSV module. We'd need to reach pretty
            # far into Flask's internals to modify this behavior, so instead
            # we'll just translate the stream into utf8-decoded unicode.
            if not PY2:
                try:
                    stream = TextIOWrapper(file_obj, encoding='utf8')
                except AttributeError:
                    # The SpooledTemporaryFile used by werkzeug does not
                    # implement an API that the TextIOWrapper expects, so we'll
                    # just consume the whole damn thing and decode it.
                    # Fixed in werkzeug 0.15.
                    stream = StringIO(file_obj.read().decode('utf8'))
            else:
                stream = file_obj.stream

            try:
                with dataset.transaction():
                    count = dataset.thaw(
                        table,
                        format=format,
                        file_obj=stream,
                        strict=strict)
            except Exception as exc:
                flash('Error importing file: %s' % exc, 'danger')
            else:
                flash(
                    'Successfully imported %s objects from %s.' % (
                        count, file_obj.filename),
                    'success')
                return redirect(url_for('table_content', table=table))

    return render_template(
        'table_import.html',
        count=count,
        strict=strict,
        table=table)

@app.route('/<table>/drop/', methods=['GET', 'POST'])
@require_table
def drop_table(table):
    if request.method == 'POST':
        model_class = dataset[table].model_class
        model_class.drop_table()
        dataset.update_cache()  # Update all tables.
        flash('Table "%s" dropped successfully.' % table, 'success')
        return redirect(url_for('index'))

    return render_template('drop_table.html', table=table)

@app.template_filter('format_index')
def format_index(index_sql):
    split_regex = re.compile(r'\bon\b', re.I)
    if not split_regex.search(index_sql):
        return index_sql

    create, definition = split_regex.split(index_sql)
    return '\nON '.join((create.strip(), definition.strip()))

@app.template_filter('value_filter')
def value_filter(value, max_length=50):
    if isinstance(value, numeric):
        return value

    if isinstance(value, binary_types):
        if not isinstance(value, (bytes, bytearray)):
            value = bytes(value)  # Handle `buffer` type.
        value = value.decode('utf-8', decode_handler)
    if isinstance(value, unicode_type):
        value = escape(value)
        if len(value) > max_length:
            return ('<span class="truncated">%s</span> '
                    '<span class="full" style="display:none;">%s</span>'
                    '<a class="toggle-value" href="#">...</a>') % (
                        value[:max_length],
                        value)
    return value

column_re = re.compile('(.+?)\((.+)\)', re.S)
column_split_re = re.compile(r'(?:[^,(]|\([^)]*\))+')

def _format_create_table(sql):
    create_table, column_list = column_re.search(sql).groups()
    columns = ['  %s' % column.strip()
               for column in column_split_re.findall(column_list)
               if column.strip()]
    return '%s (\n%s\n)' % (
        create_table,
        ',\n'.join(columns))

@app.template_filter()
def format_create_table(sql):
    try:
        return _format_create_table(sql)
    except:
        return sql

@app.template_filter('highlight')
def highlight_filter(data):
    return Markup(syntax_highlight(data))

def get_query_images():
    accum = []
    image_dir = os.path.join(app.static_folder, 'img')
    if not os.path.exists(image_dir):
        return accum
    for filename in sorted(os.listdir(image_dir)):
        basename = os.path.splitext(os.path.basename(filename))[0]
        parts = basename.split('-')
        accum.append((parts, 'img/' + filename))
    return accum

#
# Flask application helpers.
#

@app.context_processor
def _general():
    return {
        'dataset': dataset,
        'login_required': bool(app.config.get('PASSWORD')),
    }

@app.context_processor
def _now():
    return {'now': datetime.datetime.now()}

@app.before_request
def _connect_db():
    dataset.connect()

@app.teardown_request
def _close_db(exc):
    if not dataset._database.is_closed():
        dataset.close()


class PrefixMiddleware(object):
    def __init__(self, app, prefix):
        self.app = app
        self.prefix = '/%s' % prefix.strip('/')
        self.prefix_len = len(self.prefix)

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][self.prefix_len:]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ['URL does not match application prefix.'.encode()]

#
# Script options.
#

def get_option_parser():
    parser = optparse.OptionParser()
    parser.add_option(
        '-p',
        '--port',
        default=8080,
        help='Port for web interface, default=8080',
        type='int')
    parser.add_option(
        '-H',
        '--host',
        default='127.0.0.1',
        help='Host for web interface, default=127.0.0.1')
    parser.add_option(
        '-d',
        '--debug',
        action='store_true',
        help='Run server in debug mode')
    parser.add_option(
        '-x',
        '--no-browser',
        action='store_false',
        default=True,
        dest='browser',
        help='Do not automatically open browser page.')
    parser.add_option(
        '-P',
        '--password',
        action='store_true',
        dest='prompt_password',
        help='Prompt for password to access database browser.')
    parser.add_option(
        '-r',
        '--read-only',
        action='store_true',
        dest='read_only',
        help='Open database in read-only mode.')
    parser.add_option(
        '-u',
        '--url-prefix',
        dest='url_prefix',
        help='URL prefix for application.')
    return parser

def die(msg, exit_code=1):
    sys.stderr.write('%s\n' % msg)
    sys.stderr.flush()
    sys.exit(exit_code)

def open_browser_tab(host, port):
    url = 'http://%s:%s/' % (host, port)

    def _open_tab(url):
        time.sleep(1.5)
        webbrowser.open_new_tab(url)

    thread = threading.Thread(target=_open_tab, args=(url,))
    thread.daemon = True
    thread.start()

def install_auth_handler(password):
    app.config['PASSWORD'] = password

    '''@app.before_request
    def check_password():

        if not session.get('authorized') and request.path != '/dashboard/' and request.path != '/export/' and request.path != '/search/' and request.path != '/updateCharts/' and \
           not request.path.startswith(('/static/', '/favicon')):
            flash('You must log-in to view the database browser.', 'danger')
            session['next_url'] = request.base_url
            return redirect(url_for('dashboard'))'''

def initialize_app(filename, read_only=False, password=None, url_prefix=None):
    global dataset
    global migrator
    
    if password:
        install_auth_handler(password)

    if read_only:
        if sys.version_info < (3, 4, 0):
            die('Python 3.4.0 or newer is required for read-only access.')
        if peewee_version < (3, 5, 1):
            die('Peewee 3.5.1 or newer is required for read-only access.')
        db = SqliteDatabase('file:%s?mode=ro' % filename, uri=True)
        try:
            db.connect()
        except OperationalError:
            die('Unable to open database file in read-only mode. Ensure that '
                'the database exists in order to use read-only mode.')
        db.close()
        dataset = SqliteDataSet(db, bare_fields=True)
    else:
        dataset = SqliteDataSet('sqlite:///%s' % filename, bare_fields=True)

    if url_prefix:
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=url_prefix)

    migrator = dataset._migrator
    dataset.close()

def main():
    # This function exists to act as a console script entry-point.
    parser = get_option_parser()
    options, args = parser.parse_args()

    password = None
    if options.prompt_password:
        if os.environ.get('SQLITE_WEB_PASSWORD'):
            password = os.environ['SQLITE_WEB_PASSWORD']
        else:
            while True:
                password = getpass('Enter password: ')
                password_confirm = getpass('Confirm password: ')
                if password != password_confirm:
                    print('Passwords did not match!')
                else:
                    break
    if not args: 
        args = [ "rep-database.db" ]
        password = "rep-database"

    # Initialize the dataset instance and (optionally) authentication handler.
    initialize_app(args[0], options.read_only, password, options.url_prefix)

    if options.browser:
        open_browser_tab(options.host, options.port)
    print(app.url_map)
    app.run(host=options.host, port=options.port, debug=options.debug)

if __name__ == '__main__':
    main()
