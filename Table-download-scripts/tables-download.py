import urllib.request
import json
import csv

'''def getTable(tabela):
	#colocar o url correto quando estiver acessível remotamente
	response = urllib.request.urlopen("https://dgert.gov.pt/dsrcot-rep/" + tabela + ".php")
	data = response.read()	
	result = data.decode("utf8")
	response.close()

	final = json.loads(result)
	#iterar e guardar como csv


	f = open("../Tables-files/"+ tabela + ".txt", "w")
	f.write(result)
	f.close()

getTable("alteracoesEstatutos")
getTable("eleicoesCorposGerentes")
getTable("entidades")
getTable("ircts")
getTable("outorgantes")
getTable("processos")'''


def getResponse(tabela):
	username = ""
	password = ""
	request = urllib.request.Request("https://dgert.gov.pt/dsrcot-rep/" + tabela + ".php")
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   
	response = urllib.request.urlopen(request)
	data = response.read()
	result = data.decode("utf8")
	response.close()
	return result


def getTable_AlteracoesEstatutos():
	result = getResponse("alteracoesEstatutos")
	final = json.loads(result)	
	#iterar e guardar como csv

	contador=1
	f = csv.writer(open("../Tables-files/ALTERACOES_ESTATUTOS.csv", "wb+"))

	f.writerow(["TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO","CODENTG","CODENTE","NUMALT",
		"NUMBTE","DATABTE","SERIEBTE","AMBITO_GEOGRAFICO"])

	#VER DEPOIS AS COLUNAS RETORNADAS DO PHP
	for x in final:
		linha = x["alteracao_" + str(contador)]
		f.writerow([linha["tipo"],linha["especie"],linha["sub_especie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codentg"],linha["codente"],linha["numalt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],linha["ambito_geografico"]])
		contador+=1



def getTable_EleicoesCorposGerentes():
	result = getResponse("eleicoesCorposGerentes")
	final = json.loads(result)	
	#iterar e guardar como csv

	contador=1
	f = csv.writer(open("../Tables-files/ELEICAO_CORPOS_GERENTES.csv", "wb+"))

	f.writerow(["CODENTG","CODENTE","NUMALT","NUMERO_ELEICAO","DATA_ELEICAO","INSCRITOS","VOTANTES","MESES_MANDATO",
		"DATABTE","NUMBTE","SERIEBTE","NUMMAXEFECT","NUMMINEFECT","NUMMAXSUPL","NUMMINSUPL","NUM_H_EFECT","NUM_H_SUPL",
		"NUM_M_EFECT","NUM_M_SUPL","TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO"])


	#VER DEPOIS AS COLUNAS RETORNADAS DO PHP
	for x in final:
		linha = x["alteracao_" + str(contador)]
		f.writerow([linha["tipo"],linha["especie"],linha["sub_especie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codentg"],linha["codente"],linha["numalt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],linha["ambito_geografico"]])
		contador+=1



def getTable_Entidades():
	result = getResponse("entidades")
	final = json.loads(result)	
	#iterar e guardar como csv

	contador=1
	f = csv.writer(open("../Tables-files/ENTIDADES.csv", "wb+"))

	f.writerow(["CODENTG","CODENTE","NUMALT","SIGLA","NOME_ENTIDADE","CODIGOPOSTAL_ENTIDADE","ID_DISTRITO","DISTRITO_DESCRICAO",
		"ESTADO_ENTIDADE"])

	#VER DEPOIS AS COLUNAS RETORNADAS DO PHP
	for x in final:
		linha = x["alteracao_" + str(contador)]
		f.writerow([linha["tipo"],linha["especie"],linha["sub_especie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codentg"],linha["codente"],linha["numalt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],linha["ambito_geografico"]])
		contador+=1



def getTable_Ircts():
	result = getResponse("ircts")
	final = json.loads(result)	
	#iterar e guardar como csv

	contador=1
	f = csv.writer(open("../Tables-files/IRCT.csv", "wb+"))

	f.writerow(["NUMERO","NUMERO_SEQUENCIAL","ANO","TIPO_CONVENCAO_CODIGO","TIPO_CONVENCAO_DESCR",
	 	"TIPO_CONVENCAO_DESCR_LONG","TIPO_CONVENCAO_ORDEM","NATUREZA_CODIGO","NATUREZA_DESCRICAO","NOMECC",
     	"AMBITO_GEOGRAFICO_IRCT","AMBITO_GEOGRAFICO_CODE_IRCT","NUMBTE","DATABTE","SERIEBTE","AMBGEG",
     	"DATA_EFEITOS","AREA","DIST","CONC","PROV","COD_CAE"])

    #VER DEPOIS AS COLUNAS RETORNADAS DO PHP
	for x in final:
		linha = x["alteracao_" + str(contador)]
		f.writerow([linha["tipo"],linha["especie"],linha["sub_especie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codentg"],linha["codente"],linha["numalt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],linha["ambito_geografico"]])
		contador+=1



def getTable_Outorgantes():
	result = getResponse("outorgantes")
	final = json.loads(result)	
	#iterar e guardar como csv

	contador=1
	f = csv.writer(open("../Tables-files/OUTORGANTES.csv", "wb+"))

	f.writerow(["NUMERO","NUMERO_SEQUENCIAL","ANO","TIPO_CONVENCAO_CODIGO","CODENTG","CODENTE",
		"NUMALT","SIGLA_ENT_E","NOME_ENT_E"])

	#VER DEPOIS AS COLUNAS RETORNADAS DO PHP
	for x in final:
		linha = x["alteracao_" + str(contador)]
		f.writerow([linha["tipo"],linha["especie"],linha["sub_especie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codentg"],linha["codente"],linha["numalt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],linha["ambito_geografico"]])
		contador+=1



def getTable_Processos():
	result = getResponse("processos")
	final = json.loads(result)	
	#iterar e guardar como csv

	contador=1
	f = csv.writer(open("../Tables-files/PROCESSOS.csv", "wb+"))

	f.writerow(["TIPO","ESPECIE","SUB_ESPECIE","NUMERO","ANO","CONTROLO","SERVICO","COD_ASSUNTO",
		"ASSUNTO","DESIGNACAO","TITULO","DATA_ABERTURA_PROCESSO"])

	#VER DEPOIS AS COLUNAS RETORNADAS DO PHP
	for x in final:
		linha = x["alteracao_" + str(contador)]
		f.writerow([linha["tipo"],linha["especie"],linha["sub_especie"],linha["numero"],linha["ano"],linha["controlo"],
			linha["servico"],linha["codentg"],linha["codente"],linha["numalt"],linha["numBTE"],linha["dataBTE"],
			linha["serieBTE"],linha["ambito_geografico"]])
		contador+=1


'''def getTab():
	#colocar o url correto quando estiver acessível remotamente
	response = urllib.request.urlopen("https://www.dropbox.com/s/ht0tg0489i7ejr7/testar.txt?dl=1")
	data = response.read()
	result = data.decode("utf8")
	response.close()

getTab()'''


