import os
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from PIL import Image
from PDF import remove_dir
import requests


# Input: None
# Output: Download image from site
def research():
    title = input('\nSite: Mangaworld'
                + '\nInsert a title: ')

    # Search a the title
    session = HTMLSession()
    response = session.get(f'https://www.mangaworld.in/archive?keyword={title}&sort=most_read')
    soup = BeautifulSoup(response.html.html, 'html.parser')

    # Take all the results
    resultList = soup.find_all('a', class_ = 'manga-title')

    for result in resultList:
        # If found download image
        if title in result['title']:
            return get_chapter_list(result['title'], result['href'])
        
        # Else select an option
        else:
            choice = input('\n\n' + '-'*30
                            + '\nTitle mismatch:'
                            + f'\nOriginal: {title}'
                            + f'\nFound: {result["title"]}'
                            +  '\nKeep Going = 1'
                            +  '\nRename = 2'
                            +  '\nNext Result = 3'
                            +  '\nSearch for another name = 4'
                            +  '\n' + '-'*30
                            +  '\nAnswer: ')

            # "Keep Going" => Download image
            if choice == '1':
                return get_chapter_list(title, result['href'])

            # "Rename" => Change title and download image
            elif choice == '2':
                return get_chapter_list(result['title'], result['href'])

            # "Search for another name" => Change title to research
            elif choice == '4':
                return research()

    # Else = next result
    print('\nManga not found')
    return research()

# Input: title of the Manga, URL of the manga
# Output: Downloaded chapter
def get_chapter_list(title, link):
    # Start connection to the page
    session = HTMLSession()
    response = session.get(link)
    soup = BeautifulSoup(response.html.html, 'html.parser')

    # Find all the chapter and title of the manga in the page
    title_ = soup.find('h1', class_ = 'name bigger').text
    chapterList = soup.find_all('a', class_ = 'chap') 
    
    chapterLinks = []

    # Get the single chapter from bottom to the top (the first is at bottom)
    for chapter in reversed(chapterList):
        try:
            # If is a chapter then save the URL in the list, else don't do anything
            if title_ in chapter['title']:
                print(chapter.find('span').text + ' found')
                chapterLinks.append(chapter['href'] + '?style=list')
        except:
            pass

    # Skip chapter or not and download it
    if input(f'\nThere are {len(chapterLinks)} chapter, skip someone?\nAnswer: ') == 'y':
        start = input('Start: ')
        stop = input('Stop: ')
        return get_chapter(chapterLinks, title, int(start), int(stop))

    else:
        return get_chapter(chapterLinks, title, 1, len(chapterLinks))

# Input: A list of URL, title of chapter, first chapter to download, last chapter to download
# Output: Downloaded Chapter
def get_chapter(chapterlist, title, start, stop):
    # Initialize the counter
    c = start

    # In base of number of chapter add some zeros for an ordinated folder
    if stop < 10:
        zeri = 0
    elif stop < 100:
        zeri = 1
    else:
        zeri = 2

    # Remove all the chapter at the start of the list that we don't want
    for i in range(c-1):
        chapterlist.pop(0)

    # Create a folder for the manga, if it exist delete it to clean first
    folder = os.getcwd() + f'/Manga/Not Processed/{title}/'
    if os.path.isdir(folder):
        remove_dir(folder)
        
    os.mkdir(folder)

    # Initialize the variable for skip first and last page
    first = None
    last = None

    # Create a folder for each chapter
    for chapter in chapterlist:
        # If the chapter is one of that we don't want, exit the cycle
        if c >= stop:
            break

        # Select a name for the folder, add some zeros for oredered folders
        if zeri == 2 and c < 10:
            subfolder = folder + f'Capitolo 00{c}/'
        elif (zeri == 2 and c < 100) or (zeri == 1 and c < 10):
            subfolder = folder + f'Capitolo 0{c}/'
        else:
            subfolder = folder + f'Capitolo {c}/'
        
        # Create the folder
        os.mkdir(subfolder)

        print(f'\nCapitolo {c}')
        
        # Download all the image of the chapter and save preferences for first and last page
        first, last = image(chapter, subfolder, first, last)

        c += 1

