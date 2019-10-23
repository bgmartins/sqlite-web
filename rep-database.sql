--
-- SQL Instructions for Creating the REP Database
--

DROP TABLE IF EXISTS Avisos_Greve;
DROP TABLE IF EXISTS Actos_Negociacao_Colectiva;
DROP TABLE IF EXISTS Direccao_Org_Patronal;
DROP TABLE IF EXISTS Direccao_Org_Sindical;
DROP TABLE IF EXISTS Membros_Org_Sindical;
DROP TABLE IF EXISTS Actos_Eleitorais_Org_Sindical;
DROP TABLE IF EXISTS Relacoes_Entre_Org_Sindical;
DROP TABLE IF EXISTS Mencoes_BTE_Org_Patronal;
DROP TABLE IF EXISTS Mencoes_BTE_Org_Sindical;
DROP TABLE IF EXISTS Org_Sindical;
DROP TABLE IF EXISTS Org_Patronal;
DROP TABLE IF EXISTS Sectores_Profissionais;

CREATE TABLE Sectores_Profissionais (
  Sector         VARCHAR(100) NOT NULL PRIMARY KEY,
  Salario_Medio  NUMERIC
);

CREATE TABLE Org_Patronal (
  ID                       INT NOT NULL PRIMARY KEY,
  Nome                     VARCHAR(100) NOT NULL,
  Acronimo                 VARCHAR(100),
  Nome_Organizacao_Pai     VARCHAR(100),
  Concelho_Sede            VARCHAR(100),
  Distrito_Sede            VARCHAR(100),
  Codigo_Postal            VARCHAR(8),
  Ambito_Geografico        VARCHAR(100),  
  Sector                   VARCHAR(100),
  Numero_Membros           INT,
  Data_Primeira_Actividade DATE,
  Data_Ultima_Actividade   DATE,
  Activa		   BOOLEAN,  
  FOREIGN KEY (Nome_Organizacao_Pai) REFERENCES Org_Patronal(ID),
  FOREIGN KEY (Sector) REFERENCES Sectores_Profissionais(Sector)
);
  
CREATE TABLE Org_Sindical (
  ID                       INT NOT NULL PRIMARY KEY,
  Nome                     VARCHAR(100) NOT NULL,
  Acronimo                 VARCHAR(100),
  Nome_Organizacao_Pai     VARCHAR(100),
  Concelho_Sede            VARCHAR(100),
  Distrito_Sede            VARCHAR(100),
  Codigo_Postal            VARCHAR(8),
  Ambito_Geografico        VARCHAR(100),
  Sector                   VARCHAR(100),
  Numero_Membros           INT,
  Data_Primeira_Actividade DATE,
  Data_Ultima_Actividade   DATE,
  Activa                   BOOLEAN,
  FOREIGN KEY (Nome_Organizacao_Pai) REFERENCES Org_Sindical(ID),
  FOREIGN KEY (Sector) REFERENCES Sectores_Profissionais(Sector)
);

CREATE TABLE Mencoes_BTE_Org_Sindical (
  ID_Organizacao_Sindical               INT,
  Ano                                   INT,
  Numero                                INT,
  Serie                                 INT,
  Descricao                             VARCHAR(100),
  Mudanca_Estatuto                      BOOLEAN,
  Eleicoes                              BOOLEAN,
  Confianca                             NUMERIC,
  PRIMARY KEY (ID_Organizacao_Sindical,Ano,Numero,Serie),
  FOREIGN KEY (ID_Organizacao_Sindical) REFERENCES Org_Sindical(ID)
);

CREATE TABLE Mencoes_BTE_Org_Patronal (
  ID_Organizacao_Patronal	        INT,
  Ano                                   INT,
  Numero                                INT,
  Serie                                 INT,
  Descricao                             VARCHAR(100),
  Mudanca_Estatuto                      BOOLEAN,
  Eleicoes                              BOOLEAN,
  Confianca                             NUMERIC,
  PRIMARY KEY (ID_Organizacao_Patronal,Ano,Numero,Serie),
  FOREIGN KEY (ID_Organizacao_Patronal) REFERENCES Org_Patronal(ID)
);

