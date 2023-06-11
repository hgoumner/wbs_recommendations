# import modules
from bs4 import BeautifulSoup
from requests import get, head

HEADER = {'Accept-Language': 'en-US,en;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}


def get_imdb_cover_image_url(imdbId):
    ''' get cover image of given movie '''

    url = f'https://www.imdb.com/title/tt{imdbId}/'

    response = get(url, headers=HEADER)

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        cover_url = soup.find(name='img', attrs={'class': 'ipc-image'})['src']
        return cover_url
    except Exception as e:
        return None


def get_imdb_cover_image_status_code(imdbId):
    ''' get cover image of given movie '''

    url = f'https://www.imdb.com/title/tt{imdbId}/'

    response = head(url, headers=HEADER)

    return response.status_code


def get_tmdb_cover_image_url(tmdbId):
    ''' get cover image of given movie '''

    url = f'https://www.themoviedb.org/movie/{tmdbId}/'

    response = get(url, headers=HEADER)

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        cover_url = soup.find(name='img', attrs={'class': 'poster lazyload lazyloaded'})['src']
        return 'https://www.themoviedb.org/' + str(cover_url)
    except Exception as e:
        return None


def get_tmdb_cover_image_status_code(tmdbId):
    ''' get cover image of given movie '''

    url = f'https://www.themoviedb.org/movie/{tmdbId}/'

    response = head(url, headers=HEADER)

    return response.status_code