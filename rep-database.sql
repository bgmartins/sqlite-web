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
  URL                                   VARCHAR(100),
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
  URL			                VARCHAR(100),
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

CREATE TRIGGER Mencoes_BTE_Org_Sindical_update AFTER UPDATE ON Mencoes_BTE_Org_Sindical BEGIN
    UPDATE Mencoes_BTE_Org_Sindical
    SET    URL = "https://github.com/bgmartins/rep-database/raw/master/BTE-data/bte" || [NEW].Numero || "_" || [NEW].Ano || ".pdf"
    WHERE ID_Organizacao_Sindical = [NEW].ID_Organizacao_Sindical; 
END;

CREATE TRIGGER Mencoes_BTE_Org_Patronal_update AFTER UPDATE ON Mencoes_BTE_Org_Patronal BEGIN
    UPDATE Mencoes_BTE_Org_Patronal
    SET    URL = "https://github.com/bgmartins/rep-database/raw/master/BTE-data/bte" || [NEW].Numero || "_" || [NEW].Ano || ".pdf"
    WHERE ID_Organizacao_Patronal = [NEW].ID_Organizacao_Patronal; 
END;

CREATE TRIGGER Mencoes_BTE_Org_Sindical_insert AFTER INSERT ON Mencoes_BTE_Org_Sindical BEGIN
    UPDATE Mencoes_BTE_Org_Sindical
    SET    URL = "https://github.com/bgmartins/rep-database/raw/master/BTE-data/bte" || [NEW].Numero || "_" || [NEW].Ano || ".pdf"
    WHERE ID_Organizacao_Sindical = [NEW].ID_Organizacao_Sindical; 
END;

CREATE TRIGGER Mencoes_BTE_Org_Patronal_insert AFTER INSERT ON Mencoes_BTE_Org_Patronal BEGIN
    UPDATE Mencoes_BTE_Org_Patronal
    SET    URL = "https://github.com/bgmartins/rep-database/raw/master/BTE-data/bte" || [NEW].Numero || "_" || [NEW].Ano || ".pdf"
    WHERE ID_Organizacao_Patronal = [NEW].ID_Organizacao_Patronal; 
END;

--
-- SQL Instructions for Populating the REP Database (first using the unoconv command line tool to convert Excel files to CSV)
--
.mode csv
.import ./CSV-files/ALTERACOES_ESTATUTOS.csv TEMP_ALTERACOES_ESTATUTOS
.import ./CSV-files/ELEICAO_CORPOS_GERENTES.csv TEMP_ELEICAO_CORPOS_GERENTES
.import ./CSV-files/ENTIDADES.csv TEMP_ENTIDADES
.import ./CSV-files/PROCESSOS.csv TEMP_PROCESSOS
.import ./CSV-files/Protocolo_ICS_INESC_DGERT_ListaIRCTs_ID.csv Lista_IRCTs_ID
-- O ficheiro abaixo é conversão para UTF8 usando NOTEPAD do Protocolo_ICS_INESC_DGERT_ListadosOutorgantes.csv que tinha sido convertido para CSV usando Excel e os ; passados para , em NOTEPAD 
.import ./CSV-files/Protocolo_ICS_INESC_DGERT_ListadosOutorgantes_UTF8.txt LISTA_OUTORGANTES_UTF



UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = trim(replace(replace(replace(NOME_ENTIDADE, X'0A', ' '),'  ',' '),'  ',' '));
UPDATE TEMP_ENTIDADES SET SIGLA = trim(replace(replace(replace(SIGLA, X'0A', ' '),'  ',' '),'  ',' '));

UPDATE TEMP_ENTIDADES SET SIGLA = TRIM(SUBSTR(NOME_ENTIDADE,0,instr(NOME_ENTIDADE,'-'))) 
WHERE (SIGLA IS NULL OR TRIM(SIGLA)='') AND instr(NOME_ENTIDADE, '-') > 0 AND instr(TRIM(SUBSTR(NOME_ENTIDADE,0,instr(NOME_ENTIDADE,'-'))),' ') <=0;

UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = TRIM(SUBSTR(NOME_ENTIDADE,instr(NOME_ENTIDADE,'-') + 1, LENGTH(NOME_ENTIDADE) - instr(NOME_ENTIDADE,'-') + 1)) 
WHERE instr(NOME_ENTIDADE, '-') > 0 AND instr(TRIM(SUBSTR(NOME_ENTIDADE,0,instr(NOME_ENTIDADE,'-'))),' ') <=0
AND (TRIM(SIGLA)='' OR TRIM(SIGLA)=TRIM(SUBSTR(NOME_ENTIDADE,0,instr(NOME_ENTIDADE,'-'))));

UPDATE TEMP_ENTIDADES SET SIGLA = TRIM(SUBSTR(NOME_ENTIDADE,instr(NOME_ENTIDADE,'-') + 1, LENGTH(NOME_ENTIDADE) - instr(NOME_ENTIDADE,'-') + 1)) 
WHERE (SIGLA IS NULL OR TRIM(SIGLA)='') AND instr(NOME_ENTIDADE, '-') > 0 AND instr(TRIM(SUBSTR(NOME_ENTIDADE,instr(NOME_ENTIDADE,'-') + 1, LENGTH(NOME_ENTIDADE) - instr(NOME_ENTIDADE,'-') + 1)),' ') <=0;

UPDATE TEMP_ENTIDADES SET NOME_ENTIDADE = TRIM(SUBSTR(NOME_ENTIDADE,0,instr(NOME_ENTIDADE,'-')))
WHERE instr(NOME_ENTIDADE, '-') > 0 AND instr(TRIM(SUBSTR(NOME_ENTIDADE,instr(NOME_ENTIDADE,'-') + 1, LENGTH(NOME_ENTIDADE) - instr(NOME_ENTIDADE,'-') + 1)) , ' ') <=0
AND (TRIM(SIGLA)='' OR TRIM(SIGLA)=TRIM(SUBSTR(NOME_ENTIDADE,instr(NOME_ENTIDADE,'-') + 1, LENGTH(NOME_ENTIDADE) - instr(NOME_ENTIDADE,'-') + 1)));

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
       REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(trim(DISTRITO_DESCRICAO),'DISTRITO DO ',''),'DIST. DO ',''),'DISTRITO DE ',''),'DIST. DE ',''),'DISTRITO DA ',''),'DIST. DA ',''),
       trim(CODIGOPOSTAL_ENTIDADE), 
       NULL, 
       NULL, 
       NULL, 
       MIN_DATA,
       MAX_DATA,
       CASE lower(trim(ESTADO_ENTIDADE)) WHEN 'ativa' THEN 1 ELSE 0 END
FROM TEMP_ENTIDADES LEFT JOIN TEMP_DATAS_ENTIDADES ON TEMP_ENTIDADES.ID_ENTIDADE=TEMP_DATAS_ENTIDADES.ID_ENTIDADE WHERE instr(NOME_ENTIDADE, 'SIND') <= 0 AND instr(NOME_ENTIDADE, 'TRABALH') <= 0 AND instr(NOME_ENTIDADE, 'PROFISSI') <= 0 AND instr(NOME_ENTIDADE, 'CGTPIN') <= 0 AND instr(NOME_ENTIDADE, 'FEDERA') <= 0;

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
       REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(trim(DISTRITO_DESCRICAO),'DISTRITO DO ',''),'DIST. DO ',''),'DISTRITO DE ',''),'DIST. DE ',''),'DISTRITO DA ',''),'DIST. DA ',''),
       trim(CODIGOPOSTAL_ENTIDADE),  
       NULL, 
       NULL, 
       NULL, 
       MIN_DATA,
       MAX_DATA,
       CASE lower(trim(ESTADO_ENTIDADE)) WHEN 'ativa' THEN 1 ELSE 0 END
