import io
import os
import urllib.request
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

def extract_text_from_pdf( pdf_path ):
  text = ""
  resource_manager = PDFResourceManager()
  fake_file_handle = io.StringIO()
  converter = TextConverter(resource_manager, fake_file_handle)
  page_interpreter = PDFPageInterpreter(resource_manager, converter)
  with open(pdf_path, 'rb') as fh:
     for page in PDFPage.get_pages(fh, caching=True, check_extractable=True): page_interpreter.process_page(page)
     text = fake_file_handle.getvalue()
  converter.close()
  fake_file_handle.close()
  file = open(pdf_path.replace('.pdf','.txt'), 'w')
  file.write(text)
  file.close()
        
def download_bte( year , number ):      
  filename = "bte" + repr(number) + "_" + repr(year) + ".pdf"
  download_url = "http://bte.gep.msess.gov.pt/completos/" + repr(year) + "/" + filename
  response = urllib.request.urlopen(download_url)
  file = open("../BTE-data/" + filename, 'wb')
  file.write(response.read())
  file.close()
  return filename

for year in range(1977, 2019):
  for number in range(1, 49):
    filename = download_bte( year , number )
    extract_text_from_pdf( "../BTE-data/" + filename )
for fich in os.listdir('../BTE-data/'):
  fich = "../BTE-data/" + fich
  fich2 = "../BTE-data/" + fich + "tmp"
  if fich[-3:]=="pdf": os.system("ps2pdf -dPDFSETTINGS=/ebook %s %s" % (fich,fich2))
  if os.path.isfile(fich2):
    os.remove(fich)
    os.rename(fich2, fich)
