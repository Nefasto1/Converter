import PyPDF2
import os


# Input: Path of PDF, subfolder name
# Output: A converted PDF in EPUB
def PDF_merge(Path, subfolder):

    # List of PDF to Merge
    PDFlist = [Path + subfolder + '/' + f for f in os.listdir(Path + subfolder)]

    merger = PyPDF2.PdfFileMerger()

    # For each PDF merge it to other
    for PDF in PDFlist:
        name = PDF.split('/')[-1].split('.')[-2]
        merger.append(PyPDF2.PdfFileReader(PDF), name)
        os.remove(PDF)
    
    # Save the new file
    merger.write(Path + f'/{subfolder}.pdf')

    # Delete original directory
    os.rmdir(Path + subfolder)