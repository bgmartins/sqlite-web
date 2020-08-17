import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import json
import csv
import base64


#sem autenticacao
def getTable(tabela):
	#colocar o url correto quando estiver acessível remotamente
	response = urllib.request.urlopen("https://www.dgert.gov.pt/application-dgert-projeto-rep-php/" + tabela + ".php")
	data = response.read()	
	result = data.decode("utf8")
	response.close()

	return result


#com autenticacao
def getResponse(tabela):
	username = ""
	password = ""
	request = urllib.request.Request("https://www.dgert.gov.pt/application-dgert-projeto-rep-php/" + tabela + ".php")
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   
	response = urllib.request.urlopen(request)
	data = response.read()
	result = data.decode("utf8")
	response.close()
	return result


def getTable_AlteracoesEstatutos():
	result = getTable("alteracoesEstatutos")
	final = json.loads(result)	

	f = csv.writer(open("../Tables-files/ALTERACOES_ESTATUTOS.csv","w",newline=''))

	f.writerow(["TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO","CODENTG","CODENTE","NUMALT",
		"NUMBTE","DATABTE","SERIEBTE","AMBITO_GEOGRAFICO"])

	for key in final:
		linha = final[key]

		if "ambitoGeografico" not in linha:
			ambGeo = ""
		else:
			ambGeo = linha["ambitoGeografico"]

		f.writerow([linha["tipo"],linha["especie"],linha["subEspecie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codEntG"],linha["codEntE"],linha["numAlt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],ambGeo])



def getTable_EleicoesCorposGerentes():
	result = getTable("eleicoesCorposGerentes")
	final = json.loads(result)	

	f = csv.writer(open("../Tables-files/ELEICAO_CORPOS_GERENTES.csv","w",newline=''))

	f.writerow(["CODENTG","CODENTE","NUMALT","NUMERO_ELEICAO","DATA_ELEICAO","INSCRITOS","VOTANTES","MESES_MANDATO",
		"DATABTE","NUMBTE","SERIEBTE","NUMMAXEFECT","NUMMINEFECT","NUMMAXSUPL","NUMMINSUPL","NUM_H_EFECT","NUM_H_SUPL",
		"NUM_M_EFECT","NUM_M_SUPL","TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO"])

	for key in final:
		linha = final[key]

		if "servico" not in linha:
			servico = ""
		else:
			servico = linha["servico"]

		f.writerow([linha["codEntG"],linha["codEntE"],linha["numAlt"],linha["numeroEleicao"],linha["dataEleicao"],linha["inscritos"],
			linha["votantes"],linha["mesesMandato"],linha["dataBTE"],linha["numBTE"],linha["serieBTE"],linha["numMaxEfect"],
			linha["numMinEfect"],linha["numMaxSupl"],linha["numMinSupl"],linha["numHEfect"],linha["numHSupl"],linha["numMEfect"],
			linha["numMSupl"],linha["tipo"],linha["especie"],linha["subEspecie"],linha["numero"],linha["ano"],linha["controlo"],servico])



def getTable_Entidades():
	result = getTable("entidades")
	final = json.loads(result)

	f = csv.writer(open("../Tables-files/ENTIDADES.csv","w",newline=''))

	f.writerow(["CODENTG","CODENTE","NUMALT","SIGLA","NOME_ENTIDADE","CODIGOPOSTAL_ENTIDADE","ID_DISTRITO","DISTRITO_DESCRICAO","ESTADO_ENTIDADE"])

	for key in final:
		linha = final[key]

		if "sigla" not in linha:
			sigla = ""
		else:
			sigla = linha["sigla"]

		f.writerow([linha["codEntG"],linha["codEntE"],linha["numAlt"],sigla,linha["nomeEntidade"],linha["codigoPostalEntidade"],
			linha["idDistrito"],linha["distritoDescricao"],linha["estadoEntidade"]])


#VER DEPOIS AS COLUNAS RETORNADAS DO PHP
def getTable_Ircts():
	result = getResponse("ircts")
	final = json.loads(result)	
	#iterar e guardar como csv

	f = csv.writer(open("../Tables-files/IRCT.csv","w",newline=''))

	f.writerow(["NUMERO","NUMERO_SEQUENCIAL","ANO","TIPO_CONVENCAO_CODIGO","TIPO_CONVENCAO_DESCR",
	 	"TIPO_CONVENCAO_DESCR_LONG","TIPO_CONVENCAO_ORDEM","NATUREZA_CODIGO","NATUREZA_DESCRICAO","NOMECC",
     	"AMBITO_GEOGRAFICO_IRCT","AMBITO_GEOGRAFICO_CODE_IRCT","NUMBTE","DATABTE","SERIEBTE","AMBGEG",
     	"DATA_EFEITOS","AREA","DIST","CONC","PROV","COD_CAE"])
  
	for key in final:
		linha = final[key]
		f.writerow([linha["tipo"],linha["especie"],linha["sub_especie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codentg"],linha["codente"],linha["numalt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],linha["ambito_geografico"]])


#VER DEPOIS AS COLUNAS RETORNADAS DO PHP
def getTable_Outorgantes():
	result = getResponse("outorgantes")
	final = json.loads(result)	
	#iterar e guardar como csv

	f = csv.writer(open("../Tables-files/OUTORGANTES.csv","w",newline=''))

	f.writerow(["NUMERO","NUMERO_SEQUENCIAL","ANO","TIPO_CONVENCAO_CODIGO","CODENTG","CODENTE",
		"NUMALT","SIGLA_ENT_E","NOME_ENT_E"])

	for key in final:
		linha = final[key]
		f.writerow([linha["tipo"],linha["especie"],linha["sub_especie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codentg"],linha["codente"],linha["numalt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],linha["ambito_geografico"]])



def getTable_Processos():
	result = getTable("processos")
	final = json.loads(result)	

	f = csv.writer(open("../Tables-files/PROCESSOS.csv","w",newline=''))

	f.writerow(["TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO","COD_ASSUNTO",
		"ASSUNTO","DESIGNACAO","TITULO","DATA_ABERTURA_PROCESSO"])

	for key in final:
		linha = final[key]

		if "dataAberturaProcesso" not in linha:
			dataAP = ""
		else:
			dataAP = linha["dataAberturaProcesso"]

		f.writerow([linha["tipo"],linha["especie"],linha["subEspecie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codAssunto"],linha["assunto"],linha["designacao"],linha["titulo"],dataAP])