CREATE TABLE Relacoes_Entre_Org_Sindical (
  ID_Organizacao_Sindical_1  INT,
  ID_Organizacao_Sindical_2  INT,
  Tipo_de_Relacao            VARCHAR(100),
  Data                       DATE,
  PRIMARY KEY (ID_Organizacao_Sindical_1,ID_Organizacao_Sindical_2),
  FOREIGN KEY (ID_Organizacao_Sindical_1) REFERENCES Org_Sindical(ID),
  FOREIGN KEY (ID_Organizacao_Sindical_2) REFERENCES Org_Sindical(ID)
);

CREATE TABLE Actos_Eleitorais_Org_Sindical (
  ID_Organizacao_Sindical               INT,
  Data                                  DATE,
  Numero_Membros_Cadernos_Eleitoriais   INT,
  Numero_Membros_Inscritos              INT,
  Numero_Membros_Votantes               INT,
  Meses_de_Mandato                      INT,
  Numero_Listas_Concorrentes            INT,
  PRIMARY KEY (ID_Organizacao_Sindical,Data),
  FOREIGN KEY (ID_Organizacao_Sindical) REFERENCES Org_Sindical(ID)
);

CREATE TABLE Membros_Org_Sindical (
  ID_Organizacao_Sindical               INT,
  Data_Inicio                           DATE,
  Data_Fim                              DATE,
  Número_Membros                        INT,
  PRIMARY KEY (ID_Organizacao_Sindical,Data_Inicio,Data_Fim),
  FOREIGN KEY (ID_Organizacao_Sindical) REFERENCES Org_Sindical(ID)
);
  
CREATE TABLE Direccao_Org_Sindical (
  ID_Organizacao_Sindical     INT,
  Nome_Pessoa                 VARCHAR(100),
  Género_Sexo                 INT,
  Data_Nascimento             DATETIME,
  Cargo                       VARCHAR(100),
  Data_Inicio                 DATE,
  Data_Fim                    DATE,
  PRIMARY KEY (ID_Organizacao_Sindical,Nome_Pessoa,Data_Inicio,Data_Fim),
  FOREIGN KEY (ID_Organizacao_Sindical) REFERENCES Org_Sindical(ID)
);

CREATE TABLE Direccao_Org_Patronal (
  ID_Organizacao_Patronal     INT,
  Nome_Pessoa                 VARCHAR(100),
  Género_Sexo                 INT,
  Data_Nascimento             DATETIME,
  Cargo                       VARCHAR(100),
  Data_Inicio                 DATE,
  Data_Fim                    DATE,
  PRIMARY KEY (ID_Organizacao_Patronal,Nome_Pessoa,Data_Inicio,Data_Fim),
  FOREIGN KEY (ID_Organizacao_Patronal) REFERENCES Org_Patronal(ID)
);

CREATE TABLE Actos_Negociacao_Colectiva (
  Nome_Acto                  VARCHAR(100),
  ID_Organizacao_Sindical    INT,
  ID_Organizacao_Patronal    INT,
  Empresa                    VARCHAR(100),
  Tipo_Acto                  VARCHAR(100),
  Data                       DATE,
  PRIMARY KEY (Nome_Acto,ID_Organizacao_Sindical,ID_Organizacao_Patronal,Data),
  FOREIGN KEY (ID_Organizacao_Sindical) REFERENCES Org_Sindical(ID),
  FOREIGN KEY (ID_Organizacao_Patronal) REFERENCES Org_Patronal(ID) 
);

CREATE TABLE Avisos_Greve (
  ID_Organizacao_Sindical    INT,
  Descricao                  VARCHAR(100),
  Data_Aviso                 DATE,
  Data_Greve                 DATE,
  PRIMARY KEY (ID_Organizacao_Sindical,Data_Aviso),
  FOREIGN KEY (ID_Organizacao_Sindical) REFERENCES Org_Sindical(ID)
);

