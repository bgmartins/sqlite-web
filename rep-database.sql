--
-- SQL Instructions for Creating the REP Database
--

DROP TABLE IF EXISTS Avisos_Greve;
DROP TABLE IF EXISTS Actos_Negociacao_Colectiva;
DROP TABLE IF EXISTS Direccao_Organizacao_Patronal;
DROP TABLE IF EXISTS Direccao_Organizacao_Sindical;
DROP TABLE IF EXISTS Membros_Organizacao_Sindical;
DROP TABLE IF EXISTS Actos_Eleitorais_Organizacao_Sindical;
DROP TABLE IF EXISTS Relacoes_Entre_Organizacao_Sindical;
DROP TABLE IF EXISTS Mencoes_BTE_Organizacao_Patronal;
DROP TABLE IF EXISTS Mencoes_BTE_Organizacao_Sindical;
DROP TABLE IF EXISTS Organizacao_Sindical;
DROP TABLE IF EXISTS Organizacao_Patronal;
DROP TABLE IF EXISTS Sectores_Profissionais;

CREATE TABLE Sectores_Profissionais (
  Sector         VARCHAR(100) NOT NULL PRIMARY KEY,
  Salario_Medio  NUMERIC
);

CREATE TABLE Organizacao_Patronal (
  Nome                   VARCHAR(100) NOT NULL PRIMARY KEY,
  Acronimo               VARCHAR(100),
  Nome_Organizacao_Pai   VARCHAR(100),
  Concelho_Sede          VARCHAR(100),
  Distrito_Sede          VARCHAR(100),
  Codigo_Postal          VARCHAR(8),
  Âmbito_Geográfico      VARCHAR(100),  
  Sector                 VARCHAR(100),
  Numero_Membros         INT,
  Data_Criacao           DATE,
  Data_Extincao          DATE,
  FOREIGN KEY (Nome_Organizacao_Pai) REFERENCES Organizacao_Patronal,
  FOREIGN KEY (Sector) REFERENCES Sectores_Profissionais
);
  
CREATE TABLE Organizacao_Sindical (
  Nome                   VARCHAR(100) NOT NULL PRIMARY KEY,
  Acronimo               VARCHAR(100),
  Nome_Organizacao_Pai   VARCHAR(100),
  Concelho_Sede          VARCHAR(100),
  Distrito_Sede          VARCHAR(100),
  Codigo_Postal          VARCHAR(8),
  Âmbito_Geográfico      VARCHAR(100),
  Sector                 VARCHAR(100),
  Numero_Membros         INT,
  Data_Criacao           DATE,
  Data_Extincao          DATE,
  FOREIGN KEY (Nome_Organizacao_Pai) REFERENCES Organizacao_Sindical,
  FOREIGN KEY (Sector) REFERENCES Sectores_Profissionais
);

CREATE TABLE Mencoes_BTE_Organizacao_Sindical (
  Nome_Organizacao_Sindical             VARCHAR(100),
  Ano                                   INT,
  Numero                                INT,
  Serie                                 INT,
  Descricao                             VARCHAR(100),
  Mudanca_Estatuto                      BOOLEAN,
  Confianca                             NUMERIC,
  PRIMARY KEY (Nome_Organizacao_Sindical,Ano,Numero,Serie),
  FOREIGN KEY (Nome_Organizacao_Sindical) REFERENCES Organizacao_Sindical
);

CREATE TABLE Mencoes_BTE_Organizacao_Patronal (
  Nome_Organizacao_Patronal             VARCHAR(100),
  Ano                                   INT,
  Numero                                INT,
  Serie                                 INT,
  Descricao                             VARCHAR(100),
  Mudanca_Estatuto                      BOOLEAN,
  Confianca                             NUMERIC,
  PRIMARY KEY (Nome_Organizacao_Patronal,Ano,Numero,Serie),
  FOREIGN KEY (Nome_Organizacao_Patronal) REFERENCES Organizacao_Patronal
);