FROM TEMP_ENTIDADES LEFT JOIN TEMP_DATAS_ENTIDADES ON TEMP_ENTIDADES.ID_ENTIDADE=TEMP_DATAS_ENTIDADES.ID_ENTIDADE WHERE instr(NOME_ENTIDADE, 'SIND') > 0 OR instr(NOME_ENTIDADE, 'TRABALH') > 0 OR instr(NOME_ENTIDADE, 'PROFISSI') > 0 OR instr(NOME_ENTIDADE, 'CGTPIN') > 0 OR instr(NOME_ENTIDADE, 'FEDERA') > 0;

UPDATE Org_Sindical SET Ambito_Geografico = ( 
 SELECT DISTINCT AMBITO_GEOGRAFICO FROM TEMP_ENTIDADES NATURAL JOIN (SELECT DISTINCT ID_ENTIDADE, AMBITO_GEOGRAFICO FROM TEMP_ALTERACOES_ESTATUTOS WHERE trim(AMBITO_GEOGRAFICO) <> '')
 WHERE ID_ENTIDADE = ID
) WHERE ID IN (
 SELECT DISTINCT ID_ENTIDADE
 FROM TEMP_ENTIDADES NATURAL JOIN (SELECT DISTINCT ID_ENTIDADE, AMBITO_GEOGRAFICO FROM TEMP_ALTERACOES_ESTATUTOS WHERE trim(AMBITO_GEOGRAFICO) <> '')
 GROUP BY ID_ENTIDADE
 HAVING COUNT(DISTINCT AMBITO_GEOGRAFICO) = 1
);

INSERT INTO Relacoes_Entre_Org_Sindical
SELECT A.ID AS ID_Organizacao_Sindical_1, B.ID AS ID_Organizacao_Sindical_2, 'CONTIDO EM', NULL
FROM ORG_SINDICAL AS A, ORG_SINDICAL AS B
WHERE A.Nome_Organizacao_Pai IS NOT NULL AND B.NOME = A.Nome_Organizacao_Pai;

INSERT INTO Relacoes_Entre_Org_Sindical
SELECT B.ID AS ID_Organizacao_Sindical_1, A.ID AS ID_Organizacao_Sindical_2, 'CONTEM', NULL
FROM ORG_SINDICAL AS A, ORG_SINDICAL AS B
WHERE A.Nome_Organizacao_Pai IS NOT NULL AND B.NOME = A.Nome_Organizacao_Pai;

INSERT INTO Mencoes_BTE_Org_Sindical
SELECT DISTINCT TEMP_ENTIDADES.ID_ENTIDADE, NULL,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao,
       0 AS Mudanca_Estatuto,
       0 AS Eleicoes,
       1 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS WHERE instr(NOME_ENTIDADE, 'SIND') > 0 OR instr(NOME_ENTIDADE, 'TRABALH') > 0 OR instr(NOME_ENTIDADE, 'PROFISSI') > 0 OR instr(NOME_ENTIDADE, 'CGTPIN') > 0 OR instr(NOME_ENTIDADE, 'FEDERA') > 0
UNION
SELECT DISTINCT TEMP_ENTIDADES.ID_ENTIDADE, NULL,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao,
       0 AS Mudanca_Estatuto,
       0 AS Eleicoes,
       1 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES WHERE instr(NOME_ENTIDADE, 'SIND') > 0 OR instr(NOME_ENTIDADE, 'TRABALH') > 0 OR instr(NOME_ENTIDADE, 'PROFISSI') > 0 OR instr(NOME_ENTIDADE, 'CGTPIN') > 0 OR instr(NOME_ENTIDADE, 'FEDERA') > 0;

UPDATE Mencoes_BTE_Org_Sindical SET Mudanca_Estatuto = 1 WHERE ID_Organizacao_Sindical || ' - ' || Ano || ' - ' || Numero || ' - ' || Serie IN (
  SELECT TEMP_ENTIDADES.ID_ENTIDADE || ' - ' || strftime('%Y',date(replace(DATABTE,'.','-'))) || ' - ' || NUMBTE || ' - ' || SERIEBTE 
  FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS 
);

