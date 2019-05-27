import io
import urllib2
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
  file = open(filename.replace('.pdf','.txt'), 'wb')
  file.write(text)
  file.close()
    	
def download_bte( year , number ):	
  filename = "bte" + rep(number) + "_" + rep(year) + ".pdf"
  download_url = "http://bte.gep.msess.gov.pt/completos/" + rep(year) + "/" + filename
 	response = urllib2.urlopen(download_url)
  file = open(filename, 'wb')
  file.write(response.read())
  file.close()
	return filename

for year in range(1977, 1978):
	for number in range(1, 49):
		filename = download_bte( year , number )
		extract_text_from_pdf( filename )	