CREATE TABLE Relacoes_Entre_Organizacao_Sindical (
  Nome_Organizacao_Sindical_1  VARCHAR(100),
  Nome_Organizacao_Sindical_2  VARCHAR(100),
  Tipo_de_Relacao              VARCHAR(100),
  Data                         DATE,
  PRIMARY KEY (Nome_Organizacao_Sindical_1,Nome_Organizacao_Sindical_2),
  FOREIGN KEY (Nome_Organizacao_Sindical_1) REFERENCES Organizacao_Sindical,
  FOREIGN KEY (Nome_Organizacao_Sindical_2) REFERENCES Organizacao_Sindical
);

CREATE TABLE Actos_Eleitorais_Organizacao_Sindical (
  Nome_Organizacao_Sindical             VARCHAR(100),
  Data                                  DATE,
  Número_Membros_Cadernos_Eleitoriais   INT,
  Número_Listas_Concorrentes            INT,
  PRIMARY KEY (Nome_Organizacao_Sindical,Data),
  FOREIGN KEY (Nome_Organizacao_Sindical) REFERENCES Organizacao_Sindical
);

CREATE TABLE Membros_Organizacao_Sindical (
  Nome_Organizacao_Sindical             VARCHAR(100),
  Data_Inicio                           DATE,
  Data_Fim                              DATE,
  Número_Membros                        INT,
  PRIMARY KEY (Nome_Organizacao_Sindical,Data_Inicio,Data_Fim),
  FOREIGN KEY (Nome_Organizacao_Sindical) REFERENCES Organizacao_Sindical
);
  
CREATE TABLE Direccao_Organizacao_Sindical (
  Nome_Organizacao_Sindical   VARCHAR(100),
  Nome_Pessoa                 VARCHAR(100),
  Género_Sexo                 INT,
  Data_Nascimento             DATETIME,
  Cargo                       VARCHAR(100),
  Data_Inicio                 DATE,
  Data_Fim                    DATE,
  PRIMARY KEY (Nome_Organizacao_Sindical,Nome_Pessoa,Data_Inicio,Data_Fim),
  FOREIGN KEY (Nome_Organizacao_Sindical) REFERENCES Organizacao_Sindical
);

CREATE TABLE Direccao_Organizacao_Patronal (
  Nome_Organizacao_Patronal   VARCHAR(100),
  Nome_Pessoa                 VARCHAR(100),
  Género_Sexo                 INT,
  Data_Nascimento             DATETIME,
  Cargo                       VARCHAR(100),
  Data_Inicio                 DATE,
  Data_Fim                    DATE,
  PRIMARY KEY (Nome_Organizacao_Patronal,Nome_Pessoa,Data_Inicio,Data_Fim),
  FOREIGN KEY (Nome_Organizacao_Patronal) REFERENCES Organizacao_Patronal  
);

CREATE TABLE Actos_Negociacao_Colectiva (
  Nome_Acto                  VARCHAR(100),
  Nome_Organizacao_Sindical  VARCHAR(100),
  Nome_Organizacao_Patronal  VARCHAR(100),
  Empresa                    VARCHAR(100),
  Tipo_Acto                  VARCHAR(100),
  Data                       DATE,
  PRIMARY KEY (Nome_Acto,Nome_Organizacao_Sindical,Nome_Organizacao_Patronal,Data),
  FOREIGN KEY (Nome_Organizacao_Sindical) REFERENCES Organizacao_Sindical,
  FOREIGN KEY (Nome_Organizacao_Patronal) REFERENCES Organizacao_Patronal 
);

CREATE TABLE Avisos_Greve (
  Nome_Organizacao_Sindical  VARCHAR(100),
  Descricao                  VARCHAR(100),
  Data_Aviso                 DATE,
  Data_Greve                 DATE,
  PRIMARY KEY (Nome_Organizacao_Sindical,Data_Aviso),
  FOREIGN KEY (Nome_Organizacao_Sindical) REFERENCES Organizacao_Sindical
);