UPDATE Mencoes_BTE_Org_Sindical SET Eleicoes = 1 WHERE ID_Organizacao_Sindical || ' - ' || Ano || ' - ' || Numero || ' - ' || Serie IN (
  SELECT TEMP_ENTIDADES.ID_ENTIDADE || ' - ' || strftime('%Y',date(replace(DATABTE,'.','-'))) || ' - ' || NUMBTE || ' - ' || SERIEBTE 
  FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES
);

INSERT INTO Mencoes_BTE_Org_Patronal
SELECT DISTINCT TEMP_ENTIDADES.ID_ENTIDADE, NULL,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao, 
       0 AS Mudanca_Estatuto,
       0 AS Eleicoes,
       1 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ALTERACOES_ESTATUTOS WHERE instr(NOME_ENTIDADE, 'SIND') <= 0 AND instr(NOME_ENTIDADE, 'TRABALH') <= 0 AND instr(NOME_ENTIDADE, 'PROFISSI') <= 0 AND instr(NOME_ENTIDADE, 'CGTPIN') <= 0 AND instr(NOME_ENTIDADE, 'FEDERA') <= 0
UNION
SELECT DISTINCT TEMP_ENTIDADES.ID_ENTIDADE, NULL,
       strftime('%Y',date(replace(DATABTE,'.','-'))) AS Ano,
       NUMBTE AS Numero,
       SERIEBTE AS Serie,
       NULL AS Descricao, 
       0 AS Mudanca_Estatuto,
       0 AS Eleicoes,
       1 AS Confianca
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES WHERE instr(NOME_ENTIDADE, 'SIND') <= 0 AND instr(NOME_ENTIDADE, 'TRABALH') <= 0 AND instr(NOME_ENTIDADE, 'PROFISSI') <= 0 AND instr(NOME_ENTIDADE, 'CGTPIN') <= 0 AND instr(NOME_ENTIDADE, 'FEDERA') <= 0;

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
FROM TEMP_ENTIDADES NATURAL JOIN TEMP_ELEICAO_CORPOS_GERENTES WHERE instr(NOME_ENTIDADE, 'SIND') > 0 OR instr(NOME_ENTIDADE, 'TRABALH') > 0 OR instr(NOME_ENTIDADE, 'PROFISSI') > 0 OR instr(NOME_ENTIDADE, 'CGTPIN') > 0  OR instr(NOME_ENTIDADE, 'FEDERA') > 0
GROUP BY ID_Organizacao_Sindical, Data;

UPDATE Org_Sindical SET (Concelho_Sede) = (SELECT TEMP_CONCELHOS.Cnome FROM TEMP_CODIGOS, TEMP_CONCELHOS WHERE TEMP_CODIGOS.num_cod_postal = substr(Org_Sindical.Codigo_Postal,1,4) AND TEMP_CODIGOS.ext_cod_postal = substr(Org_Sindical.Codigo_Postal,6,9) AND TEMP_CONCELHOS.Dcod = TEMP_CODIGOS.cod_distrito AND TEMP_CONCELHOS.Ccod = TEMP_CODIGOS.cod_concelho) WHERE substr(Org_Sindical.Codigo_Postal,6,3) IS NOT NULL;

DROP VIEW TEMP_DATAS_ENTIDADES;
DROP TABLE TEMP_ALTERACOES_ESTATUTOS;
DROP TABLE TEMP_ELEICAO_CORPOS_GERENTES;
DROP TABLE TEMP_ENTIDADES;
DROP TABLE TEMP_PROCESSOS;

CREATE TABLE CAE_SECCOES_TEMP( SECCAO CHAR(1) PRIMARY KEY , RANK, INTEGER, TITLE VARCHAR(100) , SALARY FLOAT );
CREATE TABLE CAE_SECCOES_KEYWORDS_TEMP( SECCAO CHAR(1) , KEYWORD VARCHAR(100) , FOREIGN KEY(SECCAO) REFERENCES CAE_SECCOES_TEMP );

