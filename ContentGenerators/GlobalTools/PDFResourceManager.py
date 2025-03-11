# PDF Resource Manager for the GemEssayGenerator
# Author Sami Chemali
import io
from pathlib import Path
import PyPDF4
import requests
import fitz
from random import randint
import os


def CheckPDF(url):
    try:
        response = requests.get(url)
        pdf_content = io.BytesIO(response.content)
        pdf = PyPDF4.PdfFileReader(pdf_content)
        return pdf.getNumPages() > 0
    except (requests.exceptions.RequestException, PyPDF4.utils.PdfReadError):
        return False


def ExtractText(url):
    try:
        filename = "Resource" + str(randint(0, 999999999999999999999999999)) + ".pdf"
        # DOWNLOAD THE PDF FROM THE URL PROVIDED
        filename = Path(filename)
        response = requests.get(url)
        filename.write_bytes(response.content)
        # EXTRACT THE TEXT FROM THE PDF
        doc = fitz.open(filename)
        text = ""
        for page in doc:
            text += page.get_text()
        text = text[0:5000]
        doc.close()
        os.remove(filename)
        return text
    except:
        return 'error'