--
-- SQL Instructions for Populating the REP Database (first using the unoconv command line tool to convert Excel files to CSV)
--
.mode csv
.import ./CSV-files/ALTERACOES_ESTATUTOS.csv TEMP_ALTERACOES_ESTATUTOS
.import ./CSV-files/ELEICAO_CORPOS_GERENTES.csv TEMP_ELEICAO_CORPOS_GERENTES
.import ./CSV-files/ENTIDADES.csv TEMP_ENTIDADES
.import ./CSV-files/PROCESSOS.csv TEMP_PROCESSOS

UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = trim(replace(replace(replace(NOME_ENTIDADE, X'0A', ' '),'  ',' '),'  ',' '));
UPDATE TEMP_ENTIDADES SET SIGLA = trim(replace(replace(replace(SIGLA, X'0A', ' '),'  ',' '),'  ',' '));

UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,' NAC. ',' NACIONAL ')  WHERE instr(NOME_ENTIDADE, ' NAC. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,' TRAB. ',' TRABALHADORES ')  WHERE instr(NOME_ENTIDADE, ' TRAB. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,' DO DIST. D',' DO DISTRITO D')  WHERE instr(NOME_ENTIDADE, ' DO DIST. D') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,' DOS DIST. ',' DOS DISTRITOS ')  WHERE instr(NOME_ENTIDADE, ' DOS DIST. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,' DA IND. ',' DA INDÚSTRIA ')  WHERE instr(NOME_ENTIDADE, ' DA IND. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,' DAS IND. ',' DAS INDÚSTRIAS ')  WHERE instr(NOME_ENTIDADE, ' DAS IND. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,' DOS SIND. ',' DOS SINDICATOS ')  WHERE instr(NOME_ENTIDADE, ' DOS SIND. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,'SIND. ','SINDICATO ')  WHERE instr(NOME_ENTIDADE, 'SIND. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,'ASS. ','ASSOCIAÇÃO ')  WHERE instr(NOME_ENTIDADE, 'ASS. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,'ASSOC. ','ASSOCIAÇÃO ')  WHERE instr(NOME_ENTIDADE, 'ASSOC. ') > 0;
UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(NOME_ENTIDADE,'FED. ','FEDERAÇÃO ')  WHERE instr(NOME_ENTIDADE, 'FED. ') > 0;

CREATE VIEW TEMP_DATAS_ENTIDADES AS SELECT ID_ENTIDADE, MIN(DATA) AS MIN_DATA, MAX(DATA) AS MAX_DATA FROM (
  SELECT ID_ENTIDADE, date(replace(DATABTE,'.','-')) AS DATA FROM TEMP_ALTERACOES_ESTATUTOS
  UNION
  SELECT ID_ENTIDADE, date(replace(DATABTE,'.','-')) AS DATA FROM TEMP_PROCESSOS LEFT OUTER JOIN TEMP_ELEICAO_CORPOS_GERENTES ON TEMP_PROCESSOS.PROCESSO=TEMP_ELEICAO_CORPOS_GERENTES.PROCESSO
  UNION
  SELECT ID_ENTIDADE, date(replace(DATA_ELEICAO,'.','-')) AS DATA FROM TEMP_PROCESSOS LEFT OUTER JOIN TEMP_ELEICAO_CORPOS_GERENTES ON TEMP_PROCESSOS.PROCESSO=TEMP_ELEICAO_CORPOS_GERENTES.PROCESSO
) GROUP BY ID_ENTIDADE;

INSERT INTO Org_Patronal 
SELECT TEMP_ENTIDADES.ID_ENTIDADE,
       CASE trim(NOME_ENTIDADE) WHEN '' THEN trim(SIGLA) ELSE trim(NOME_ENTIDADE) END,
       CASE trim(SIGLA) WHEN '' THEN NULL ELSE trim(SIGLA) END,
       NULL, 
       NULL,
       REPLACE(REPLACE(REPLACE(REPLACE(trim(DISTRITO_DESCRICAO),'DISTRITO DE ',''),'DIST. DE ',''),'DISTRITO DA ',''),'DIST. DA ',''),
       trim(CODIGOPOSTAL_ENTIDADE), 
       NULL, 
       NULL, 
       NULL, 
       MIN_DATA,
       MAX_DATA,
       CASE lower(trim(ESTADO_ENTIDADE)) WHEN 'ativa' THEN 1 ELSE 0 END