INSERT INTO CAE_SECCOES_TEMP VALUES ( 'A' , 1, 'AGRICULTURA, PRODUÇÃO ANIMAL, CAÇA, FLORESTA E PESCA', 726.3);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'B' , 2, 'INDÚSTRIAS EXTRACTIVAS', 867.2);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'C' , 2, 'INDÚSTRIAS TRANSFORMADORAS', 868.5);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'D' , 2, 'ELECTRICIDADE, GÁS, VAPOR, ÁGUA QUENTE E FRIA E AR FRIO', 867.2);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'E' , 2, 'CAPTAÇÃO, TRATAMENTO E DISTRIBUIÇÃO DE ÁGUA; SANEAMENTO GESTÃO DE RESÍDUOS E DESPOLUIÇÃO', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'F' , 2, 'CONSTRUÇÃO', 798.3);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'G' , 3, 'COMÉRCIO POR GROSSO E A RETALHO; REPARAÇÃO DE VEÍCULOS AUTOMÓVEIS E MOTOCICLOS', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'H' , 2, 'TRANSPORTES E ARMAZENAGEM', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'I' , 3, 'ALOJAMENTO, RESTAURAÇÃO E SIMILARES', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'J' , 3, 'ACTIVIDADES DE INFORMAÇÃO E DE COMUNICAÇÃO', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'K' , 3, 'ACTIVIDADES FINANCEIRAS E DE SEGUROS', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'L' , 3, 'ACTIVIDADES IMOBILIÁRIAS', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'M' , 3, 'ACTIVIDADES DE CONSULTORIA, CIENTÍFICAS, TÉCNICAS E SIMILARES', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'N' , 3, 'ACTIVIDADES ADMINISTRATIVAS E DOS SERVIÇOS DE APOIO', 953.7);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'O' , 3, 'ADMINISTRAÇÃO PÚBLICA E DEFESA; SEGURANÇA SOCIAL OBRIGATÓRIA', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'P' , 3, 'EDUCAÇÃO', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'Q' , 3, 'ACTIVIDADES DE SAÚDE HUMANA E APOIO SOCIAL', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'R' , 3, 'ACTIVIDADES ARTÍSTICAS, DE ESPECTÁCULOS, DESPORTIVAS E RECREATIVAS', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'S' , 3, 'OUTRAS ACTIVIDADES DE SERVIÇOS', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'T' , 3, 'ACTIVIDADES DAS FAMÍLIAS EMPREGADORAS DE PESSOAL DOMÉSTICO E ACTIVIDADES DE PRODUÇÃO DAS FAMÍLIAS PARA USO PRÓPRIO', NULL);
INSERT INTO CAE_SECCOES_TEMP VALUES ( 'U' , 3, 'ACTIVIDADES DOS ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRA-TERRITORIAIS', NULL);

INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'A' , 'AGRICULTURA'), ( 'A' , 'PRODUÇÃO ANIMAL'), ( 'A' , 'CAÇA'), ( 'A' , 'FLORESTA'), ( 'A' , 'PESCA');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'B' , 'INDÚSTRIAS EXTRACTIVAS'), ( 'B' , 'MINAS');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'C' , 'INDÚSTRIAS TRANSFORMADORAS'), ( 'C' , 'TEXTEIS'), ( 'B' , 'TÊXT');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'D' , 'ELECTRICIDADE'), ( 'D' , 'GÁS'), ( 'D' , 'VAPOR'), ( 'D' , 'ÁGUA QUENTE E FRIA'), ( 'D' , 'AR FRIO');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'E' , 'ÁGUA'), ( 'E' , 'SANEAMENTO'), ( 'E' , 'RESÍDUOS'), ( 'E' , 'DESPOLUIÇÃO');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'F' , 'CONSTRUÇÃO');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'G' , 'COMÉRCIO'), ( 'G' , 'REPARAÇÃO DE VEÍCULOS AUTOMÓVEIS'), ( 'G' , 'REPARAÇÃO DE MOTOCICLOS');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'H' , 'TRANSPORTES'), ( 'H' , 'ARMAZENAGEM');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'I' , 'ALOJAMENTO'), ( 'I' , 'RESTAURAÇÃO'), ( 'I' , 'HOTEL');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'J' , 'INFORMAÇÃO E COMUNICAÇÃO'), ( 'J' , 'JORNAL');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'K' , 'FINANÇAS'), ( 'K' , 'SEGUROS');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'L' , 'IMOBILIÁRI');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'M' , 'CONSULTORIA TÉCNICA'), ( 'M' , 'CIENTÍ'), ( 'M' , 'CIÊNT́'), ( 'M' , 'CIÊNCIA');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'N' , 'ACTIVIDADES ADMINISTRATIVAS'), ( 'N' , 'SERVIÇOS');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'O' , 'ADMINISTRAÇÃO PÚBLICA'), ( 'O' , 'DEFESA'), ( 'O' , 'POLÍCIA'), ( 'O' , 'SEGURANÇA PÚBLICA'), ( 'O' , 'SEGURANÇA SOCIAL');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'P' , 'EDUCAÇÃO'), ( 'P' , 'PROFESSORES');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'Q' , 'SAÚDE'), ( 'Q' , 'MEDICOS'), ( 'Q' , 'ENFERMEIROS'), ( 'Q' , 'APOIO SOCIAL');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'R' , 'ARTÍST'), ( 'R' , 'ESPECTÁCULOS'), ( 'R' , 'DESPORTI'), ( 'R' , 'RECREATIV');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'S' , 'OUTROS SERVIÇOS');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'T' , 'PESSOAL DOMÉSTICO');
INSERT INTO CAE_SECCOES_KEYWORDS_TEMP VALUES ( 'U' , 'ORGANISMOS INTERNACIONAIS'), ( 'U' , 'INSTITUIÇÕES EXTRA-TERRITORIAIS');

INSERT INTO Sectores_Profissionais SELECT TITLE AS Sector, SALARY AS Salario_Medio FROM CAE_SECCOES_TEMP;
UPDATE Org_Sindical SET Sector=(SELECT DISTINCT TITLE FROM CAE_SECCOES_TEMP NATURAL JOIN CAE_SECCOES_KEYWORDS_TEMP WHERE instr(Nome,KEYWORD) > 0);
UPDATE Org_Patronal SET Sector=(SELECT DISTINCT TITLE FROM CAE_SECCOES_TEMP NATURAL JOIN CAE_SECCOES_KEYWORDS_TEMP WHERE instr(Nome,KEYWORD) > 0);

DROP TABLE CAE_SECCOES_KEYWORDS_TEMP;
DROP TABLE CAE_SECCOES_TEMP;

--
-- Import data regarding postal codes and cross with entity information
-- 
.mode csv
.separator ";"
.import ./codigos-postais/concelhos.txt TEMP_MUNICIPIOS
.import ./codigos-postais/todos_cp.txt TEMP_CP
CREATE TABLE TEMP_MCP( DESIG VARCHAR(1000) , CP VARCHAR(9) );
INSERT INTO TEMP_MCP 
 SELECT DESIG, CP4 || '-' || CP3 || '-' AS CP FROM TEMP_MUNICIPIOS NATURAL JOIN TEMP_CP 
UNION
 SELECT DESIG, CP4 || CP3 || '-' AS CP FROM TEMP_MUNICIPIOS NATURAL JOIN TEMP_CP 
UNION
 SELECT DESIG, CP4 || '-' AS CP FROM TEMP_MUNICIPIOS NATURAL JOIN TEMP_CP;
