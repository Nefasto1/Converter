from os import getcwd
from Download import research
from PDF import convert_to_PDF
from MOBI import convert_to_MOBI
from Mail import send_book

if __name__ == "__main__":
    
    # Get the path of file
    basePath = getcwd()

    # Select to search a manga or not
    while input('Search a manga?\nAnswer: ') == 'y':
        research()

    # Convert Image to PDF files
    convert_to_PDF(basePath)

    # Convert PDF to MOBI files
    convert_to_MOBI(basePath)

    # Send them by mail
    send_book(basePath)