import sys
sys.stdout.reconfigure(encoding='utf-8')
from googlesearch import search
import sqlite3

conn = None
try:
    conn = sqlite3.connect("./rep-database.db")
except Error as e:
    print(e)

c = conn.cursor()

def websites_Sindicais():

	c.execute('SELECT DISTINCT Nome FROM Org_Sindical;')

	websites_sindicais = open("./websites/websites_sindicais.txt", "w",encoding="utf8")
	websites_sindicais.write("Nome_Org;Website")
	websites_sindicais.write("\n")


	#verificar por parlamento e bte e .pdf
	#verificar por racius

	for row in c.fetchall():
		org_name = row[0]
		url = search(org_name, num_results=5)
		for link in url:
			if len(link)==0:
				websites_sindicais.write(org_name + ";" + " ")
				break
			
			if not (("parlamento" in link and ".pdf" in link) or ("bte" in link and ".pdf" in link) or ("racius" in link)):
				websites_sindicais.write(org_name + ";" + link)
				break

		websites_sindicais.write("\n")

	websites_sindicais.close()


def websites_Patronais():
	
	c.execute('SELECT DISTINCT Nome FROM Org_Patronal;')

	websites_patronais = open("./websites/websites_patronais.txt", "w",encoding="utf8")
	websites_patronais.write("Nome_Org;Website")
	websites_patronais.write("\n")

	#verificar por parlamento e bte e .pdf
	#verificar por racius

	for row in c.fetchall():
		org_name = row[0]
		url = search(org_name, num_results=5)
		for link in url:
			if len(link)==0:
				websites_patronais.write(org_name + ";" + " ")
				break
			
			if not (("parlamento" in link and ".pdf" in link) or ("bte" in link and ".pdf" in link) or ("racius" in link)):
				websites_patronais.write(org_name + ";" + link)
				break
		
		websites_patronais.write("\n")

	websites_patronais.close()