UPDATE Org_Sindical SET Codigo_Postal=Codigo_Postal || '-' WHERE Codigo_Postal IS NOT NULL AND NOT(substr(Codigo_Postal, -1)='-');
UPDATE Org_Patronal SET Codigo_Postal=Codigo_Postal || '-' WHERE Codigo_Postal IS NOT NULL AND NOT(substr(Codigo_Postal, -1)='-');
CREATE INDEX TMPIDX1 ON Org_Sindical(Codigo_Postal);
CREATE INDEX TMPIDX2 ON Org_Patronal(Codigo_Postal);
CREATE INDEX TMPIDX3 ON TEMP_MCP(CP);
UPDATE Org_Sindical SET Concelho_Sede=(SELECT DISTINCT UPPER(DESIG) FROM TEMP_MCP WHERE Codigo_Postal = CP);
UPDATE Org_Patronal SET Concelho_Sede=(SELECT DISTINCT UPPER(DESIG) FROM TEMP_MCP WHERE Codigo_Postal = CP);
UPDATE Org_Sindical SET Codigo_Postal=SUBSTR(Codigo_Postal, 0, LENGTH(Codigo_Postal)) WHERE Codigo_Postal IS NOT NULL AND substr(Codigo_Postal, -1)='-';
UPDATE Org_Patronal SET Codigo_Postal=SUBSTR(Codigo_Postal, 0, LENGTH(Codigo_Postal)) WHERE Codigo_Postal IS NOT NULL AND substr(Codigo_Postal, -1)='-';
UPDATE Org_Sindical SET Codigo_Postal=SUBSTR(Codigo_Postal, 0, 4) || '-' || SUBSTR(Codigo_Postal, 5, 3) WHERE Codigo_Postal IS NOT NULL AND instr(Codigo_Postal,'-') <= 0 AND LENGTH(Codigo_Postal)=7;
UPDATE Org_Patronal SET Codigo_Postal=SUBSTR(Codigo_Postal, 0, 4) || '-' || SUBSTR(Codigo_Postal, 5, 3) WHERE Codigo_Postal IS NOT NULL AND instr(Codigo_Postal,'-') <= 0 AND LENGTH(Codigo_Postal)=7;
DROP INDEX TMPIDX1;
DROP INDEX TMPIDX2;
DROP INDEX TMPIDX3;
DROP TABLE TEMP_MCP;
DROP TABLE TEMP_MUNICIPIOS;
DROP TABLE TEMP_CP;

SELECT ORG_SINDICAL.ID, LISTA_OUTORGANTES_UTF.CODENTG, LISTA_OUTORGANTES_UTF.CODENTE, LISTA_OUTORGANTES_UTF.NUMALT, ORG_SINDICAL.NOME, LISTA_OUTORGANTES_UTF.NOME_ENT_E FROM ORG_SINDICAL, LISTA_OUTORGANTES_UTF WHERE (ORG_SINDICAL.ID = LISTA_OUTORGANTES_UTF.CODENTG || '.' ||LISTA_OUTORGANTES_UTF.CODENTE || '.' || LISTA_OUTORGANTES_UTF.NUMALT);
UPDATE ORG_SINDICAL SET NOME = (SELECT d.NOME_ENT_E FROM LISTA_OUTORGANTES_UTF d WHERE ORG_SINDICAL.ID = (d.CODENTG || '.' || d.CODENTE || '.' || d.NUMALT) ) WHERE EXISTS (SELECT d.NOME_ENT_E FROM LISTA_OUTORGANTES_UTF d WHERE ORG_SINDICAL.ID = (d.CODENTG || '.' || d.CODENTE || '.' || d.NUMALT) );
SELECT ORG_SINDICAL.ID, LISTA_OUTORGANTES_UTF.CODENTG, LISTA_OUTORGANTES_UTF.CODENTE, LISTA_OUTORGANTES_UTF.NUMALT, ORG_SINDICAL.NOME, LISTA_OUTORGANTES_UTF.NOME_ENT_E FROM ORG_SINDICAL, LISTA_OUTORGANTES_UTF WHERE (ORG_SINDICAL.ID = LISTA_OUTORGANTES_UTF.CODENTG || '.' ||LISTA_OUTORGANTES_UTF.CODENTE || '.' || LISTA_OUTORGANTES_UTF.NUMALT);

