import os
from PyPDF4 import PdfFileWriter, PdfFileReader
from ContentGenerators.GlobalTools.SettingsManager import Settings

settings = Settings().data
watermark = settings["DOCUMENT_SETTINGS"]["WATERMARK_PDF_LOCATION"]

def get_file_size(file_path):
    # Get file size in bytes
    try:
        size_bytes = os.path.getsize(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Convert bytes to KB and MB, and round to the tenth place
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024

    size_kb_rounded = round(size_kb, 1)
    size_mb_rounded = round(size_mb, 1)

    # Determine whether to use KB or MB
    if size_mb >= 1:
        return f"{size_mb_rounded} MB"
    else:
        return f"{size_kb_rounded} KB"


def put_watermark(pdfname):
    watermark_instance = PdfFileReader(watermark)
    watermark_page = watermark_instance.getPage(0)
    pdf_reader = PdfFileReader(pdfname)
    pdf_writer = PdfFileWriter()
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(pdfname, 'wb') as out:
        pdf_writer.write(out)