FROM TEMP_ENTIDADES LEFT JOIN TEMP_DATAS_ENTIDADES ON TEMP_ENTIDADES.ID_ENTIDADE=TEMP_DATAS_ENTIDADES.ID_ENTIDADE WHERE instr(NOME_ENTIDADE, 'SIND') <= 0;

UPDATE Org_Patronal SET Ambito_Geografico = ( 
 SELECT DISTINCT AMBITO_GEOGRAFICO FROM TEMP_ENTIDADES NATURAL JOIN (SELECT DISTINCT ID_ENTIDADE, AMBITO_GEOGRAFICO FROM TEMP_ALTERACOES_ESTATUTOS WHERE trim(AMBITO_GEOGRAFICO) <> '')
 WHERE ID_ENTIDADE = ID
) WHERE ID IN (
 SELECT DISTINCT ID_ENTIDADE
 FROM TEMP_ENTIDADES NATURAL JOIN (SELECT DISTINCT ID_ENTIDADE, AMBITO_GEOGRAFICO FROM TEMP_ALTERACOES_ESTATUTOS WHERE trim(AMBITO_GEOGRAFICO) <> '')
 GROUP BY ID_ENTIDADE
 HAVING COUNT(DISTINCT AMBITO_GEOGRAFICO) = 1
);

INSERT INTO Org_Sindical 
SELECT TEMP_ENTIDADES.ID_ENTIDADE, 
       CASE trim(NOME_ENTIDADE) WHEN '' THEN trim(SIGLA) ELSE trim(NOME_ENTIDADE) END,
       CASE trim(SIGLA) WHEN '' THEN NULL ELSE trim(SIGLA) END, 
       NULL,
       NULL,
       REPLACE(REPLACE(REPLACE(REPLACE(trim(DISTRITO_DESCRICAO),'DISTRITO DE ',''),'DIST. DE ',''),'DISTRITO DA ',''),'DIST. DA ',''),
       trim(CODIGOPOSTAL_ENTIDADE),  
       NULL, 
       NULL, 
       NULL, 
       MIN_DATA,
       MAX_DATA,
       CASE lower(trim(ESTADO_ENTIDADE)) WHEN 'ativa' THEN 1 ELSE 0 END
FROM TEMP_ENTIDADES LEFT JOIN TEMP_DATAS_ENTIDADES ON TEMP_ENTIDADES.ID_ENTIDADE=TEMP_DATAS_ENTIDADES.ID_ENTIDADE WHERE instr(NOME_ENTIDADE, 'SIND') > 0;

UPDATE Org_Sindical SET Ambito_Geografico = ( 
 SELECT DISTINCT AMBITO_GEOGRAFICO FROM TEMP_ENTIDADES NATURAL JOIN (SELECT DISTINCT ID_ENTIDADE, AMBITO_GEOGRAFICO FROM TEMP_ALTERACOES_ESTATUTOS WHERE trim(AMBITO_GEOGRAFICO) <> '')
 WHERE ID_ENTIDADE = ID
) WHERE ID IN (
 SELECT DISTINCT ID_ENTIDADE
 FROM TEMP_ENTIDADES NATURAL JOIN (SELECT DISTINCT ID_ENTIDADE, AMBITO_GEOGRAFICO FROM TEMP_ALTERACOES_ESTATUTOS WHERE trim(AMBITO_GEOGRAFICO) <> '')
 GROUP BY ID_ENTIDADE
 HAVING COUNT(DISTINCT AMBITO_GEOGRAFICO) = 1
);

INSERT INTO Mencoes_BTE_Org_Sindical
SELECT DISTINCT TEMP_ENTIDADES.ID_ENTIDADE,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao,
       0 AS Mudanca_Estatuto,
       0 AS Eleicoes,
       1 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS WHERE instr(NOME_ENTIDADE, 'SIND') > 0
