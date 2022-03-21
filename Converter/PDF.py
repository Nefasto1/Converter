import os
from PIL import Image
from Merge import PDF_merge


# Input: Folder's Path
# Output: Delete the folder
def remove_dir(Path):

    # Take all the element in the folder
    for fold in os.listdir(Path):
        locPath = Path + '/' + fold

        # If the file is a directory recall the function
        if os.path.isdir(locPath):
            remove_dir(locPath)

        # If is a file remove it
        else:
            os.remove(locPath)
        
    # Delete the directory
    os.rmdir(Path)


# Input: None
# Output: Two Boolean variables to select the PDF file style
def menu():

    s = ('-'*82 
        + '\n|        1)      |                2)              |               3)             |' 
        + '\n|   Single PDF   |   Single PDF for each folder   |   Single PDF for subfolder   |\n' 
        + '-'*82)

    try:
        a = int(input(s + '\nAnswer: ')) 
    except:
        pass

    if a == 1:
        a = True
        b = True
    elif a == 2:
        a = False
        b = True
    else:
        a = False
        b = False

    return a, b


# Input: Main Path
# Output: Converted Files
def convert_to_PDF(Path):

    Path += "/Manga/"

    # Get all the Manga to convert
    mangaList = get_dir(Path + 'Not Processed/')

    # If the directory isn't empty
    if mangaList:

        # Select the PDF mode
        a,b = menu()

        # Get all the Chapter
        print('\nScan Folder...')
        chapterList = get_chapterList(mangaList, "Manga", a)

        # Get all the Image
        print('\nScan Subfolder...')
        imageList = get_imageList(chapterList, a, b)

        # Convert the Image to PDF
        check_convertion(imageList, a, b)

        # Select if delete the image or not
        for manga in os.listdir(Path + 'Not Processed/'):
            if input(f'\nKeep {manga} image?\nAnswer: ') == 'y':
                os.rename(Path + 'Not Processed/' + manga, Path + 'Processed/' + manga)
            else:
                remove_dir(Path + 'Not Processed/' + manga)


def check_convertion(imageList, singleFolder = True, singleSub = True):
    #Single PDF
    if singleFolder and singleSub :
        print(f'Converting file')
        convert(imageList, 'Merged')

    # A PDF that merge the subfolder but not the main folder
    elif singleSub:
        # Convert a folder at time
        for firstFolder in imageList:
            foldName = firstFolder[0].split('/')[-3]
            print(f"Converting folder: {foldName}")

            convert(firstFolder, foldName)

    # A PDF for each subfolder
    else:
        # Convert a folder a time
        for firstFolder in imageList:
            folderName = firstFolder[0]
            mangaName = folderName.split('/')[-2]
            folderName = folderName.split('/')[-3]

            print(f"Converting folder: {folderName}")

            # Check if the directory exist, if not create it
            if not os.path.isdir(os.getcwd() + "/PDF/Not Processed/" + folderName):
                os.mkdir(os.getcwd() + "/PDF/Not Processed/" + folderName)

            convert(firstFolder, mangaName, True, folderName + '/')
        
        # Merge the chapter in a single PDF
        if input('\nDo you want to merge the file?\nAnswer: ') == 'y':
            Path = os.getcwd() + '/PDF/Not Processed/'
            folder = os.listdir(Path)

            # Take a directory at time and merge that
            for dir in folder:
                if os.path.isdir(Path + dir):
                    print(f'Merging {dir}\'s PDFs')
                    PDF_merge(Path, dir)


# Input: Folder's Path, Name of file, Boolean to show the Subfolder name, Subfolder name
# Output: File PDF stored in the relative path
def convert(folder, name = "filename", show = False, subfolder = ''):
    # Show the subfolder's name
    if show:
        print(f"\t-Subfolder: {folder[0].split('/')[-2]}")

    # Remove the first image to use it as the main
    im = folder[0]
    folder.remove(im)
    im = Image.open(im)
    im = im.convert('RGB')

    # Take each image in the folder
    openedImage = []
    for image in folder:
        print(f"\t\t-Image: {image.split('/')[-1]}")

        # Try to open the image 
        try:
            tmp = Image.open(image)
            x,y = tmp.size[0], tmp.size[1]
            
            # if it's more large than high it is rotated
            if x > y:
                tmp = tmp.transpose(Image.ROTATE_90)
                tmp = tmp.resize((959, 1400))
            
            # Convert in "RGB" mode (resolve some bug of conversion to PDF)
            tmp = tmp.convert('RGB')
            
            # Add the image to the list of opened image
            openedImage.append(tmp)

        # If an error occurred, skip the image
        except:
            print(f'Error, skipped')

    # Convert the image in PDF and append the list of images
    im.save(os.getcwd() + "/PDF/Not Processed/" + subfolder + name + ".pdf", "PDF", resolution = 100.0, save_all = True, append_images = openedImage)

   
# Input: Folder's Path, Folder's Name, A boolean that is "True" if you need one PDF for each folder (merge all the subfolder files but not of main folder)
# Output: A list of chapter inside a folder
def get_chapterList(folder, name = "Manga", singleFolder = True):
    # A PDF for each folder
    if singleFolder:
        chapterList = get_subfolder(folder, name)
    
    # A PDF that merge all the folder
    else:
        chapterList = []
        for sub in folder:
            chapterList.append(get_subfolder([sub], name))
    
    return chapterList


# Input: Folder's Path, Single PDF for each folder, Single PDF for each subfolder
# Output: A list of Image
def get_imageList(folder, singleFolder = True, singleSub = True):
    # A single PDF
    if singleFolder and singleSub:
            imageList = get_image(folder)

    # A PDF that merge the subfolder but not the main folder
    elif singleSub:
        imageList = []
        for sub in folder:
                imageList.append(get_image(sub))

    # A PDF for each subfolder
    else:
        imageList = []
        for sub in folder:
            for image in sub:
                imageList.append(get_image([image]))

    return imageList


# Input: Folder's Path
# Output: A list of image's path in the folder
def get_image(folder):
    imageList = []

    subfolder = get_subfolder(folder, "Chapter")

    # Get all the file that have "jpg" or "png" in the path
    for item in subfolder:
        if "png" in item or "jpg" in item:
            imageList.append(item[0:-1])

    return imageList


# Input: A list of folder's path and a name of the "Main" folder
# Output: A list that contains a list for each folder in the list
def get_subfolder(folderList, name = "Folder"):
    subfolderList = []

    # Take all the subfolder and append the list to the main list
    for folder in folderList:
        folderName = folder.split("/")[-2]
        print (name + " " + folderName)

        subfolderList += get_dir(folder)

    return subfolderList


# Input: Folder's Path
# Output: A list that contains all the path of file in a folder
def get_dir(folder):
    return [folder + f + '/' for f in os.listdir(folder)]