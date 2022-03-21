from bs4 import BeautifulSoup
from requests_html import HTMLSession

# Input: title of Manga, site selection
# Output: author name, cover URL, eventually new title
def get_author_cover(title, site = 1):
    session = HTMLSession()
    print('\n\nSearching for Manga...')

    # Check the site, if 1 = Mangaworld
    if site == 1:
    
        # Try to get information
        try:

            found = False

            # Connect to the site
            response = session.get(f'https://www.mangaworld.in/archive?keyword={title}&sort=most_read')
            soup = BeautifulSoup(response.html.html, 'html.parser')
            result = soup.find('a', class_ = 'manga-title')

            # Search for another title if no result found
            if not result:
                return get_author_cover(input('\nManga not found, insert another title: '))

            # If found take URL
            if title == result['title']:
                page = result['href']
            
            # If title mismatch select an option
            else:
                choice = input('-'*30
                    + '\nSite: Mangaworld'
                    + '\nTitle mismatch:'
                    + f'\nOriginal: {title}'
                    + f'\nFound: {result["title"]}'
                    +  '\nKeep Going = 1'
                    +  '\nRename = 2'
                    +  '\nSearch for another name = 3'
                    +  '\n' + '-'*30
                    +  '\nAnswer: ')

                # "Keep going" => Save the URL
                if choice == '1':
                    page = result['href']
                
                # "Rename" => Change title and save URL
                elif choice == '2':
                    title = result['title']
                    page = result['href']

                # "Search for another name" => Change the title name
                else:
                    return get_author_cover(input('\nInsert another title: '))

        # If can't get information
        except:
            print('Error, connection failed')
            return None, None, title

        print('Manga found')
        print('Searching for cover and author...')

        # Take information into page
        response = session.get(page)
        soup = BeautifulSoup(response.html.html, 'html.parser')

        try:
            cover = f'--cover={soup.find("img", class_ = "rounded")["src"]}'
        except:
            cover = 'Not Found'

        try:
            author = soup.find("div", class_ = "col-12 col-md-6").find("a").text
        except:
            author = 'Unknown'

        return author, cover, title