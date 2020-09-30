import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import json
import csv
import base64

#com autenticacao
def getResponse(tabela, ano):
	username = "projeto-rep"
	password = "YXA797B*fU)etGH"
	request = urllib.request.Request("https://www.dgert.gov.pt/application-dgert-projeto-rep-php/" + tabela + ".php?ano=" + str(ano))
	string = '%s:%s' % (username, password)
	base64string = base64.standard_b64encode(string.encode('utf-8'))
	request.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))   
	response = urllib.request.urlopen(request)
	data = response.read()
	result = data.decode("utf8")
	response.close()
	return result


def getTable_AlteracoesEstatutos(ano, csvWriter):
	result = getResponse("alteracoesEstatutos", ano)
	final = json.loads(result)
	
	for key in final:	
		linha = final[key]
		
		if "ambitoGeografico" not in linha:
			ambGeo = ""
		else:
			ambGeo = linha["ambitoGeografico"]

		csvWriter.writerow([linha["tipo"],linha["especie"],linha["subEspecie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codEntG"],linha["codEntE"],linha["numAlt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],ambGeo])


def alteracoesEstatutos():

	altEst = csv.writer(open("../Tables-files/ALTERACOES_ESTATUTOS.csv","a",newline=''))

	altEst.writerow(["TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO","CODENTG","CODENTE","NUMALT",
		"NUMBTE","DATABTE","SERIEBTE","AMBITO_GEOGRAFICO"])

	for ano in range(1977,2020):
		getTable_AlteracoesEstatutos(ano, altEst)
		print("ano " + str(ano) + " concluido \n")

	print("Tabela ALTERACOES_ESTATUTOS extraída")




def getTable_EleicoesCorposGerentes(ano, csvWriter):
	result = getResponse("eleicoesCorposGerentes", ano)
	final = json.loads(result)	

	for key in final:
		linha = final[key]

		if "servico" not in linha:
			servico = ""
		else:
			servico = linha["servico"]

		csvWriter.writerow([linha["codEntG"],linha["codEntE"],linha["numAlt"],linha["numeroEleicao"],linha["dataEleicao"],linha["inscritos"],
			linha["votantes"],linha["mesesMandato"],linha["dataBTE"],linha["numBTE"],linha["serieBTE"],linha["numMaxEfect"],
			linha["numMinEfect"],linha["numMaxSupl"],linha["numMinSupl"],linha["numHEfect"],linha["numHSupl"],linha["numMEfect"],
			linha["numMSupl"],linha["tipo"],linha["especie"],linha["subEspecie"],linha["numero"],linha["ano"],linha["controlo"],servico])


def eleicoesCorposGerentes():
	
	eleicCorpG = csv.writer(open("../Tables-files/ELEICAO_CORPOS_GERENTES.csv","a",newline=''))

	eleicCorpG.writerow(["CODENTG","CODENTE","NUMALT","NUMERO_ELEICAO","DATA_ELEICAO","INSCRITOS","VOTANTES","MESES_MANDATO",
		"DATABTE","NUMBTE","SERIEBTE","NUMMAXEFECT","NUMMINEFECT","NUMMAXSUPL","NUMMINSUPL","NUM_H_EFECT","NUM_H_SUPL",
		"NUM_M_EFECT","NUM_M_SUPL","TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO"])

	for ano in range(1977,2020):
		getTable_EleicoesCorposGerentes(ano, eleicCorpG)
		print("ano " + str(ano) + " concluido \n")

	print("Tabela ELEICAO_CORPOS_GERENTES extraída")


def getTable_Entidades(ano, csvWriter):
	result = getResponse("entidades", ano)
	final = json.loads(result)

	for key in final:
		linha = final[key]

		if "sigla" not in linha:
			sigla = ""
		else:
			sigla = linha["sigla"]

		csvWriter.writerow([linha["codEntG"],linha["codEntE"],linha["numAlt"],sigla,linha["nomeEntidade"],linha["codigoPostalEntidade"],
			linha["idDistrito"],linha["distritoDescricao"],linha["estadoEntidade"]])

def entidades():
	ent = csv.writer(open("../Tables-files/ENTIDADES.csv","a",newline=''))

	ent.writerow(["CODENTG","CODENTE","NUMALT","SIGLA","NOME_ENTIDADE","CODIGOPOSTAL_ENTIDADE","ID_DISTRITO","DISTRITO_DESCRICAO","ESTADO_ENTIDADE"])

	for ano in range(1977,2020):
		getTable_Entidades(ano, ent)
		print("ano " + str(ano) + " concluido \n")

	print("Tabela Entidades Extraída")


#VER DEPOIS AS COLUNAS RETORNADAS DO PHP
def getTable_Ircts(ano, csvWriter):
	result = getResponse("ircts", ano)
	final = json.loads(result)
  
	for key in final:
		
		linha = final[key]

		if "dataEfeitos" not in linha:
			dataEfeitos = ""
		else:
			dataEfeitos = linha["dataEfeitos"]
		
		csvWriter.writerow([linha["numero"],linha["numeroSequencial"],linha["ano"],linha["tipoConvencaoCodigo"],linha["tipoConvencaoDescr"],linha["tipoConvencaoDescrLong"],
			linha["tipoConvencaoOrdem"],linha["naturezaCodigo"],linha["naturezaDescricao"],linha["nomeCC"],linha["ambitoGeograficoIRCT"],linha["ambitoGeograficoCodeIRCT"],
			linha["numBTE"],linha["dataBTE"],linha["serieBTE"],linha["ambGeg"],dataEfeitos,linha["area"],linha["dist"],linha["conc"],linha["prov"],linha["codCAE"]])


def ircts():
	ircts = csv.writer(open("../Tables-files/IRCT.csv","a",newline=''))

	ircts.writerow(["NUMERO","NUMERO_SEQUENCIAL","ANO","TIPO_CONVENCAO_CODIGO","TIPO_CONVENCAO_DESCR",
	 	"TIPO_CONVENCAO_DESCR_LONG","TIPO_CONVENCAO_ORDEM","NATUREZA_CODIGO","NATUREZA_DESCRICAO","NOMECC",
     	"AMBITO_GEOGRAFICO_IRCT","AMBITO_GEOGRAFICO_CODE_IRCT","NUMBTE","DATABTE","SERIEBTE","AMBGEG",
     	"DATA_EFEITOS","AREA","DIST","CONC","PROV","COD_CAE"])

	for ano in range(1977,2020):
		getTable_Ircts(ano, ircts)
		print("ano " + str(ano) + " concluido \n")

	print("Tabela IRCTS Extraída")



def getTable_Outorgantes(ano, csvWriter):
	result = getResponse("outorgantes", ano)
	final = json.loads(result)

	for key in final:

		linha = final[key]

		if "siglaEntE" not in linha:
			siglaEntE = ""
		else:
			siglaEntE = linha["siglaEntE"]

		csvWriter.writerow([linha["numero"],linha["numSeq"],linha["ano"],linha["tipoConv"],linha["CodEntG"],linha["CondEntE"],
			linha["numAlt"],siglaEntE,linha["nomeEntE"]])


def outorgantes():
	outorg = csv.writer(open("../Tables-files/OUTORGANTES.csv","a",newline=''))

	outorg.writerow(["NUMERO","NUMERO_SEQUENCIAL","ANO","TIPO_CONVENCAO_CODIGO","CODENTG","CODENTE",
		"NUMALT","SIGLA_ENT_E","NOME_ENT_E"])

	for ano in range(1977,2020):
		getTable_Outorgantes(ano, outorg)
		print("ano " + str(ano) + " concluido \n")

	print("Tabela Outorgantes Extraída")


def getTable_Processos(ano, csvWriter):
	result = getResponse("processos", ano)
	final = json.loads(result)	

	for key in final:
		linha = final[key]

		if "dataAberturaProcesso" not in linha:
			dataAP = ""
		else:
			dataAP = linha["dataAberturaProcesso"]

		csvWriter.writerow([linha["tipo"],linha["especie"],linha["subEspecie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codAssunto"],linha["assunto"],linha["designacao"],linha["titulo"],dataAP])



def processos():
	proc = csv.writer(open("../Tables-files/PROCESSOS.csv","a",newline=''))

	proc.writerow(["TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO","COD_ASSUNTO",
		"ASSUNTO","DESIGNACAO","TITULO","DATA_ABERTURA_PROCESSO"])

	for ano in range(1977,2020):
		getTable_Processos(ano, proc)
		print("ano " + str(ano) + " concluido \n")

	print("Tabela Processos Extraída")


processos()