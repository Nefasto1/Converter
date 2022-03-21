import subprocess
import os
from Metadata import get_author_cover


# Input: Main Path
# Output: A file MOBI
def convert_to_MOBI(Path):
    # Convert the PDF files to EPUB files
    PDF_to_EPUB(Path)

    # Convert the EPUB files to MOBI files
    EPUB_to_MOBI(Path)


# Input: Main Path
# Output: A converted PDF in EPUB
def PDF_to_EPUB(Path):

    # List of book in the directory
    bookList = [Path + '/PDF/Not Processed/' + f for f in os.listdir(Path + '/PDF/Not Processed')]
    
    # for each book in list...
    for book in bookList:
        # If is a file convert it
        if os.path.isfile(book): 
            bookName = book.split('/')[-1]
            print('\n\nConverting ' + bookName + ' to EPUB file')

            subprocess.call(['ebook-convert', book, Path + '/Epub/' + bookName.split('.')[-2] + '.epub'])
            
            # Remove PDF file
            if input(f'\nKeep {bookName} file?\nAnswer: ') == 'y':
                os.rename(book, Path + '/PDF/Processed/' + bookName)
            else:
                os.remove(book)


# Input: Main Path
# Output: A converted EPUB in MOBI
def EPUB_to_MOBI(Path):

    # List of book in the directory
    bookList = [Path + '/EPUB/' + f for f in os.listdir(Path + '/EPUB/')]

    # for each book in list...
    for book in bookList:        
        bookName = book.split('/')[-1]
        print('\n\nConverting ' + bookName + ' to MOBI file')

        # Initialize Metadata
        authors = None
        cover = None
        title = bookName.split(".")[-2]

        # While not found search for metadata
        while authors == None and cover == None:
            authors, cover, title = get_author_cover(title)

        # Set variables Metadata
        authorSort = f'--author-sort={authors}'
        authors = f'--authors={authors}'
        titleSort = f'--title-sort={title}'
        title = f'--title={title}'

        # If cover not found set default
        if cover == 'Not Found':
            subprocess.call(['ebook-convert', book, 
                        Path + '/MOBI/' + bookName.split('.')[-2] + '.mobi', 
                        title, titleSort, 
                        authors, authorSort])

        # Else add it
        else:                
            subprocess.call(['ebook-convert', book, 
                        Path + '/MOBI/' + bookName.split('.')[-2] + '.mobi', 
                        title, titleSort, 
                        authors, authorSort,
                        cover])

        # Remove EPUB file
        os.remove(book)