# Input: chapter link, chapter folder name, boolean to skip first page, boolean to skip last page
# Output: Download the image, boolean to skip first page, boolean to skip last page
def image(chapter, folder, first, last):
    # Connect to the chapter page
    session = HTMLSession()
    response = session.get(chapter)
    soup = BeautifulSoup(response.html.html, 'html.parser')

    # Get all the image
    imageList = soup.find_all('img', class_ = 'page-image img-fluid')

    imageLinks = []

    # Add to list all the image's URL
    for image in imageList:
        imageLinks.append(image['src'])

    # Download the image
    first, last = downloadImage(imageLinks, folder, first, last)

    return first, last

# Input: List of image's URL, chapter folder's name, boolean to skip first page, boolean to skip last page
# Output: Downloaded Image
def downloadImage(imageList, folder, first, last):
    c = 1

    # Remove first and last page for the first time
    if not first and not None:
        imageList.pop(0)
    if not last and not None:
        imageList.pop(-1)
        
    # If is the first time that we see the chapter, see if we want keep first page 
    if first == None:
        first, c = first_page(imageList.pop(0), folder, c)  

        # Keep the last page
        tempImage = imageList.pop(-1) 

    # Download the images
    for image in imageList:
        try:
            # Download the image
            temp = requests.get(image)

            # Select a name for the image, add zeros for ordered files
            if c < 10:
                file = open(folder + f"0{c}.{image.split('.')[-1]}", 'wb')
            else:
                file = open(folder + f"{c}.{image.split('.')[-1]}", 'wb')

            # Save the image
            file.write(temp.content)
            file.close()
            
            print(f'\t\tPage {c} Downloaded')
        
        except:
            pass

        c += 1
    
    #If is the first time that we see the chapter, see if we want to keep last page
    if last == None:
        last = last_page(tempImage, folder, c)      

    return first, last

# Input: Link of the first image, chapter folder's name, the counter of pages
# Output: Preferences for first image
def first_page(image, folder, c):
    # Download the image
    temp = requests.get(image)

    # Select a name for file, add zeros for ordered files
    if c < 10:
        file = open(folder + f"0{c}.{image.split('.')[-1]}", 'wb')
    else:
        file = open(folder + f"{c}.{image.split('.')[-1]}", 'wb')

    # Save the image
    file.write(temp.content)
    file.close()

    # Open the image file
    if c < 10:
        file = open(folder + f"0{c}.{image.split('.')[-1]}", 'rb')
    else:
        file = open(folder + f"{c}.{image.split('.')[-1]}", 'rb')

    # Open the image and show it
    file = Image.open(file)
    file.show()
    file.close()

    # Select to keep first page or not
    if input('\nKeep First page?\nAnswer: ') == 'y':
        first = True
        c += 1
    
    # If not, delete the image
    else:
        first = False
        if c < 10:
            os.remove(folder + f"0{c}.{image.split('.')[-1]}") 
        else:
            os.remove(folder + f"{c}.{image.split('.')[-1]}")  

    return first, c

# Input: Link of last image, chapter folder's name, the counter of pages
# Output: Preferences for last image
def last_page(image, folder, c):
    # Download the image
    temp = requests.get(image)

    # Select a name for file, add zeros for ordered files
    if c < 10:
        file = open(folder + f"0{c}.{image.split('.')[-1]}", 'wb')
    else:
        file = open(folder + f"{c}.{image.split('.')[-1]}", 'wb')

    # Save the image
    file.write(temp.content)
    file.close()

    # Open the image file
    if c < 10:
        file = open(folder + f"0{c}.{image.split('.')[-1]}", 'rb')
    else:
        file = open(folder + f"{c}.{image.split('.')[-1]}", 'rb')
    
    # Open the image and show it
    file = Image.open(file)
    file.show()
    file.close()

    # Select to keep first page or not
    if input('\nKeep Last page?\nAnswer: ') == 'y':
        last = True

    # If not, delete the image
    else:
        last = False
        if c < 10:
            os.remove(folder + f"0{c}.{image.split('.')[-1]}") 
        else:
            os.remove(folder + f"{c}.{image.split('.')[-1]}") 

    return last