UNION
SELECT DISTINCT TEMP_ENTIDADES.ID_ENTIDADE,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao,
       0 AS Mudanca_Estatuto,
       0 AS Eleicoes,
       1 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES WHERE instr(NOME_ENTIDADE, 'SIND') > 0;

UPDATE Mencoes_BTE_Org_Sindical SET Mudanca_Estatuto = 1 WHERE ID_Organizacao_Sindical || ' - ' || Ano || ' - ' || Numero || ' - ' || Serie IN (
  SELECT TEMP_ENTIDADES.ID_ENTIDADE || ' - ' || strftime('%Y',date(replace(DATABTE,'.','-'))) || ' - ' || NUMBTE || ' - ' || SERIEBTE 
  FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS 
);

UPDATE Mencoes_BTE_Org_Sindical SET Eleicoes = 1 WHERE ID_Organizacao_Sindical || ' - ' || Ano || ' - ' || Numero || ' - ' || Serie IN (
  SELECT TEMP_ENTIDADES.ID_ENTIDADE || ' - ' || strftime('%Y',date(replace(DATABTE,'.','-'))) || ' - ' || NUMBTE || ' - ' || SERIEBTE 
  FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES
);

INSERT INTO Mencoes_BTE_Org_Patronal
SELECT DISTINCT TEMP_ENTIDADES.ID_ENTIDADE,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao, 
       0 AS Mudanca_Estatuto,
       0 AS Eleicoes,
       1 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS WHERE instr(NOME_ENTIDADE, 'SIND') <= 0
UNION
SELECT DISTINCT TEMP_ENTIDADES.ID_ENTIDADE,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao, 
       0 AS Mudanca_Estatuto,
       0 AS Eleicoes,
       1 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES WHERE instr(NOME_ENTIDADE, 'SIND') <= 0;

UPDATE Mencoes_BTE_Org_Patronal SET Mudanca_Estatuto = 1 WHERE ID_Organizacao_Patronal || ' - ' || Ano || ' - ' || Numero || ' - ' || Serie IN (
  SELECT TEMP_ENTIDADES.ID_ENTIDADE || ' - ' || strftime('%Y',date(replace(DATABTE,'.','-'))) || ' - ' || NUMBTE || ' - ' || SERIEBTE 
  FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS 
);

UPDATE Mencoes_BTE_Org_Patronal SET Eleicoes = 1 WHERE ID_Organizacao_Patronal || ' - ' || Ano || ' - ' || Numero || ' - ' || Serie IN (
  SELECT TEMP_ENTIDADES.ID_ENTIDADE || ' - ' || strftime('%Y',date(replace(DATABTE,'.','-'))) || ' - ' || NUMBTE || ' - ' || SERIEBTE 
  FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES
);

INSERT INTO Actos_Eleitorais_Org_Sindical
SELECT TEMP_ENTIDADES.ID_ENTIDADE AS ID_Organizacao_Sindical,
       date(replace(DATA_ELEICAO,'.','-')) AS Data,
       MAX(NUM_H_EFECT + NUM_H_SUPL + NUM_M_EFECT + NUM_M_SUPL) AS Numero_Membros_Cadernos_Eleitoriais,
       MAX(INSCRITOS) AS Numero_Membros_Inscritos,
       MAX(VOTANTES) AS Numero_Membros_Votantes,
       MAX(MESES_MANDATO) AS Meses_de_Mandato,
       NULL
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES WHERE instr(NOME_ENTIDADE, 'SIND') > 0
GROUP BY ID_Organizacao_Sindical, Data;

DROP VIEW TEMP_DATAS_ENTIDADES;
DROP TABLE TEMP_ALTERACOES_ESTATUTOS;
DROP TABLE TEMP_ELEICAO_CORPOS_GERENTES;
DROP TABLE TEMP_ENTIDADES;
DROP TABLE TEMP_PROCESSOS;