--
-- SQL Instructions for Populating the REP Database (first using the unoconv command line tool to convert Excel files to CSV)
--
.mode csv
.import ./CSV-files/ALTERACOES_ESTATUTOS.csv TEMP_ALTERACOES_ESTATUTOS
.import ./CSV-files/ELEICAO_CORPOS_GERENTES.csv TEMP_ELEICAO_CORPOS_GERENTES
.import ./CSV-files/ENTIDADES.csv TEMP_ENTIDADES
.import ./CSV-files/PROCESSOS.csv TEMP_PROCESSOS

UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = replace(replace(replace(NOME_ENTIDADE, X'0A', ' '),'  ',' '),'  ',' ');

UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = ID_ENTIDADE || ' - ' || trim(NOME_ENTIDADE)
WHERE trim(NOME_ENTIDADE) IN (SELECT trim(NOME_ENTIDADE) FROM TEMP_ENTIDADES GROUP BY trim(NOME_ENTIDADE) HAVING COUNT(*) > 1);

INSERT INTO Organizacao_Patronal 
SELECT CASE trim(NOME_ENTIDADE) WHEN '' THEN trim(SIGLA) ELSE trim(NOME_ENTIDADE) END,
       CASE trim(SIGLA) WHEN '' THEN NULL ELSE trim(SIGLA) END,
       NULL, 
       REPLACE(trim(DISTRITO_DESCRICAO),'DISTRITO DE ',''),
       trim(CODIGOPOSTAL_ENTIDADE), 
       NULL, 
       NULL, 
       NULL, 
       NULL, 
       NULL, 
       NULL
FROM TEMP_ENTIDADES WHERE instr(NOME_ENTIDADE, 'SINDICATO') <= 0;

INSERT INTO Organizacao_Sindical 
SELECT CASE trim(NOME_ENTIDADE) WHEN '' THEN trim(SIGLA) ELSE trim(NOME_ENTIDADE) END,
       CASE trim(SIGLA) WHEN '' THEN NULL ELSE trim(SIGLA) END, 
       NULL, 
       REPLACE(trim(DISTRITO_DESCRICAO),'DISTRITO DE ',''),
       trim(CODIGOPOSTAL_ENTIDADE), 
       NULL, 
       NULL, 
       NULL, 
       NULL, 
       NULL, 
       NULL
FROM TEMP_ENTIDADES WHERE instr(NOME_ENTIDADE, 'SINDICATO') > 0;

INSERT INTO Mencoes_BTE_Organizacao_Sindical
SELECT CASE trim(NOME_ENTIDADE) WHEN '' THEN trim(SIGLA) ELSE trim(NOME_ENTIDADE) END AS Nome_Organizacao_Sindical,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao,
       1.0 AS Mudanca_Estatuto,
       1.0 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS WHERE instr(NOME_ENTIDADE, 'SINDICATO') > 0
GROUP BY Nome_Organizacao_Sindical, Ano, Numero, Serie, Descricao, Mudanca_Estatuto, Confianca;

INSERT INTO Mencoes_BTE_Organizacao_Patronal
SELECT CASE trim(NOME_ENTIDADE) WHEN '' THEN trim(SIGLA) ELSE trim(NOME_ENTIDADE) END AS Nome_Organizacao_Patronal,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao, 
       1.0 AS Mudanca_Estatuto,
       1.0 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS WHERE instr(NOME_ENTIDADE, 'SINDICATO') <= 0
GROUP BY Nome_Organizacao_Patronal, Ano, Numero, Serie, Descricao, Mudanca_Estatuto, Confianca;

DROP TABLE TEMP_ALTERACOES_ESTATUTOS;
DROP TABLE TEMP_ELEICAO_CORPOS_GERENTES;
DROP TABLE TEMP_ENTIDADES;
DROP TABLE TEMP_PROCESSOS;